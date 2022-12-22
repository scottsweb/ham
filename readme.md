# HAM (Home Automation Machine)

This is version two of HAM ([see version one](https://github.com/scottsweb/ham/tree/master)), the host machine is now running [Fedora Silverblue](https://silverblue.fedoraproject.org/) and uses [Podman](https://podman.io/) instead of Docker. This allows the containers to run rootless and have a slightly more stable system upon which to build my #homelab. have also upgraded from a Raspberry Pi to a small x86 system with a small footprint and power demands.

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

## Containers
