# HAM (Home Automation Machine)

This is version two of HAM ([see version one](https://github.com/scottsweb/ham/tree/master)), the host machine is now running [Fedora Silverblue](https://silverblue.fedoraproject.org/) and uses [Podman](https://podman.io/) instead of Docker. This allows the containers to run rootless and have a slightly more stable system upon which to build my #homelab. I have also upgraded from a Raspberry Pi to a x86 system with a small footprint and low power demands.

I am mostly just publishing the relevant `docker-compose` / `podman-compose` files that are grouped into pods around certain pieces of functionality like home automation or media. I think this makes more sense, especially as more of my Home Assistant config is moved from YAML to the database.

## General / OS tweaks

### Packages

I layer the following packages:

```
rpm-ostree install sshfs docker-compose podman-docker podman-compose wireguard-tools cronie
```

`podman-docker` allows you to use the [Monitor Docker Home Assistant component](https://github.com/ualex73/monitor_docker) for automating and monitoring containers.

### Podman

Enable the Podman socket and set the `DOCKER_HOST` environment variable for more Docker like behaviour:

```
systemctl --user enable podman.socket
systemctl --user start podman.socket
systemctl --user status podman.socket
```

Add the following to your `~/.bash_profile`

```
export DOCKER_HOST=unix:///run/user/$UID/podman/podman.sock
```

Reference: [Use Docker Compose with Podman](https://fedoramagazine.org/use-docker-compose-with-podman-to-orchestrate-containers-on-fedora/)

Test the Docker API with:

```
sudo curl -H "Content-Type: application/json" --unix-socket /run/user/1000/podman/podman.sock http://localhost/_ping
```

Reference: [Using Podman and Docker Compose](https://www.redhat.com/sysadmin/podman-docker-compose)

Start the Podman restart service (restarts containers set to `restart: always`) after a reboot:

```
systemctl --user enable podman-restart.service
systemctl --user start podman-restart.service
```

### Allow long running tasks

As Silverblue is a desktop OS, it tries to shutdown long running tasks (including Podman containers). This can be turned off by running: `loginctl enable-linger`, check the status with `ls /var/lib/systemd/linger`, then reboot.

### Connectivity check

Fedora has a built in connectivity check that phones home rather frequently. It's probably more useful on a system that uses WiFi, but as this machine is connected via Ethernet I decided to turn it off. `sudo nano /etc/NetworkManager/NetworkManager.conf`:

```
[connectivity]
enabled=false
uri=http://fedoraproject.org/static/hotspot.txt
response=OK
interval=300
```

Then run `systemctl restart NetworkManager` for the changes to be picked up.

### SSH

Tweak some SSH settings to restrict access:

```
PermitRootLogin	no
PermitEmptyPasswords no
X11Forwarding no
PasswordAuthentication no
AllowUsers username@192.168.1.* username@10.80.x.x (example for more IPs)
```

These tweaks can be added to `/etc/sshd/sshd_config.d/50-redhat.conf` and applied with `sudo systemctl reload sshd`.

### Cron

`cronie` is a layered package (`rpm-ostree install cronie`).

```
sudo nano /etc/cron.allow
# add your username

systemctl enable crond.service
systemctl start crond.service

crontab -e
```

Reference: [Scheduling tasks with Cron](https://fedoramagazine.org/scheduling-tasks-with-cron/), [Automating System Tasks](https://docs.fedoraproject.org/en-US/fedora/latest/system-administrators-guide/monitoring-and-automation/Automating_System_Tasks/)

### USB sleep / Auto suspend

To save power Fedora will sleep USB devices. We need to turn this off for Deconz and the Zigbee USB stick (ConBee II):

```
sudo rpm-ostree kargs --append=usbcore.autosuspend=-1

# check
cat /sys/module/usbcore/parameters/autosuspend
```

## Containers

### Caddy

I am using Caddy as a local reverse proxy. Along with the Pi-hole it allows custom domains like `homeassistant.lan` for each of the services. Caddy needs access to port 80 and 443 so the firewall needs to be opened:

```
sudo firewall-cmd --zone=FedoraWorkstation --add-service=http
sudo firewall-cmd --zone=FedoraWorkstation --add-service=http --permanent
sudo firewall-cmd --zone=FedoraWorkstation --add-service=https
sudo firewall-cmd --zone=FedoraWorkstation --add-service=https --permanent
```

`firewall-cmd --get-default-zone` will let you know which zone you are currently using.

### Pi-hole

Pi-hole also needs a few tweaks (including a hole in the local firewall):

```
sudo sysctl net.ipv4.ip_unprivileged_port_start=53
sudo nano /etc/sysctl.conf
# add net.ipv4.ip_unprivileged_port_start=53

sudo nano /etc/systemd/resolved.conf
# add DNSStubListener=no

sudo systemctl restart systemd-resolved
sudo systemctl restart NetworkManager

sudo firewall-cmd --zone=FedoraWorkstation --add-port=53/udp
sudo firewall-cmd --zone=FedoraWorkstation --add-port=53/tcp
sudo firewall-cmd --permanent --zone=FedoraWorkstation --add-port=53/udp
sudo firewall-cmd --permanent --zone=FedoraWorkstation --add-port=53/tcp
```

Reference: [Using firewalld](https://docs.fedoraproject.org/en-US/quick-docs/firewalld/), [Running Pi-hole in a Podman container](https://jreypo.io/2021/03/12/running-pihole-as-a-podman-container-in-fedora/)

### Home Assistant

The `nmap` scanner has to run in unprivileged mode. To do this modify the Nmap Tracker options in the Home Assistant UI and add `--unprivileged` to the raw configurable scan options.

## Deconz

The Deconz container needs access to USB which is a little tricking using Podman. You need to create a udev rule that changes the group and owner of the USB device when its plugged in so the container can access it.

```
# set policy for containers to use USB devices in SELinux
setsebool -P container_use_devices on

# get access to /dev/ttyACM0 by being in same group
ls -l /dev/ttyACM0
grep -E '^dialout:' /usr/lib/group | sudo tee -a /etc/group
sudo usermod -a -G dialout username

# change owner of /dev/ttyACM0 to your username
lsusb
sudo nano /etc/udev/rules.d/99-deconz.rules

# add the following to the rule file (based on what you get from lsusb)
SUBSYSTEM=="tty", ATTRS{idVendor}=="1cf1", ATTRS{idProduct}=="0030", OWNER="username", GROUP="dialout"

# apply changes
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Reference: [Access USB from rootless container](https://bugzilla.redhat.com/show_bug.cgi?id=1770553), [udev rule tips](https://gist.github.com/edro15/1c6cd63894836ed982a7d88bef26e4af)
