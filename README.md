# Kraft Punk Bot
Kraft Punk Bot is a bot for Discord built with Discord.py. Kraft Punk will 
respond to keyword triggers said by users of a Discord server with related images
from The Eric Andre Show.

## Adding Kraft Punk Bot to Your Server
I make no guarantees about service quality or uptime, since this is a self-hosted project.

Invite the bot with this link:  
https://discord.com/oauth2/authorize?client_id=397901256602943489

## Development
Kraft Punk Bot uses Python with Poetry for dependency management, and Google Firebase as a database.

- Clone the project
- Install dependenices with `poetry install`
- Obtain your [Firebase service account credentials](https://firebase.google.com/docs/admin/setup#initialize-sdk). Name the file `db-creds.json` and place it in the `config` directory of the project.
- Set the following environment variables with your development values:
```
BOT_TOKEN=<a Discord app bot token>
GOOGLE_APPLICATION_CREDENTIALS=config/db-creds.json
```
- Start the bot with `poetry run python src/bot.py`

## Deployment
- Create a `.env` file with the same variables as above set to your production values
- Build and tag the image: `docker build -t kraftpunk-bot:latest .`
- Run the image, passing in your `.env` file and mounting the directory with the Firebase credentials file to the path you specified in `GOOGLE_APPLICATION_CREDENTIALS`:  
`docker run --env-file .env -v /path/to/creds/dir:${GOOGLE_APPLICATION_CREDENTIALS} kraftpunk-bot:latest` 

## Contributing
If you for some reason want to contribute to this silly thing feel free to fork it and open a PR!