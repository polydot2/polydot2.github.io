import requests
from bs4 import BeautifulSoup

def get(url):
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

# main
result = get('https://crucknuk.itch.io/free-hugs-kraken')
print(result["screenshots"])