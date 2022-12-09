from google_play_scraper import app
from urllib.request import urlretrieve
from urllib.error import HTTPError

#actu
result = app(
    'com.poly.france_actu',
    lang='fr', # defaults to 'en'
    country='fr' # defaults to 'us'
)

index = 0
for url in result["screenshots"] :
    try:
        urlretrieve(url, '../ac'+str(index)+'.png')
    except FileNotFoundError as err:
        print(err)   # something wrong with local path
    except HTTPError as err:
        print(err)  # something wrong with url
    index = index + 1

#astro
result = app(
    'com.poly.astrology',
    lang='fr', # defaults to 'en'
    country='fr' # defaults to 'us'
)

index = 0
for url in result["screenshots"] :
    try:
        urlretrieve(url, '../as'+str(index)+'.png')
    except FileNotFoundError as err:
        print(err)   # something wrong with local path
    except HTTPError as err:
        print(err)  # something wrong with url
    index = index + 1