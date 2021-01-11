from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

''' Open URL from url parameter and return a BeautifulSoup object 
which is a parsed version of the website's HTML '''
def openURL(url):
	page = urlopen(url)
	html = page.read().decode("utf-8")
	poshmark = BeautifulSoup(html, "html.parser")

	# Return parsed version of the Poshmark link
	return poshmark

def getNewListings(url):
	# Dictionary to hold item information
	itemInfo = {}

	while True:
		poshmark = openURL(url)

		# Get all cards which contain each item's listing information
		cards = poshmark.find_all(class_="card")

		for card in cards:
			''' Since the website leads to the listing's page when you click the product image, 
			you can get the listing's relative URL by getting the href attribute of the 
			element with class tile__covershot '''
			listingRelativeURL = card.find(class_="tile__covershot")["href"]

			if listingRelativeURL in itemInfo:
				break

			baseURL = "https://poshmark.com/"
			listingURL = baseURL +listingRelativeURL

			''' Get the src attribute of the img element for the current listing '''
			listingImageURL = card.find('img')['src']

			''' Get the title and price of the listing, which are contained in the elements with 
			tile__title and p--t--1 classes respsectively. Strip strings to remove whitespace 
			and new line characters '''
			listingTitle = card.find(class_="tile__title").string.strip()
			listingPrice = card.find(class_="p--t--1").string.strip()

			''' Get the size of the listing, which is contained in the element with class 
			tile__details__pipe__size. The string in between the tags is of the format Size: XX 
			so just split that string and only take the part with the actual size '''
			listingSize = card.find(class_="tile__details__pipe__size").string.strip().split()[1]


			''' Add a new entry to the itemInfo dictionary which uses the listing's relative URL as a key
			and contains a dictionary with the item's information as its value.'''
			itemInfo[listingRelativeURL] = {
				'listingURL':listingURL, 
				'listingImageURL':listingImageURL, 
				'listingTitle':listingTitle,
				'listingPrice':listingPrice,
				'listingSize':listingSize
				}

			# Print item info
			print(f"{listingTitle}\nSize:{listingSize}\nPrice:{listingPrice}\nImage URL:{listingImageURL}\n{listingURL}\n\n")

def main():
	# Get lululemon postings page on Poshmark
	url = "https://poshmark.com/search?query=lululemon%20athletica&sort_by=added_desc"
	getNewListings(url)

main()
