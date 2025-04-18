# Web Scraping Code Explanation

## General Overview:

[TMDB API (The Movie Database API)](https://developer.themoviedb.org/reference/movie-details) is a public data interface that provides access to rich information about movies, TV shows, actors, and trailers.

The API offers structured and updated information, including summaries, ratings, budgets, revenues, streaming platforms, and more — useful for data analysis projects, apps, and websites.

## What is an API?

An API (Application Programming Interface) is a communication interface that allows different software components to talk to each other in a structured and controlled way.

You can think of it like a restaurant menu: the menu shows what dishes (services) are available, and we place an order with the waiter (the API), who then brings us the dish (the data).

Technically speaking, an API is a collection of URLs and rules that allow us to send requests to a server and receive responses — usually in JSON format.

For example, if we want information about a specific movie, we send a request with the movie’s ID, and the server returns its details.

In our project, we used the TMDB API to fetch up-to-date information about thousands of movies: including movie names, budgets, revenues, languages, ratings, streaming platforms, and more.

Instead of manually entering data, we sent thousands of automated requests to the API and received the data directly into our code — enabling us to build a ready-to-analyze dataset quickly, accurately, and efficiently.

To use an API, you usually need an access key (API Key) — a unique identifier for the user to ensure the service is used in a controlled manner and to prevent overuse.

## Code Breakdown:

### 1. Importing Libraries 📚

- `requests` – for sending requests to the TMDB API
- `pandas` – for storing and processing data in tables (DataFrame)
- `time` – to allow delays (`sleep`) so as not to overload the server

### 2. API Configuration 🔑

- `api_key` – your personal access key to the TMDB API.
- `base_url` – the main URL for TMDB’s API.

### 3. Function to Retrieve Full Movie Details 🎬

- The function receives a `movie_id` and builds a URL using the key.
- A GET request is made to fetch movie details, trailers, and streaming platforms.
- Possible status codes:
  - ✅ 200 – success
  - ❌ 404 – not found
  - ⚠️ 500 – server error
- If the request is successful, the function returns the movie’s JSON data. Otherwise, it returns `None`.

### 4. Initial Variable Setup 🧾

- `max_movies` – how many movies to fetch.
- `movies_list` – the list of movies being collected.
- `movie_ids` – a set of collected IDs to avoid duplicates.
- `page` – the starting page for loading results.
- `movie_fields` – the specific details to collect; some need processing (`lambda`).

### 5. Downloading Data from the API (Main Loop)

#### Function 1: Loop Over Categories and Collect Movies

- Loops over 4 categories:

  - Popular (popular)
  - Top Rated (top_rated)
  - Now Playing (now_playing)
  - Upcoming (upcoming)

- Builds the URL based on page and category, sends request, converts to JSON, and extracts from `results`.
- For each movie, it calls `add_movie_by_id()` which fetches full details.

#### Function 2: Fetch Movie Details by ID and Add to List

- Receives a movie ID, checks if it's already collected, saves it, and sends the request.
- Fields are processed if needed (like genres joined into a string).
- A clean dictionary of movie details is built and added to the main list.

> 📝 Note: `end='\r'` in the print statement means each print replaces the previous one live — a kind of real-time progress display.

### 6. Saving Data to a CSV File 📥

- Converts `movies_list` into a DataFrame.
- Saves to a file called `all_movies.csv` without an index (`index=False`).

## Code example:

### - installing the collector package using pip

```bash
pip install -e ./movies-api-collector
```

### - use it in python

```python
from movies-collector import MovieCollector

if __name__ == "__main__":
  collector = MovieCollector(os.envron["API_KEY"], max_movies=10000)
  collector.collect_movies()
```
