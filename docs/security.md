# Security Notes

## Never Commit Secrets

Do not commit:

- Jellyfin API keys
- SABnzbd API keys
- Sonarr/Radarr/Prowlarr API keys
- OpenSubtitles credentials
- Newshosting credentials
- PrivadoVPN credentials
- session cookies
- passwords
- SSH private keys

Use placeholders in documentation:

```text
<API_KEY>
<USERNAME>
<PASSWORD>
```

## Public vs Local Services

Public:

```text
jellyfin.kenfy.dev
seer.kenfy.dev
play.kenfy.dev:25565
play.kenfy.dev:7777
```

Local-only:

- Proxmox
- Crafty
- Pterodactyl panel
- Radarr
- Sonarr
- SABnzbd
- Prowlarr
- Bazarr
- AdGuard
- Homepage
- Uptime Kuma

## Router

Do not forward management ports directly.

Use only the required public ports:

- 80 / 443 → Caddy
- game ports → game server hosts

## Jellyfin Users

Use separate accounts for remote users.

Normal users should not receive administrator or deletion permissions.

## API Key Rotation

If an API key is accidentally exposed:

1. regenerate it
2. update all dependent services
3. test connections
4. remove/revoke the old key
