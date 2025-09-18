from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("league-of-legend")

# Constants
DD_API_BASE = "https://ddragon.leagueoflegends.com/cdn/15.18.1/data/en_US/"
USER_AGENT = "lol-app/1.0"



async def make_dd_request(url: str) -> dict[str, Any] | None:
    """Make a request to the Data Dragon API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    # ...existing code...

@mcp.tool()
async def get_champion_stats(champion: str) -> str:
    """Get stats for a League of Legends champion by name (first letter capitalized).

    Args:
        champion: Name of the champion (e.g. Aatrox)
    """
    url = f"{DD_API_BASE}champion/{champion}.json"
    data = await make_dd_request(url)

    if not data or "data" not in data or champion not in data["data"]:
        return "Unable to fetch stats or champion not found."

    champ_data = data["data"][champion]
    stats = champ_data.get("stats", {})
    info = champ_data.get("info", {})
    title = champ_data.get("title", "")
    tags = champ_data.get("tags", [])

    return f"""
Name: {champion}
Title: {title}
Tags: {', '.join(tags)}

Stats:
- HP: {stats.get('hp', 'N/A')}
- Attack: {info.get('attack', 'N/A')}
- Defense: {info.get('defense', 'N/A')}
- Magic: {info.get('magic', 'N/A')}
- Difficulty: {info.get('difficulty', 'N/A')}
- Attack Damage: {stats.get('attackdamage', 'N/A')}
- Armor: {stats.get('armor', 'N/A')}
- Spell Block: {stats.get('spellblock', 'N/A')}
- Movespeed: {stats.get('movespeed', 'N/A')}
- HP Regen: {stats.get('hpregen', 'N/A')}
- Mana: {stats.get('mp', 'N/A')}
- Mana Regen: {stats.get('mpregen', 'N/A')}
"""



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')