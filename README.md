# TMDB Discord bot

A simple discord bot that incorporates some features of the The Movie Database (TMDB) API. This bot was made using discord.py. 
The functionality of the bot is restricted to the movies listed in TMDB, it does not incorporate TV shows listed in TMDB. <br />

TMDB API: https://developers.themoviedb.org/3 <br />
Discord API: https://discord.com/developers/docs/ <br />
Discord Python API: https://discordpy.readthedocs.io/ <br />

## Installation

Clone the repository

``` git clone https://github.com/oalsaab/TMDB-discord-bot ```

Install the python dependencies

``` pip install -r requirements.txt ```

Create a .env file with the following variables and add your TMDB & Discord API keys

TMDB_KEY => TMDB API key <br />
DISCORD_TOKEN => Discord token key

## Features

The following commands are available:

* Random
* Genres
* Genre
* Random_Genre
* Search
* Help

You must prefix the commands with a '!' to use them. <br />
Use the Help command to receive details of what the command performs.

