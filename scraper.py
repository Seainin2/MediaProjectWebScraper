#import pandas as pd
from selenium import webdriver
from chromedriver_py import binary_path
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyodbc
import uuid
import datetime
from code import parse_date

#Movie urls to be scraped
MOVIE_MEATCRITIC_COMING_SOON_URL = 'https://www.metacritic.com/browse/movies/release-date/coming-soon/date?view=detailed'
MOVIE_IMDB_COMING_SOON_URL = 'https://www.imdb.com/movies-coming-soon/'

#Game urls to be scraped
GAME_METACRITIC_COMING_SOON_URL = 'https://www.metacritic.com/feature/major-upcoming-video-game-release-dates-xbox-ps4-pc-switch'
GAME_STEAM_COMING_SOON_URL = 'https://store.steampowered.com/explore/upcoming/'

#Book urls to be scraped
BOOK_FANTASTIC_COMING_SOON_URL = 'https://www.fantasticfiction.com/coming-soon/'
BOOK_AMAZON_COMING_SOON_URL = "https://www.amazon.com/Books-Coming-Soon/s?rh=n%3A283155%2Cp_n_publication_date%3A1250228011"
BOOK_RISINGSHADOW_COMING_SOON_URL = "https://www.risingshadow.net/library/comingbooks"

#Show urls to be scraped
SHOW_METACRITIC_COMING_SOON_URL = 'https://www.metacritic.com/browse/tv/release-date/coming-soon/date'

#Path to chrome driver
PATH_TO_CHROMEDRIVER = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'

#Database connection string
DB_CONNECTION = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:mysqlserverseaininkeenan.database.windows.net,1433;Database=MediaApiDb;Uid=seaininkeenan;Pwd=1Azurepassword;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--headless')

    service_object = Service(binary_path)
    driver = webdriver.Chrome(service=service_object,options=chrome_options)
    return driver


def check_if_class_exists(type, tag, html):
    try:

        if type == 'class':
            isText = html.find_element(By.CLASS_NAME, tag).text.strip()
        if type == 'tag':
            isText = html.find_element(By.TAG_NAME, tag).text.strip()

        if not isText:
            return False
        return True
    except:
        return False

#Show-START****************************************************************************************************************************************************************************        
def handle_shows_metacritic(driver, url, file):
    driver.get(url)
    shows = driver.find_elements(By.TAG_NAME, 'tr')

    shows_data = []

    for show in shows:
        parsedShow = parse_show_metacritic(show)

        if parsedShow is not None:
            if parsedShow['date'] is not None:
                shows_data.append(parsedShow)
    add_shows_to_db(shows_data)

    #shows_df = pd.DataFrame(shows_data)
    #shows_df.to_csv(file)


def add_shows_to_db(shows_data):
    try:
        with pyodbc.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cursor:
                shows = []
                q ="INSERT INTO [dbo].[Shows] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,ImageName) VALUES (?,?,?,?,?,?)"
                for show in shows_data:
                    
                    mediaId = uuid.uuid4()
                    seriesId = uuid.uuid4()
                    creatingPropertyId = uuid.uuid4()

                    shows.append((
                        mediaId,
                        seriesId,
                        creatingPropertyId,
                        'show',
                        show['title'],
                        show['img_url'],
                    ))
                

                cursor.executemany(q,shows)
                conn.commit()
    except Exception as e:
        print(e)

def parse_show_metacritic(show):
    try:
        title_tag = show.find_element(By.CLASS_NAME, 'title')
        title = title_tag.text

        img_url_tag = show.find_element(By.TAG_NAME, 'img')
        img_url = img_url_tag.get_attribute('src')

        score_tag = show.find_element(By.CLASS_NAME, 'metascore_w')
        score = score_tag.text

        multi_tag = show.find_element(By.CLASS_NAME, 'clamp-details')
        multi = multi_tag.text

        description_tag = show.find_element(By.CLASS_NAME, 'summary')
        description = description_tag.text

        return {
            'title': title,
            'img_url': img_url+' ',
            'date': parse_date(multi),
            'score': score,
            'description': description
        }
    except:
        return None
#Shows-END****************************************************************************************************************************************************************************


#Games-START****************************************************************************************************************************************************************************
def handle_games_steam(driver, url, file):
    driver.get(url)
    page = driver.find_element(By.ID, 'tab_popular_comingsoon_content')
    games = page.find_elements(By.TAG_NAME, 'a')

    games_data = []

    for game in games:
        
        parsedGame = parse_game_steam(game)
        if parsedGame is not None:
            if parsedGame['date'] is not None:
                games_data.append(parsedGame)
    add_games_to_db(games_data)

    #games_df = pd.DataFrame(games_data)
    #games_df.to_csv(file)

