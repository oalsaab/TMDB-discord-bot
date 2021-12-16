import requests
import random
from dotenv import load_dotenv
import os


load_dotenv()


class BaseTMDB:
    
    def __init__(self):
        """Initialize class with API token and TMDB API base url"""
        
        self.base_url = 'https://api.themoviedb.org/3'
        self.key = os.getenv('TMDB_KEY')
    
class SearchTMDB(BaseTMDB):

    def __init__(self):
        super().__init__()
    
    def search_movie(self, query):
        """Method utilizing TMDB search feature. Returns a list."""

        self.query = query
        search = requests.get(f'{self.base_url}/search/movie', params={'api_key': self.key, 'query': self.query})
        exact = search.json()['results']
        
        for i in exact:
            for keys in list(i): #list dictionary to make a copy to iterate over it
                if 'release_date' not in i:
                    i['release_date'] = 'no release date'
        
        list_ids = [[i['title'], i['release_date'], i['id']] for i in exact]
            

        return list_ids
        
    def similar_movie_by_search(self, id):
        """Method to find similar movies to the one searched for. Returns a list"""

        similar = requests.get(f'{self.base_url}/movie/{str(id)}/similar', params={'api_key': self.key})
        match = similar.json()['results']

        self.similar_match = [i['title'] for i in match]

        return self.similar_match
        
class DiscoverTMDB(BaseTMDB):

    def __init__(self):
        super().__init__()

    def movie_genres(self):
        """Method to get all of the availaible genres in TMDB and their associated ID. Returns list of genre names."""

        genres = requests.get(f'{self.base_url}/genre/movie/list', params={'api_key': self.key})
        genres_data = genres.json()['genres']

        names_list = [i['name'] for i in genres_data]
        id_list = [i['id'] for i in genres_data]
        
        self.genre_dicts = dict(zip(names_list, id_list))

        return names_list
    
    def discover_movies(self, disc, sort_by_input):
        """Method to discover movies by genre with option to sort results. Returns a list."""

        self.disc = disc
        self.sort_by_input = sort_by_input

        self.sort_by = {
            'Popular': 'popularity.desc',
            'New': 'release_date.desc',
            'Rating': 'vote_average.desc'
        }

        try:
            full_params = {
                'api_key': self.key,
                'with_genres': self.genre_dicts[self.disc],
                'sort_by': self.sort_by[self.sort_by_input]
            }
        
        except KeyError:
            return 'Please choose a correct genre and/or sort method'

        discover = requests.get(f'{self.base_url}/discover/movie', params=full_params)
        discover_json = discover.json()['results']

        self.discover_results = [i['title'] for i in discover_json]

        return self.discover_results

    def discover_random_genre(self):
        """Method of choosing a random genre from list of genres and find movies associated with that genre"""
        
        genre, responses = random.choice(list(self.genre_dicts.items()))

        discover_random = requests.get(f'{self.base_url}/discover/movie', params={'api_key': self.key, 'with_genres': responses})
        discover_random_json = discover_random.json()['results']
        
        discover_random_result = [i['title'] for i in discover_random_json]
        
        return [genre, discover_random_result]
    
    def discover_random_movies(self):
        """Method of choosing a random page out of 500 pages of movie results and return list of movies in that page."""

        discover_random_mov = requests.get(f'{self.base_url}/discover/movie', params={'api_key': self.key, 'page': random.randint(1, 500)})
        discover_random_mov_json = discover_random_mov.json()['results']

        self.result_random_page = [i['title'] for i in discover_random_mov_json]

        return self.result_random_page









