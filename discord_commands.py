import os
import asyncio
from TMDB_class import BaseTMDB, SearchTMDB, DiscoverTMDB

from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv() #loads API keys stored in a env file
TOKEN = os.getenv('DISCORD_TOKEN')

base = BaseTMDB()
discover = DiscoverTMDB()
search = SearchTMDB()

bot = commands.Bot(command_prefix= '!')


@bot.command(name = 'Random', help='Responds with list of random movies')
async def random_movies(ctx):
    responses = discover.discover_random_movies()
    response = '\n'.join([str(i) for i in responses])

    await ctx.send(response)

@bot.command(name = 'Genres', help='Responds with all available genres')
async def genres_list(ctx):
    responses = discover.movie_genres()
    response = '\n'.join([str(i) for i in responses])

    await ctx.send(response)


@bot.command(name = 'Genre', help='Responds with list of movies with the specified genre and sort method')
async def genre_response(ctx, genre, sort):
    discover.movie_genres()
    responses = discover.discover_movies(genre.title(), sort.title())
    
    if isinstance(responses, list): #if return value of class method is list
        response = '\n'.join([str(i) for i in responses])
    else: #if keyerror is raised in class method return that a correct genre/sort must be specified
        response = responses
    

    await ctx.send(response) 


@bot.command(name = 'Random_Genre', help='Responds with a list of movies from a random genre')
async def random_genre_response(ctx):
    discover.movie_genres()
    responses = discover.discover_random_genre()
    genre, result = responses[0], responses[1]
    response = '\n'.join([str(i) for i in result])

    await ctx.send(f'**The random genre is {genre}**: \n{response}')

@bot.command(name = 'Search', help='Responds with results of the movie searched for, use quotation around movie title to get more accurate results') 
async def search_movie_response(ctx, movie):
    responses = search.search_movie(movie)[0:10]

    for count, movies in enumerate(responses):
        await ctx.send(f'**{count}**: {movies[0]} {movies[1]}')
    
    await ctx.send('**Please enter the index of the correct movie:**')

    def check(m: discord.Message):
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
    
    try:
        movie_index = await bot.wait_for(event = 'message', check = check, timeout = 30.0)
    except asyncio.TimeoutError:
        await ctx.send(f'**Please choose the corrext index for movie within 30 sec**')
    else:
        response_list = search.similar_movie_by_search(responses[int(movie_index.content)][2])
        response = '\n'.join([str(i) for i in response_list])
        await ctx.send(response)


bot.run(TOKEN)


