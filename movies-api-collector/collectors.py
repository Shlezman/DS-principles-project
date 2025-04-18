import requests
import pandas as pd
import time

class MovieCollector:
    def __init__(self, api_key, max_movies=10):
        self.max_movies = max_movies
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3'
        self.movies_df = pd.DataFrame()  # Initialize an empty DataFrame to store movie data
        self.movie_ids = set()
        self.movie_fields = {
    'title': 'title',  # Movie name
    'overview': 'overview',  # Plot summary
    'release_date': 'release_date',  # Date the movie was released
    'runtime': 'runtime',  # Length of the movie in minutes
    'genres': lambda d: ', '.join([g['name'] for g in d.get('genres', [])]),  # Genres (e.g. Action, Drama)
    'production_companies': lambda d: ', '.join([c['name'] for c in d.get('production_companies', [])]),  # Studios that produced the movie
    'popularity': 'popularity',  # Popularity score on TMDB
    'vote_average': 'vote_average',  # Average rating from users
    'vote_count': 'vote_count',  # Number of users who rated
    'budget': 'budget',  # Movie production budget (in USD)
    'revenue': 'revenue',  # Total box office revenue (in USD)
    'poster_path': 'poster_path',  # Path to the movie poster image
    'spoken_languages': lambda d: ', '.join([l['name'] for l in d.get('spoken_languages', [])]),  # Languages spoken in the movie
    'trailer': lambda d: f"https://www.youtube.com/watch?v={d.get('videos', {}).get('results', [{}])[0].get('key')}" if d.get('videos', {}).get('results') else None,  # Link to the trailer on YouTube
    'watch_providers': lambda d: ', '.join(d.get('watch/providers', {}).get('results', {}).keys()),  # Streaming platforms available
    'homepage': 'homepage',  # Official movie website
    'tagline': 'tagline',  # Short marketing slogan or phrase
    'belongs_to_collection': lambda d: d.get('belongs_to_collection', {}).get('name') if d.get('belongs_to_collection') else None,  # Name of the movie series (if part of one)
    'adult': 'adult',  # True if it's adult content (18+)
    'imdb_id': 'imdb_id',  # IMDb ID
    'production_countries': lambda d: ', '.join([c['name'] for c in d.get('production_countries', [])]),  # Countries where the movie was produced
    'original_language': 'original_language',  # Original language of the movie
    'original_title': 'original_title',  # Original title (before translation)
    'status': 'status'  # Production status (e.g. Released, Canceled)
}

        

    # This function gets full movie details from TMDB API using the movie ID
    def get_movie_details(self, movie_id):
        url = f'{self.base_url}/movie/{movie_id}?api_key={self.api_key}&language=en-US&append_to_response=videos,watch/providers'
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.json() #   # the request was successful
        except:
            return None
        return None

    # collects list of movies from multiple TMDB categories
    def collect_movies_from_categories(self):
        categories = ['popular', 'top_rated', 'now_playing', 'upcoming']

        # Keep collecting until reaching the target number of movies
        while self.movies_df.shape[0] < self.max_movies:

            for category in categories:
                # Build the API URL for the current category and page
                url = f'{self.base_url}/movie/{category}?api_key={self.api_key}&language=en-US&page={self.movies_df.shape[0]+1}' 
                try:
                    response = requests.get(url, timeout=10) # GET request to fetch the movie list
                    if response.status_code != 200:
                        continue # If the request failed
                except:
                    continue
                
                movies = response.json().get('results', []) # Extract the list of movies from the API response

                # For each movie in the list, fetch and save full details using its ID
                for movie in movies:
                    self.add_movie_by_id(movie['id'])

                    if self.movies_df.shape[0] >= self.max_movies: # stop processing this page
                        break

                if self.movies_df.shape[0] >= self.max_movies: # stop processing this category
                    break
            time.sleep(0.5)

    #receives a movie ID and collect full details
    def add_movie_by_id(self, movie_id):  

        if movie_id in self.movie_ids: # If the movie was already collected – skip to avoid duplicates
            return

        self.movie_ids.add(movie_id) # Add the ID to the list of already collected movies

        details = self.get_movie_details(movie_id) 
        if not details:
            return
    
    
        movie_data = {} # store data of each movie

        for key, extractor in self.movie_fields.items():
            if callable(extractor):  # If the value is a function (like lambda) – apply it on the details
                movie_data[key] = extractor(details)
            else:  # If it's a string – get the value directly
                movie_data[key] = details.get(extractor)

        self.movies_df = self.movies_df.append(movie_data, ignore_index=True)
        print(f'Collected: {self.movies_df.shape[0]} movies', end='\r') # Show progress of collected movies
        time.sleep(0.5) # Sleep for 0.5 seconds to avoid hitting the API rate limit

    # Full flow (collection)
    def collect_movies(self):
        self.collect_movies_from_categories()
        self.movies_df.to_csv('movies_data.csv', index=False)  # Save the DataFrame to a CSV file
        print('Done!🎉 \nFile name: movies_data.csv')
