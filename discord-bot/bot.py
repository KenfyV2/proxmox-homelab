import os
import time
import asyncio
import aiohttp
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

SERVICES = {
    "Media": {
        "Jellyfin": "http://<JELLYFIN_IP>:8096",
        "Seerr": "http://<ARR_IP>:5055",
        "Radarr": "http://<ARR_IP>:7878",
        "Sonarr": "http://<ARR_IP>:8989",
        "SABnzbd": "http://<ARR_IP>:8080",
        "Prowlarr": "http://<ARR_IP>:9696",
        "Bazarr": "http://<ARR_IP>:6767",
    },
    "Utility": {
        "Homepage": "http://<UTILITY_IP>:3002",
        "Uptime Kuma": "http://<UTILITY_IP>:3001",
        "AdGuard Home": "http://<UTILITY_IP>:3000",
    },
    "Games": {
        "Crafty": "https://<MINECRAFT_IP>:8443",
        "Pterodactyl": "http://<GAMES_IP>",
    },
}

TCP_SERVICES = {
    "Games": {
        "Cobbleverse": ("<MINECRAFT_IP>", 25565),
        "Terraria": ("<GAMES_IP>", 7777),
    }
}

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


async def check_http_service(session, name, url):
    start = time.perf_counter()
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=5),
            ssl=False
        ) as response:
            latency = round((time.perf_counter() - start) * 1000)
            return {
                "name": name,
                "up": 200 <= response.status < 400,
                "latency": latency,
            }
    except Exception:
        return {
            "name": name,
            "up": False,
            "latency": None,
        }


async def check_tcp_service(name, host, port):
    start = time.perf_counter()
    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=5
        )
        latency = round((time.perf_counter() - start) * 1000)
        writer.close()
        await writer.wait_closed()
        return {
            "name": name,
            "up": True,
            "latency": latency,
        }
    except Exception:
        return {
            "name": name,
            "up": False,
            "latency": None,
        }


def format_result(result):
    if result["up"]:
        return f"🟢 **{result['name']}** — `{result['latency']} ms`"
    return f"🔴 **{result['name']}** — `DOWN`"


async def build_status_embed(category=None):
    async with aiohttp.ClientSession() as session:
        all_results = {}
        categories = [category] if category else SERVICES.keys()

        for group in categories:
            group_results = []

            if group in SERVICES:
                for name, url in SERVICES[group].items():
                    group_results.append(
                        await check_http_service(session, name, url)
                    )

            if group in TCP_SERVICES:
                for name, (host, port) in TCP_SERVICES[group].items():
                    group_results.append(
                        await check_tcp_service(name, host, port)
                    )

            all_results[group] = group_results

    down_services = [
        result["name"]
        for results in all_results.values()
        for result in results
        if not result["up"]
    ]

    if down_services:
        description = (
            "Homelab is online.\n"
            f"**{len(down_services)} service(s) currently unavailable.**"
        )
    else:
        description = "All checked services are operational."

    embed = discord.Embed(
        title="🟢 Homelab Status",
        description=description,
        color=discord.Color.green(),
    )

    for group, results in all_results.items():
        if results:
            embed.add_field(
                name=group,
                value="\n".join(format_result(r) for r in results),
                inline=False,
            )

    embed.set_footer(text="Homelab • Live status check")
    return embed


@bot.event
async def on_ready():
    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Logged in as {bot.user}")


@bot.tree.command(name="status", description="Check all homelab services")
async def status(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=await build_status_embed())


@bot.tree.command(name="media", description="Check media services")
async def media(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=await build_status_embed("Media"))


@bot.tree.command(name="utility", description="Check utility services")
async def utility(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=await build_status_embed("Utility"))


@bot.tree.command(name="games", description="Check game services")
async def games(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(embed=await build_status_embed("Games"))


bot.run(TOKEN)
