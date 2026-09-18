# Utility Stack

Utility services run in CT 102 at:

```text
<UTILITY_IP>
```

## Services

### Caddy

Caddy is the reverse proxy.

Current public routes conceptually look like:

```caddy
jellyfin.example.com {
    reverse_proxy <JELLYFIN_IP>:8096
}

seer.example.com {
    reverse_proxy <ARR_IP>:5055
}
```

Caddy automatically manages HTTPS certificates.

---

### AdGuard Home

Local URL:

```text
http://<UTILITY_IP>:3000
```

Provides DNS/ad-blocking for selected clients.

---

### Uptime Kuma

Local URL:

```text
http://<UTILITY_IP>:3001
```

Used to monitor services such as:

- Jellyfin
- Seerr
- Radarr
- Sonarr
- SABnzbd
- Prowlarr
- Bazarr
- Homepage
- Crafty
- Pterodactyl
- AdGuard

Typical HTTP monitor:

```text
Type: HTTP(s)
Interval: 60 seconds
Retries: 2
Timeout: 10 seconds
Accepted status: 200-299
```

---

### Homepage

Local URL:

```text
http://<UTILITY_IP>:3002
```

Config mount:

```text
/opt/homepage/config → /app/config
```

Homepage is used as the local administrative dashboard.

Suggested entries:

- Proxmox
- Jellyfin
- Seerr
- Radarr
- Sonarr
- SABnzbd
- Prowlarr
- Bazarr
- Pterodactyl
- Crafty
- AdGuard Home
- Uptime Kuma

Use local URLs in Homepage rather than public URLs.

## Docker Boot Fix

Utility Docker initially failed to start after reboot because `networking.service` was timing out on DHCPv6.

After changing the LXC to:

```text
ip6=manual
```

the boot sequence became:

```text
networking.service → active
docker.service → active
homepage → healthy
uptime-kuma → healthy
```

Both Docker containers are configured to restart automatically.
