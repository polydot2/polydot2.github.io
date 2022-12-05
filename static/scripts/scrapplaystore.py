from google_play_scraper import app

result = app(
    'com.poly.france_actu',
    lang='fr', # defaults to 'en'
    country='fr' # defaults to 'us'
)

print(result)