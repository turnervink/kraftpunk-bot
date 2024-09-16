# Kraft Punk Bot
Kraft Punk Bot is a bot for Discord built with Discord.py. Kraft Punk will 
respond to keyword triggers said by users of a Discord server with related images
from The Eric Andre Show.

## Adding Kraft Punk Bot to Your Server
I make no guarantees about service quality or uptime, since this is a self-hosted project.

Invite the bot with this link:  
https://discord.com/oauth2/authorize?client_id=397901256602943489

## Development
Kraft Punk Bot uses Python with Poetry for dependency management, and Postgres as a database.

- Clone the project
- Install dependenices with `poetry install`
- Set the following environment variables with your development values:
```
BOT_TOKEN=<discord bot token>

# Database information for local development
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DATABASE=postgres
POSTGRES_USERNAME=<dev postgres username>
POSTGRES_PASSWORD=<dev postgres password>
```
- Create a `pgdata` directory in the project root
- Start a local database with `docker compose -f docker-compose.local.yml up -d`
- Start the bot with `poetry run python src/bot.py`
- When you're done stop the local database with `docker compose -f docker-compose.local.yml down`

## Deployment
- Create a `.env` file with your production values:
```
# The token for your Discord bot
BOT_TOKEN=<discord bot token>

# Database information
POSTGRES_USERNAME=<dev postgres username>
POSTGRES_PASSWORD=<dev postgres password>
```
- Build the production image with `docker compose build`
- Use `docker compose up` to start the bot's container stack on your production machine

## Contributing
If you for some reason want to contribute to this silly thing feel free to fork it and open a PR!