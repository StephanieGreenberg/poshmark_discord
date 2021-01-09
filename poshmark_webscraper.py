from bs4 import BeautifulSoup
from urllib.request import urlopen

# Get lululemon postings page on Poshmark
url = "https://poshmark.com/search?query=lululemon%20athletica&sort_by=added_desc"
page = urlopen(url)
html = page.read().decode("utf-8")
poshmark = BeautifulSoup(html, "html.parser")

# Get all cards which contain each item's listing information
cards = poshmark.find_all(class_="card")

itemInfo = []

for card in cards:
	baseURL = 'https://poshmark.com/'
	listingURL = baseURL + card.find(class_='tile__covershot')['href']
	listingImageURL = card.find('img')['src']

	# Strip strings to remove whitespace and new line characters
	listingTitle = card.find(class_="tile__title").string.strip()
	listingPrice = card.find(class_="p--t--1").string.strip()

	''' The string in between the tags is of the format Size: XX so just split that string
	and only take the part with the actual size '''
	listingSize = card.find(class_="tile__details__pipe__size").string.strip().split()[1]

	itemInfo.append({
		'listingURL':listingURL, 
		'listingImageURL':listingImageURL, 
		'listingTitle':listingTitle,
		'listingPrice':listingPrice,
		'listingSize':listingSize
		})

# Print all item info
for item in itemInfo:
	print(f"{item['listingTitle']}\nSize:{item['listingSize']}\nPrice:{item['listingPrice']}\n{item['listingURL']}\n\n")
