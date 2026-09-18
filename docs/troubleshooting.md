# Troubleshooting

## Jellyfin Does Not Start After LXC Reboot

Symptoms:

```text
jellyfin.service → inactive
networking.service → activating
dhclient -6 repeatedly retries
```

Check:

```bash
systemctl status networking --no-pager
systemctl list-jobs
cat /etc/network/interfaces
```

If the interface contains:

```text
iface eth0 inet6 dhcp
```

and Proxmox has:

```text
ip6=dhcp
```

change the Proxmox LXC interface to:

```text
ip6=manual
```

Preserve:

- MAC address
- firewall setting
- IPv4 DHCP setting

---

## Utility Docker Does Not Start After Reboot

Check:

```bash
systemctl status networking --no-pager
systemctl status docker --no-pager
```

If networking failed due to DHCPv6, apply the same `ip6=manual` fix.

---

## Movie Exists on Disk but Not Jellyfin

Check from Jellyfin LXC:

```bash
find "/media/data/media/movies" -maxdepth 2 -type f
```

If the file exists, run:

```text
Jellyfin → Dashboard → Libraries → Scan All Libraries
```

---

## Sonarr Finds Releases But Downloads Nothing

Use Interactive Search.

Hover/click the red rejection icon.

Common reasons:

- custom format score below profile minimum
- unwanted quality
- language mismatch
- size limit
- release blocklisted
- wrong episode mapping

For anime, release names often do not reliably advertise every audio language. Avoid overly strict regex-based custom format minimums.

---

## SAB 403 From Radarr/Sonarr

When SAB is behind Gluetun, Radarr/Sonarr connect through:

```text
gluetun:8080
```

SAB's host whitelist must allow the stable hostname:

```text
gluetun
```

Do not rely on a changing Docker container ID.

---

## Subtitle Not Appearing in Jellyfin

Check:

1. Bazarr has the title.
2. A language profile is assigned.
3. A provider is enabled.
4. Subtitle actually downloaded.
5. Jellyfin integration is connected.
6. Run Jellyfin library/metadata refresh if needed.
