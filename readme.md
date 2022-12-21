# HAM (Home Automation Machine)

This is version two of HAM ([see version one](https://github.com/scottsweb/ham/tree/master)), the host machine is now running [Fedora Silverblue](https://silverblue.fedoraproject.org/) and uses [Podman](https://podman.io/) instead of Docker. This allows me to run these containers rootless and have a slightly more stable system upon which to build my #homelab.

I am mostly just publishing the relevant `docker-compose` / `podman-compose` files now that are grouped into pods around certain pieces of functionality like home automation or media.

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

Start the Podman restart service (restarts containers set to `restart: always`) after a reboot:

```
systemctl --user enable podman-restart.service
systemctl --user start podman-restart.service
```

### Allow long running tasks

As Silverblue is a desktop OS, it tries to shutdown long running tasks (including Podman containers). This can be turned off by running: `loginctl enable-linger`, check the status with `ls /var/lib/systemd/linger`, then reboot.

... more to come