def add_games_to_db(games_data):
    try:
        with pyodbc.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cursor:
                games = []
                q ="INSERT INTO [dbo].[Games] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,ImageName,Description,NumberofTimesSearched,ReleaseDate) VALUES (?,?,?,?,?,?,?,?,?)"
                for game in games_data:
                    
                    mediaId = uuid.uuid4()
                    seriesId = uuid.uuid4()
                    creatingPropertyId = uuid.uuid4()

                    games.append((
                        mediaId,
                        seriesId,
                        creatingPropertyId,
                        'game',
                        game['title'],
                        game['img_url'],
                        'description',
                        0,
                        game['date']
                    ))
                

                cursor.executemany(q,games)
                conn.commit()
    except Exception as e:
        print(e)

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
            if check_if_class_exists('class', x, game):
                available = x + ', ' + available

        return {
            'title': title,
            'img_url': img_url+' ',
            'date': parse_date(date),
            'tags': themes,
            'available': available,
            'URL': url
        }

    except:
        return None
#Games-END****************************************************************************************************************************************************************************


#Movies-START****************************************************************************************************************************************************************************
def handle_movies_metacritic(driver, url, file):
    movies = []
    driver.get(url)
    movies = driver.find_elements(By.TAG_NAME, 'tr')

    movies_data = []

    for movie in movies:
        parsedMovie = parse_movie_metacritic(movie)

        if parsedMovie is not None:
            if parsedMovie['date'] is not None:
                
                movies_data.append(parsedMovie)

    add_movies_to_db(movies_data)

    #movies_df = pd.DataFrame(movies_data)
    #movies_df.to_csv(file)

def add_movies_to_db(movie_data):
    try:
        with pyodbc.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cursor:
                movies = []
                q ="INSERT INTO [dbo].[Movies] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,ImageName,Description,NumberofTimesSearched,Length,ReleaseDate)VALUES (?,?,?,?,?,?,?,?,?,?)";

                for movie in movie_data:
                    
                    mediaId = uuid.uuid4()
                    seriesId = uuid.uuid4()
                    creatingPropertyId = uuid.uuid4()

                    movies.append((
                        mediaId,
                        seriesId,
                        creatingPropertyId,
                        'movie',
                        movie['title'],
                        movie['img_url'],
                        movie['description'],
                        0,
                        0,
                        movie['date']
                    ))
                

                cursor.executemany(q,movies)
                conn.commit()
    except Exception as e:
        print(e)

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

        return {
            'title': title,
            'img_url': img_url+' ',
            'date': parse_date(date),
            'rating': rating,
            'score': score,
            'description': description
        }
    except:
        return None
#Movies-END****************************************************************************************************************************************************************************


#Books-START****************************************************************************************************************************************************************************
def handle_books_risingshadow(driver, url, file):
    driver.get(url)
    books = driver.find_elements(By.CLASS_NAME, 'library')
    books_data = []

    for book in books:
        parsedBook = parse_book_risingshadow(book)
        if parsedBook is not None:
            if parsedBook['date'] is not None:
                #add_books_to_db(parsedBook)
                books_data.append(parsedBook)

    add_books_to_db(books_data)
    
    #books_df = pd.DataFrame(books_data)
    #books_df.to_csv(file)

def add_books_to_db(book_data):
    try:
        with pyodbc.connect(DB_CONNECTION) as conn:
            with conn.cursor() as cursor:
                books = []
                q ="INSERT INTO [dbo].[Books] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,Description,NumberofTimesSearched,Length,ReleaseDate) VALUES (?,?,?,?,?,?,?,?,?)";

                for book in book_data:
                    
                    mediaId = uuid.uuid4()
                    seriesId = uuid.uuid4()
                    creatingPropertyId = uuid.uuid4()

                    books.append((
                        mediaId,
                        seriesId,
                        creatingPropertyId,
                        'book',
                        book['title'],
                        'Description',
                        0,
                        0,
                        book['date']
                    ))
                

                cursor.executemany(q,books)
                conn.commit()
    except Exception as e:
        print(e)

def parse_book_risingshadow(book):
    tr = book.find_elements(By.TAG_NAME, 'td')
    data = tr[1].text

    link = tr[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
    img_url = tr[0].find_element(By.TAG_NAME, 'img').get_attribute('data-src')

    data = data.split('\n')

    return {
        'title': data[0],
        'img_url': 'https://www.risingshadow.net/' + img_url+' ',
        'author': data[1],
        'date': parse_date(data[3]),
        'genre': data[4],
        'link': link
    }
#Books-END*********************************************************************************************************************************************************************************************



def main_funtion():
    print('Setting up driver')
    driver = get_driver()
    print('Driver set up')

    print('Gettting Games')
    #games on steam
    handle_games_steam(driver, GAME_STEAM_COMING_SOON_URL, 'games_steam.csv')

    print('Gettting Movies')
    #movies on metacritic
    handle_movies_metacritic(driver, MOVIE_MEATCRITIC_COMING_SOON_URL,'movies_metacritic.csv')

    print('Gettting Books')
    #books on risingshadow
    handle_books_risingshadow(driver,BOOK_RISINGSHADOW_COMING_SOON_URL,'books_risingshadow.csv')

    print('Gettting Shows')
    #shows on metacritic
    handle_shows_metacritic(driver,SHOW_METACRITIC_COMING_SOON_URL,'shows_metacritic.csv')

    

    driver.quit()
