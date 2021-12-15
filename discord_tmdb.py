import discord
from TMDB_class import BaseTMDB, SearchTMDB, DiscoverTMDB
from dotenv import load_dotenv
import os

load_dotenv()


base = BaseTMDB()
discover = DiscoverTMDB()
search = SearchTMDB()

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} connected to Discord')


@client.event
async def on_message(message):
    if message.author == client.user: #prevents bot from a infinite loop
        return
    
    if message.content == '!Genres': #returns all availaible genres to choose from
        responses_genres = discover.movie_genres()
        response_genres = '\n'.join(map(str, responses_genres))
        await message.channel.send(response_genres)
    
    if message.content.startswith('!!Genre'): #returns movies by genre with sort arguement
        discover.movie_genres()
        responses_genre = message.content.split(' ')[1]
 
        try:
            responses_genre_sort = message.content.split(' ')[2]
        except IndexError:
            responses_genre_sort = 'Popular'

        response_genre = discover.discover_movies(responses_genre, responses_genre_sort)
        await message.channel.send(response_genre)
        
    if message.content == '!!!Genre': #returns random genre (always sorts by popular)
        discover.movie_genres()
        responses_random_genre = discover.discover_random_genre()
        genre, result = responses_random_genre[0], responses_random_genre[1]
 
        result_string = '\n'.join(map(str, result))
        await message.channel.send(f'The random genre is {genre}: \n {result_string}')

    if message.content == '!Random': #returns random movies from 500 pages of results
        responses_random = discover.discover_random_movies()
        response_random = '\n'.join(map(str, responses_random))
        await message.channel.send(response_random)
    
    if message.content.startswith('!Search'): #search for movie and select which movie to search similar movies by
        split_message = message.content.split(' ')[1:]
        string_message = map(str, split_message)
        join_message = ' '.join(string_message)
        response_search = search.search_movie(join_message)[0:10]

        for count, re in enumerate(response_search):
            await message.channel.send(f'{count}: {re[0:2]}')
        
        await message.channel.send('Please enter the index of the correct movie:')

        movie_index = await client.wait_for('message')
        response_similar = search.similar_movie_by_search(response_search[int(movie_index.content)][2])
        await message.channel.send(response_similar)


#client.run(TOKEN)

