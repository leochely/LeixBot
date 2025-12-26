# LeixBot

## Installation

Create a .env file with the following variables and format:

```
ACCESS_TOKEN=abcd1234
CLIENT_SECRET=xyz789
LLM_API_URL=http://my-llm-url.com:11434
BOT_ID=12345

# Optional
BOT_PREFIX=!
OWNER_ID=1234
```

To generate the client secret, you have to register your application on the [twitch developer console](https://dev.twitch.tv/console). Log in as your **bot account** and register a new application. 
To generate the access token, go to the twitch [token generator](https://twitchtokengenerator.com/), login as your **bot account** and select "bot chat token".

You can run the bot with:

```bash
uv sync
uv run --env-file=.env src/bot.py 
```

To give the bot the right scopes, visit: http://localhost:4343/oauth?scopes=user:read:chat%20user:write:chat%20user:bot+moderator:read:blocked_terms+moderator:read:chat_settings+moderator:read:unban_requests+moderator:manage:banned_users+channel:manage:broadcast+moderator:manage:chat_messages+moderator:manage:warnings+moderator:read:moderators+moderator:read:vips+moderator:read:suspicious_users+moderator:read:followers+moderator:manage:announcements+moderator:read:chatters+moderator:read:shield_mode+moderator:manage:shield_mode+moderator:read:automod_settings+moderator:manage:automod_settings+moderator:manage:blocked_terms+moderator:manage:chat_settings+channel:read:ads&force_verify=true



## Development

A docker-compose with hot-reload is included for convenience. The following command will run the LeixBot service with `watchfiles` and a volume bound for restarting the service upon change detection:

```bash
docker compose up --build
```
