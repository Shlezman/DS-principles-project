
import json
import requests
from playwright.sync_api import sync_playwright

# URL and parameters
def get_coordinates(city):
    """
    TODO: use geoapi to get the cordinates of city
    :param city:
    :return:
    """
    pass


def get_cityid(city):
    # TODO: use geoapi to get the id of city
    pass


def context(city:str, tag:str, id:int)-> tuple[str, dict[str, str]]:
    city_cor = get_coordinates(city)
    city_id = get_cityid(city)
    #TODO: get the correct url format
    url = f"https://www.thefork.com/_next/data/DZ0CTrRFsrWqj6w3f7pUa/en-US/search.json?coordinates={city_cor}&restaurantTagId%5B%5D={id}"
    url = f'https://www.thefork.com/_next/data/DZ0CTrRFsrWqj6w3f7pUa/en-US/search/cityTag/{city}/415144/restaurantTag/{tag}/{id}.json'
    params = {
        'citySlug': city,
        'cityId': '415144',
        'restaurantTagSlug': tag,
        'restaurantTagId': '457'
    }
    return url, params


# Method 1: Using the cookies file directly with requests
def use_cookies_file_with_requests(url, params):
    # Load cookies from file
    with open('../cookies/Scraper-cookies.json', 'r') as f:
        cookie_data = json.load(f)

    # Convert Playwright cookies to requests cookies dict
    cookies = {cookie['name']: cookie['value'] for cookie in cookie_data}

    headers = {
        'accept': '*/*',
        'accept-language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7',
        'referer': 'https://www.thefork.com/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36',
        'x-nextjs-data': '1'
    }
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    return response


# Method 2: Using Playwright's saved state
def use_playwright_with_saved_state(url, params):
    with sync_playwright() as p:
        # Launch browser and create context with saved state
        browser = p.chromium.launch(headless=True)

        # Use the saved session state
        context = browser.new_context(storage_state='sessions/Scraper.json')
        page = context.new_page()

        # Navigate to the URL
        full_url = f"{url}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
        response = page.goto(full_url)

        # Get the response body
        content = response.json()

        browser.close()
        return content


# Choose which method to use
# response = use_cookies_file_with_requests()
# Or use Playwright directly
response = use_playwright_with_saved_state()

if isinstance(response, requests.Response):
    if response.status_code == 200:
        data = response.json()
        print("Request successful!")

        # Save to file
        with open('thefork_data3.json', 'w') as f:
            json.dump(data, f, indent=2)

        print("Data saved to thefork_data.json")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
else:
    # Handle the playwright response
    with open('thefork_data.json3', 'w') as f:
        json.dump(response, f, indent=2)
    print("Data saved to thefork_data.json")