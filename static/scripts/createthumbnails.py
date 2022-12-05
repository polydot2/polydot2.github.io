import os, sys
from PIL import Image, ImageDraw, ImageFont
from google_play_scraper import app
import requests
from io import BytesIO

import requests
from bs4 import BeautifulSoup

def getFromItchio(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')

	title = soup.find("h1", class_="game_title").text
	description = soup.find("div", class_="formatted_description").text
	screenshots = soup.find_all(".screenshot_list.a")

	link_url = []
	data = soup.findAll('div',class_='screenshot_list')
	for div in data:
	    links = div.findAll('a')
	    for a in links:
	        link_url.append(a['href'])

	return { 'title': title, 'description': description, 'screenshots': link_url}

def merge(im1, im2, im3):
    w = im1.size[0] + im2.size[0] + im3.size[0]
    h = max(im1.size[1], im2.size[1], im3.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))
    im.paste(im3, (im1.size[0] + im2.size[0], 0))

    return im

def merge2(im1, im2, im3):
    im = Image.new("RGBA", (768, 512))

    im1.thumbnail((768,512))
    im2.thumbnail((768,512))
    im3.thumbnail((768,512))

    im.paste(im1)
    im.paste(im2, (256, 0))
    im.paste(im3, (512, 0))

    return im

def pasteIcon(icon, im):
	icon = icon.resize((128 , 128))
	im.paste(icon, (0, 0))

	return im

def text(img, message):
	font = ImageFont.truetype("Montserrat-Bold.ttf", 64)
	d = ImageDraw.Draw(img)

	d.multiline_text((img.size[0]/2, img.size[1]/2), message, font=font, anchor="ms", fill="white")

	return img

def miniature(package, lang, message, output = ''):

	if(output == ''):
		package.replace('.', '').lower() + '_' + lang + '.png'

	result = app(
	    package,
	    lang=lang, # defaults to 'en'
	)

	icon = Image.open(BytesIO(requests.get(result["icon"]).content))
	screen1 = Image.open(BytesIO(requests.get(result["screenshots"][0]).content))
	screen2 = Image.open(BytesIO(requests.get(result["screenshots"][1]).content))
	screen3 = Image.open(BytesIO(requests.get(result["screenshots"][2]).content))

	# merge screens
	full = merge(screen1, screen2, screen3)
	#full = full.crop((0, 0, 1980, 1080))
	#full = full.resize((256, 256))

	# paste dim
	dim = Image.new("RGBA", (full.size[0], full.size[1]))
	alpha = 0.7
	full = Image.blend(full, dim, alpha)

	# paste icon
	full = pasteIcon(icon, full)

	# paste text
	full = text(full, message)

	full = full.convert('RGB')
	full.save('../' + output, "PNG")

def miniatureFromIch(url, message, output = ''):

	if(output == ''):
		message.replace('\n', '_').replace('!', '').lower() + '.png'

	result = getFromItchio(url)

	#icon = Image.open(BytesIO(requests.get(result["icon"]).content))
	screen1 = Image.open(BytesIO(requests.get(result["screenshots"][0]).content))
	screen2 = Image.open(BytesIO(requests.get(result["screenshots"][1]).content))
	screen3 = Image.open(BytesIO(requests.get(result["screenshots"][2]).content))

	# merge screens
	full = merge2(screen1, screen2, screen3)

	# paste dim
	dim = Image.new("RGBA", (full.size[0], full.size[1]))
	alpha = 0.7
	full = Image.blend(full, dim, alpha)

	# paste text
	full = text(full, message)

	full = full.convert('RGB')
	full.save('../' + output, "PNG")

def placeholder():
	full = Image.new("RGBA", (768, 512))

	# paste text
	full = text(full, "placeholder")

	full = full.convert('RGB')
	full.save('../placeholder.png', "PNG")

## main
placeholder()

miniature('com.poly.france_actu', 'en', 'Actu France\npocket news', 'actufrance.png')
miniature('com.poly.astrology', 'en', 'Astro\ndaily news', 'astro.png')

miniature('com.clanmo.europcar', 'fr', 'Europcar', 'europcar.png')
miniature('fr.proximity.proximity', 'fr', 'MyProximity', 'myproximity.png')
miniature('com.dupuis.webtoonfactory', 'fr', 'Webtoon\nFactory', 'webtoonfactory.png')
miniature('com.francelive.france', 'fr', 'FranceLive', 'francelive.png')

miniature('com.beemenergy.mybeem', 'fr', 'Beem Energy', 'beemenergy.png')
miniature('com.backelite.vingtminutes', 'fr', '20minutes', 'vingtminutes.png')

miniature('be.rtl.info', 'fr', 'RTL info', 'rtlinfo.png')
miniature('be.appsolution.lesoir', 'fr', 'Le Soir', 'lesoir.png')
miniature('fr.k_decole.mobile', 'fr', 'Skolengo', 'skolengo.png')

miniatureFromIch('https://crucknuk.itch.io/yo-runner', "Yo!\nBox&Boxes", 'yorunner.png')
miniatureFromIch('https://crucknuk.itch.io/blobi', "Blobitronica", 'blobitronica.png')
miniatureFromIch('https://crucknuk.itch.io/deepteam', "DeepTeam", 'deepteam.png')

print("DONE")
