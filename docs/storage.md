# Storage

## Physical Storage

### NVMe

Approximately 512 GB.

Used for:

- Proxmox
- VM disks
- LXC disks

### Media HDD

Approximately 2 TB.

Mounted on Proxmox at:

```text
/mnt/pve/media
```

Media data:

```text
/mnt/pve/media/data
```

### Backup HDD

Approximately 2 TB.

Mounted at:

```text
/mnt/pve/backups
```

Used for Proxmox backup jobs.

## ARR Storage Path

The Proxmox host exports:

```text
/mnt/pve/media/data
```

to the ARR VM using NFS.

Inside VM 201:

```text
/data
```

Important paths:

```text
/data/media/movies
/data/media/tv
/data/usenet/incomplete
/data/usenet/complete/movies
/data/usenet/complete/tv
```

## Jellyfin Storage Path

The same physical media storage is bind-mounted into CT 101:

```text
/media
```

Jellyfin therefore sees:

```text
/media/data/media/movies
/media/data/media/tv
```

This means ARR and Jellyfin access the same underlying files through different mount paths.

## Why This Works

ARR writes:

```text
/data/media/movies/Movie Name/
```

On the host this corresponds to:

```text
/mnt/pve/media/data/media/movies/Movie Name/
```

Jellyfin then sees the same host directory as:

```text
/media/data/media/movies/Movie Name/
```

No second copy of the media is required.
