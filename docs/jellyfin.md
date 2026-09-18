# Jellyfin

Jellyfin runs in CT 101 at:

```text
<JELLYFIN_IP>
```

Local URL:

```text
http://<JELLYFIN_IP>:8096
```

Remote URL:

```text
https://jellyfin.kenfy.dev
```

## Libraries

Movies:

```text
/media/data/media/movies
```

Shows:

```text
/media/data/media/tv
```

The Proxmox media disk is bind-mounted into the Jellyfin LXC.

## Hardware Transcoding

The Intel UHD 630 iGPU is passed into the Jellyfin container.

Device:

```text
/dev/dri/renderD128
```

Jellyfin has access to Intel Quick Sync / VAAPI capabilities.

Verified codecs include support for common H.264, HEVC, VP8, and VP9 decode paths.

Current strategy:

- Intel Quick Sync enabled
- hardware encoding enabled
- H.264 / HEVC / VP9 hardware decoding enabled where supported
- AV1 left disabled on this generation of Intel GPU
- low-power encoding features left off unless explicitly verified

## Reverse Proxy

Remote traffic follows:

```text
Internet
  ↓
Router TCP 443
  ↓
Caddy on Utility CT <UTILITY_IP>
  ↓
Jellyfin <JELLYFIN_IP>:8096
```

Caddy terminates HTTPS. Jellyfin itself stays on local HTTP.

## Users

Use separate Jellyfin accounts for remote users.

Normal users should not have:

- server administration
- media deletion
- remote control of other users
- unnecessary download permissions

## Library Updates

Because ARR writes media through NFS and Jellyfin sees the same host storage through a bind mount, real-time file monitoring may not always notice every change instantly.

If imported media does not appear:

```text
Jellyfin → Dashboard → Libraries → Scan All Libraries
```
