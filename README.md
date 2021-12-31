# LeixBot

## Installation

Create a .env file with the following variables and format:

```
ACCESS_TOKEN=abcd1234
CHANNEL_ACCESS_TOKEN=abcd12345
CLIENT_SECRET=xyz789
BOT_PREFIX=!
CHANNEL=mychannel
INITIAL_CHANNELS=mychannel, anotherchannel1, anotherchannel2, ...
```

To generate the access token, go to the twitch [token generator](https://twitchtokengenerator.com/), login as your **bot account** and select "bot chat token".
To generate the channel access token, go to the [token generator](https://twitchtokengenerator.com/), login as your **own account** and choose "custom scope token". Select all the permissions and generate the token.
To generate the client secret, you have to register your application on the [twitch developer console](https://dev.twitch.tv/console). Log in as your **bot account** and register a new application. 

I recommend making a virtual environment using python 3.9.x or above:

```
pipenv --python 3.9
pipenv install -r requirements.txt
```

## Usage

```
(pipenv run) python bot.py
```

A Procfile is included for heroku deployment.

Use ctrl-C to stop the bot.
