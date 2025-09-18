from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("league-of-legends")

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

@mcp.tool()
async def get_champion_stats(champion: str) -> str:
    """Get stats, skins, and lore for a League of Legends champion by name.

    Args:
        champion: Name of the champion (e.g., Aatrox, Jinx, Yasuo)
    """
    url = f"{DD_API_BASE}champion/{champion}.json"
    data = await make_dd_request(url)

    if not data or "data" not in data or champion not in data["data"]:
        return f"Unable to fetch stats or champion '{champion}' not found. Please check the spelling (first letter should be capitalized)."

    champ_data = data["data"][champion]
    stats = champ_data.get("stats", {})
    info = champ_data.get("info", {})
    title = champ_data.get("title", "")
    tags = champ_data.get("tags", [])
    lore = champ_data.get("lore", "")
    skins = champ_data.get("skins", [])

    # Format skins information
    skins_info = []
    for skin in skins:
        skin_name = skin.get('name', 'Unknown')
        skin_id = skin.get('id', 'N/A')
        if skin_name != champion:  # Don't include the default skin
            skins_info.append(f"  - {skin_name} (ID: {skin_id})")
    
    skins_text = '\n'.join(skins_info) if skins_info else "  - No alternative skins available"

    return f"""
**{champion}** - {title}
**Tags:** {', '.join(tags)}

**Lore:**
{lore}

**Skins:**
{skins_text}

**Base Stats:**
- HP: {stats.get('hp', 'N/A')}
- Attack: {info.get('attack', 'N/A')}/10
- Defense: {info.get('defense', 'N/A')}/10
- Magic: {info.get('magic', 'N/A')}/10
- Difficulty: {info.get('difficulty', 'N/A')}/10
- Attack Damage: {stats.get('attackdamage', 'N/A')}
- Armor: {stats.get('armor', 'N/A')}
- Magic Resist: {stats.get('spellblock', 'N/A')}
- Movement Speed: {stats.get('movespeed', 'N/A')}
- HP Regen (per 5s): {stats.get('hpregen', 'N/A')}
- Mana: {stats.get('mp', 'N/A')}
- Mana Regen (per 5s): {stats.get('mpregen', 'N/A')}
"""


@mcp.tool()
async def get_all_champions() -> str:
    """Get a list of all available League of Legends champions."""
    url = f"{DD_API_BASE}champion.json"
    data = await make_dd_request(url)
    
    if not data or "data" not in data:
        return "Unable to fetch champions list."
    
    champions = list(data["data"].keys())
    champions.sort()
    
    return f"**Available Champions ({len(champions)} total):**\n" + ", ".join(champions)


@mcp.tool()
async def search_champions_by_role(role: str) -> str:
    """Search for champions by their primary role/tag.
    
    Args:
        role: Role to search for (e.g., Assassin, Fighter, Mage, Marksman, Support, Tank)
    """
    url = f"{DD_API_BASE}champion.json"
    data = await make_dd_request(url)
    
    if not data or "data" not in data:
        return "Unable to fetch champions data."
    
    matching_champions = []
    role_lower = role.lower()
    
    for champ_name, champ_data in data["data"].items():
        tags = [tag.lower() for tag in champ_data.get("tags", [])]
        if role_lower in tags:
            matching_champions.append(champ_name)
    
    matching_champions.sort()
    
    if not matching_champions:
        return f"No champions found with role '{role}'. Available roles: Assassin, Fighter, Mage, Marksman, Support, Tank"
    
    return f"**Champions with role '{role}' ({len(matching_champions)} found):**\n" + ", ".join(matching_champions)



if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')