import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pyodbc
import uuid
import datetime

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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
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
    table = driver.find_elements(By.TAG_NAME, 'tr')

    print(f'Found {len(table)}')
    shows = []
  
    for row in table:
        if check_if_class_exists('class', 'summary', row):
            shows.append(row)
    print(f'Found {len(shows)}')

    shows_data = []

    for show in shows:
        parsedShow = parse_show_metacritic(show)

        add_show_to_db(parsedShow)
        shows_data.append(parsedShow)

    shows_df = pd.DataFrame(shows_data)
    shows_df.to_csv(file)

def add_show_to_db(show):
    MediaId = uuid.uuid1()
    SeriesId = uuid.uuid1()
    CreatingPropertyId = uuid.uuid1()
    ReleaseDate = datetime.datetime(2009,5,5)
    
    with pyodbc.connect(DB_CONNECTION) as conn:
        with conn.cursor() as cursor:
                
            count = cursor.execute("""INSERT INTO [dbo].[Shows] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,ImageName)
             VALUES (?,?,?,?,?,?)""",MediaId,SeriesId,CreatingPropertyId,'show',show['title'],show['img_url']).rowcount
            conn.commit()

def parse_show_metacritic(show):

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
        'img_url': img_url,
        'date': multi,
        'score': score,
        'description': description
    }
#Shows-END****************************************************************************************************************************************************************************


#Games-START****************************************************************************************************************************************************************************
def handle_games_steam(driver, url, file):
    driver.get(url)
    page = driver.find_element(By.ID, 'tab_popular_comingsoon_content')
    games = page.find_elements(By.TAG_NAME, 'a')

    games_data = []

    for game in games:
        
        parsedGame = parse_game_steam(game)
        if not parsedGame['title'] == '':
            add_game_to_db(parsedGame)
            games_data.append(parsedGame)

    games_df = pd.DataFrame(games_data)
    games_df.to_csv(file)

def add_game_to_db(game):
    MediaId = uuid.uuid1()
    SeriesId = uuid.uuid1()
    CreatingPropertyId = uuid.uuid1()
    ReleaseDate = datetime.datetime(2009,5,5)
    
    with pyodbc.connect(DB_CONNECTION) as conn:
        with conn.cursor() as cursor:
                
            count = cursor.execute("""INSERT INTO [dbo].[Games] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,ImageName,Description,NumberofTimesSearched,ReleaseDate)
             VALUES (?,?,?,?,?,?,?,?,?)""",MediaId,SeriesId,CreatingPropertyId,'game',game['title'],game['img_url'],'this is a description',1,ReleaseDate).rowcount
            conn.commit()

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
#Games-END****************************************************************************************************************************************************************************


#Movies-START****************************************************************************************************************************************************************************
def handle_movies_metacritic(driver, url, file):
    movies = []
    driver.get(url)
    table = driver.find_elements(By.TAG_NAME, 'tr')
    for row in table:
        if check_if_class_exists('class', 'summary', row):
            movies.append(row)

    movies_data = []

    for movie in movies:
        parsedMovie = parse_movie_metacritic(movie)

        add_movie_to_db(parsedMovie)
        movies_data.append(parsedMovie)

    movies_df = pd.DataFrame(movies_data)
    movies_df.to_csv(file)

def add_movie_to_db(movie):
    MediaId = uuid.uuid1()
    SeriesId = uuid.uuid1()
    CreatingPropertyId = uuid.uuid1()
    ReleaseDate = datetime.datetime(2009,5,5)
    
    with pyodbc.connect(DB_CONNECTION) as conn:
        with conn.cursor() as cursor:
                
            count = cursor.execute("""INSERT INTO [dbo].[Movies] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,ImageName,Description,NumberofTimesSearched,Length,ReleaseDate)
             VALUES (?,?,?,?,?,?,?,?,?,?)""",MediaId,SeriesId,CreatingPropertyId,'movie',movie['title'],movie['img_url'],'this is a description',1,100,ReleaseDate).rowcount
            conn.commit()

def parse_movie_metacritic(movie):

    title_tag = movie.find_element(By.CLASS_NAME, 'title')
    title = title_tag.text

    img_url_tag = movie.find_element(By.TAG_NAME, 'img')
    img_url = img_url_tag.get_attribute('src')

    score_tag = movie.find_element(By.CLASS_NAME, 'metascore_w')
    score = score_tag.text

    try:
        multi_tag = movie.find_element(By.CLASS_NAME, 'clamp-details')
        multi = multi_tag.text
        m = multi.split('|')
        date = m[0]
        rating = m[1]
    except:
        print('date and rating where not found')
        date = ''
        rating = ''

    description_tag = movie.find_element(By.CLASS_NAME, 'summary')
    description = description_tag.text

    return {
        'title': title,
        'img_url': img_url,
        'date': date,
        'rating': rating,
        'score': score,
        'description': description
    }
#Movies-END****************************************************************************************************************************************************************************


#Books-START****************************************************************************************************************************************************************************
def handle_books_risingshadow(driver, url, file):
    driver.get(url)
    books = driver.find_elements(By.CLASS_NAME, 'library')
    books_data = []

    for book in books:
        parsedBook = parse_book_risingshadow(book)

        add_book_to_db(parsedBook)
        books_data.append(parsedBook)

    
    books_df = pd.DataFrame(books_data)
    books_df.to_csv(file)

def add_book_to_db(book):
    MediaId = uuid.uuid1()
    SeriesId = uuid.uuid1()
    CreatingPropertyId = uuid.uuid1()
    ReleaseDate = datetime.datetime(2009,5,5)
    
    with pyodbc.connect(DB_CONNECTION) as conn:
        with conn.cursor() as cursor:
                
            count = cursor.execute("""INSERT INTO [dbo].[Books] (MediaId,SeriesId,CreatingPropertyId,MediaType,Title,Description,NumberofTimesSearched,Length,ReleaseDate)
             VALUES (?,?,?,?,?,?,?,?,?)""",MediaId,SeriesId,CreatingPropertyId,'book',book['title'],'this is a description',1,100,ReleaseDate).rowcount
            conn.commit()

def parse_book_risingshadow(book):
    tr = book.find_elements(By.TAG_NAME, 'td')
    data = tr[1].text

    link = tr[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
    img_url = tr[0].find_element(By.TAG_NAME, 'img').get_attribute('data-src')

    data = data.split('\n')

    return {
        'title': data[0],
        'img_url': 'https://www.risingshadow.net/' + img_url,
        'author': data[1],
        'date': data[3],
        'genre': data[4],
        'link': link
    }
#Books-END*********************************************************************************************************************************************************************************************



if __name__ == "__main__":
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
