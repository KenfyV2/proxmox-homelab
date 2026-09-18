# Architecture

## Design Goals

The home lab is split into small workloads instead of putting everything into one VM.

This provides:

- failure isolation
- easier maintenance
- simpler backups
- cleaner networking
- easier hardware passthrough
- independent resource limits
- less chance that one update breaks unrelated services

## Proxmox Layout

```text
Proxmox VE - <PROXMOX_IP>
│
├── CT 100 - minecraft - <MINECRAFT_IP>
│   └── Crafty Controller
│       └── Cobbleverse Minecraft server
│
├── CT 101 - jellyfin - <JELLYFIN_IP>
│   └── Jellyfin
│       └── Intel Quick Sync hardware transcoding
│
├── VM 200 - games - <GAMES_IP>
│   ├── Pterodactyl Panel
│   ├── Wings
│   └── Terraria + other game servers
│
├── CT 102 - utility - <UTILITY_IP>
│   ├── Caddy
│   ├── AdGuard Home
│   ├── Homepage
│   └── Uptime Kuma
│
└── VM 201 - arr - <ARR_IP>
    ├── Gluetun
    ├── SABnzbd
    ├── Prowlarr
    ├── Radarr
    ├── Sonarr
    ├── Bazarr
    └── Seerr
```

## Why Jellyfin Is Separate From ARR

Jellyfin is intentionally kept outside the ARR VM.

Reasons:

1. **Hardware acceleration is simpler.**  
   Intel UHD 630 is passed directly into the Jellyfin LXC.

2. **Media playback stays up during ARR maintenance.**  
   Restarting Docker, Gluetun, SABnzbd, or Sonarr does not take Jellyfin offline.

3. **VPN isolation stays simple.**  
   Only services that need the VPN are placed behind Gluetun.

4. **Failure isolation.**  
   If the ARR VM has a Docker, NFS, or VPN problem, already-downloaded media can still be watched.

5. **Resource control.**  
   Jellyfin transcoding and ARR unpacking/scanning can be managed independently.
