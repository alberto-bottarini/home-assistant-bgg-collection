# BGG Collection

BGG Collection is a custom integration for Home Assistant that allows you to monitor your board game collection from BoardGameGeek.

## Features
- Counts the number of board games and expansions in your collection.
- Automatically updates the data.

## Installation
1. Add this repository to HACS:
   - Go to **HACS** → **Integrations** → **Three dots menu** → **Custom repositories**.
   - Add the repository URL and select "Integration" as the category.
2. Install the integration via HACS.
3. Restart Home Assistant.

## Configuration
1. Go to **Settings** → **Devices & Services**.
2. Click **Add Integration** and search for "BGG Collection".
3. Enter your BoardGameGeek username.

## Example Usage
Once the integration is set up, it creates a sensor called "BGG Collection". The sensor's state represents the total number of board games and expansions in your collection. Additionally, it provides two attributes:
- `board_games`: The number of board games.
- `expansions`: The number of expansions.