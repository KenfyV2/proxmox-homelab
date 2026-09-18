# Operations

## Starting / Stopping Workloads

From the Proxmox host:

```bash
pct start 101
pct stop 101
pct enter 101
```

For VMs:

```bash
qm start 201
qm stop 201
```

## Reboot Verification

After rebooting a workload, verify:

### Jellyfin

```bash
systemctl status networking --no-pager
systemctl status jellyfin --no-pager
ss -lntp | grep 8096
```

### Utility

```bash
systemctl status networking --no-pager
systemctl status docker --no-pager
docker ps
```

### ARR

Verify the NFS mount:

```bash
mount | grep /data
```

Then:

```bash
cd /opt/arrstack
sudo docker compose ps
```

All expected containers should be running/healthy.

## Media Troubleshooting Flow

If a requested movie/show is missing:

1. Check Seerr request status.
2. Check Radarr/Sonarr Activity → Queue.
3. Check SABnzbd queue/history.
4. Confirm Radarr/Sonarr imported the file.
5. Confirm file exists under `/data/media/...`.
6. Confirm Jellyfin sees it under `/media/data/media/...`.
7. Run Jellyfin library scan if necessary.

## Failed Usenet Release

If SAB says:

```text
Aborted, cannot be completed
```

the Usenet release likely has missing articles.

Expected behavior:

1. SAB reports failure.
2. Radarr/Sonarr blocklists that specific release.
3. Another acceptable release may be searched/grabbed.

## Backups

Proxmox backups go to the dedicated backup HDD.

Current goal:

- snapshot mode
- ZSTD compression
- retention around 7 backups

Important workloads to include:

- CT 100 Minecraft
- CT 101 Jellyfin
- CT 102 Utility
- VM 200 Games
- VM 201 ARR

Application-level backups, such as Crafty backups, are useful in addition to Proxmox backups.
