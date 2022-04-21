import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#Movie urls to be scraped
MOVIE_MEATCRITIC_COMING_SOON_URL = 'https://www.metacritic.com/browse/movies/release-date/coming-soon/date?view=detailed'
MOVIE_IMDB_COMING_SOON_URL = 'https://www.imdb.com/movies-coming-soon/'

#Game urls to be scraped
GAME_METACRITIC_COMING_SOON_URL = 'https://www.metacritic.com/feature/major-upcoming-video-game-release-dates-xbox-ps4-pc-switch'
GAME_STEAM_COMING_SOON_URL = 'https://store.steampowered.com/explore/upcoming/'

#Book urls to be scraped
BOOK_WATERSTONE_COMING_SOON_URL = 'https://www.waterstones.com/campaign/coming-soon'

#Show urls to be scraped
SHOW_METACRITIC_COMING_SOON_URL = 'https://www.metacritic.com/browse/tv/release-date/coming-soon/date'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    return driver
  

def check_if_class_exists(tag, html):
    try:
        html.find_element(By.CLASS_NAME, tag)
        return True
    except:
        return False


def parse_movie_metacritic(movie):
    try:
        title_tag = movie.find_element(By.CLASS_NAME, 'title')
        title = title_tag.text

        img_url_tag = movie.find_element(By.TAG_NAME, 'img')
        img_url = img_url_tag.get_attribute('src')

        score_tag = movie.find_element(By.CLASS_NAME, 'metascore_w')
        score = score_tag.text

        multi_tag = movie.find_element(By.CLASS_NAME, 'clamp-details')
        multi = multi_tag.text
        m = multi.split('|')
        date = m[0]
        rating = m[1]

        description_tag = movie.find_element(By.CLASS_NAME, 'summary')
        description = description_tag.text

        print('Title:', title)
        print('Image URL:', img_url)
        print('Date:', date)
        print('Rating:', rating)
        print('Score:', score)
        print('Description:', description)

        return {
            'title': title,
            'img_url': img_url,
            'date': date,
            'rating': rating,
            'score': score,
            'description': description
        }
    except:
        return {
            'title': '',
            'img_url': '',
            'date': '',
            'rating': '',
            'score': '',
            'description': ''
        }


def parse_game_steam(game):
    try:
        title_tag = game.find_element(By.CLASS_NAME, 'tab_item_name')
        title = title_tag.text

        img_url_tag = game.find_element(By.TAG_NAME, 'img')
        img_url = img_url_tag.get_attribute('src')

        date_tag = game.find_element(By.CLASS_NAME, 'release_date')
        date = date_tag.text

        themes_tag = game.find_element(By.CLASS_NAME, 'tab_item_top_tags')
        themes = themes_tag.text

        url = game.get_attribute('href')

        ava = ['win', 'mac', 'linux']
        available = ''

        for x in ava:
            if check_if_class_exists(x, game):
                available = x + ', ' + available

        return {
            'title': title,
            'img_url': img_url,
            'date': date,
            'tags': themes,
            'available': available,
            'URL': url
        }

    except:
        return {
            'title': '',
            'img_url': '',
            'date': '',
            'tags': '',
            'available': '',
            'URL': ''
        }


def handle_games_steam(driver,url,file):
    driver.get(url)
    page = driver.find_element(By.ID, 'tab_popular_comingsoon_content')
    games = page.find_elements(By.TAG_NAME, 'a')
    games_data = [parse_game_steam(game)for game in games]
    games_df = pd.DataFrame(games_data)
    games_df.to_csv(file)
    return True

if __name__ == "__main__":

    driver = get_driver()

    #games on steam  
    handle_games_steam(driver,GAME_STEAM_COMING_SOON_URL,'games_steam.csv')
  
    #movies on metacritic
    driver.get(MOVIE_MEATCRITIC_COMING_SOON_URL)
    movies = driver.find_elements(By.TAG_NAME, 'tr')
    movies_data = [parse_movie_metacritic(movie)for movie in movies]
    movies_df = pd.DataFrame(movies_data)
    movies_df.to_csv('movie_metacritic.csv')

  

    driver.quit()
