# Networking

## LAN

| Host | Address |
|---|---|
| Proxmox | `<PROXMOX_IP>` |
| Minecraft | `<MINECRAFT_IP>` |
| Games | `<GAMES_IP>` |
| Jellyfin | `<JELLYFIN_IP>` |
| Utility | `<UTILITY_IP>` |
| ARR | `<ARR_IP>` |
| Router | `<ROUTER_IP>` |

## Public DNS

Cloudflare DNS is used.

Public records are DNS-only for direct home-hosted services.

Examples:

```text
jellyfin.kenfy.dev
seer.kenfy.dev
play.kenfy.dev
```

## Router Port Forwards

```text
TCP 80  → <UTILITY_IP>:80
TCP 443 → <UTILITY_IP>:443

TCP 25565 → <MINECRAFT_IP>:25565
TCP 7777  → <GAMES_IP>:7777
```

Do not expose Proxmox port 8006 publicly.

## IPv6 DHCP Boot Issue

Both the Jellyfin and Utility LXCs experienced a boot delay/failure because Proxmox generated:

```text
iface eth0 inet6 dhcp
```

The home router advertised IPv6 but did not provide a DHCPv6 address. `dhclient -6` kept waiting and blocked `networking.service`.

The fix was to keep IPv4 DHCP while changing Proxmox networking from:

```text
ip6=dhcp
```

to:

```text
ip6=manual
```

Example final LXC network definition:

```text
net0: name=eth0,bridge=vmbr0,firewall=1,hwaddr=<MAC>,ip=dhcp,ip6=manual,type=veth
```

Important: preserve the existing MAC address when modifying the interface. The router's DHCP lease depends on it for stable addresses.

## DNS

AdGuard Home runs at:

```text
<UTILITY_IP>:3000
```

The Windows desktop is configured to use the AdGuard host for DNS. It is not currently enforced for the entire household.
