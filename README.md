# League of Legends MCP Server

Un serveur MCP (Model Context Protocol) pour obtenir des informations sur les champions de League of Legends.

## Fonctionnalités

- **get_champion_stats**: Obtient les statistiques, skins et lore d'un champion spécifique
- **get_all_champions**: Liste tous les champions disponibles
- **search_champions_by_role**: Recherche des champions par rôle (Assassin, Fighter, Mage, Marksman, Support, Tank)

## Installation

1. Installez les dépendances avec uv :

```bash
uv sync
```

2. Le serveur utilise l'API Data Dragon de Riot Games pour récupérer les informations des champions.

## Configuration MCP

Ajoutez cette configuration à votre fichier `mcp.json` :

```json
{
  "servers": {
    "league-of-legends": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "league_of_legends.py"],
      "cwd": "/chemin/vers/league_of_legends_mcp"
    }
  }
}
```

## Utilisation

Une fois configuré, vous pouvez demander des informations sur les champions League of Legends :

- "Quelles sont les stats de Jinx ?"
- "Liste tous les champions"
- "Quels champions sont des mages ?"

## API utilisée

Ce MCP utilise l'API Data Dragon de Riot Games version 15.18.1.
