# Discord Homelab Status Bot

A small Discord bot for on-demand homelab status checks.

## Commands

```text
/status   Check all services
/media    Check media services
/utility  Check utility services
/games    Check game services
```

The bot checks web services over HTTP and game servers over TCP.

## Included Checks

### Media
- Jellyfin
- Seerr
- Radarr
- Sonarr
- SABnzbd
- Prowlarr
- Bazarr

### Utility
- Homepage
- Uptime Kuma
- AdGuard Home

### Games
- Crafty
- Pterodactyl
- Cobbleverse
- Terraria

## Environment

Copy the example:

```bash
cp .env.example .env
```

Then set:

```env
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_server_id_here
```

Never commit `.env`.

## Network Placeholders

Replace these placeholders in `bot.py` with your own LAN addresses:

```text
<JELLYFIN_IP>
<ARR_IP>
<UTILITY_IP>
<MINECRAFT_IP>
<GAMES_IP>
```

## Docker

Build:

```bash
docker build -t homelab-discord-bot .
```

Run:

```bash
docker run -d \
  --name homelab-discord-bot \
  --restart unless-stopped \
  --env-file .env \
  homelab-discord-bot
```

Logs:

```bash
docker logs homelab-discord-bot
```

## Uptime Kuma

Uptime Kuma handles automatic UP/DOWN Discord alerts.

This bot is intentionally separate and provides on-demand status checks with slash commands.
