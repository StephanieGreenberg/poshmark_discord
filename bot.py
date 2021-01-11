# bot.py

import os
import discord
import random
import logging
import poshmark_webscraper as webscraper
from dotenv import load_dotenv
from discord.ext import commands
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

#logging.basicConfig(level=logging.INFO)

#get discord token and discord guild from .env file. note: guild means the same thing as server.
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#channel IDs
LULU_LEMON_CHANNEL = 795488593778311179

#sets correct permissions
intents = discord.Intents.all()

#create a new discord client, which represents a connection to discord
client = commands.Bot(command_prefix = '!', intents=intents)

''' 
Open URL from url parameter and return a BeautifulSoup object 
which is a parsed version of the website's HTML 
'''
def openURL(url):
	page = urlopen(url)
	html = page.read().decode("utf-8")
	poshmark = BeautifulSoup(html, "html.parser")

	# Return parsed version of the Poshmark link
	return poshmark

#the on_ready event is triggered when the client has connected to discord
@client.event
async def on_ready():
	print('Bot is ready.')
	channel = client.get_channel(LULU_LEMON_CHANNEL)
	url = "https://poshmark.com/search?query=lululemon%20athletica&sort_by=added_desc"

	# Dictionary to hold item information
	itemInfo = {}

	''' 
	Continuously refresh the URL specified in the url parameter and 
	look for new listings. Print info about each listing including the listing
	URL, title, price, and size
	'''
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
			await channel.send(f"{listingTitle}\nSize: {listingSize}\nPrice: {listingPrice}\n{listingURL}\n\n")

@client.event
async def on_member_join(member):
	print(f'{member} has joined a server.')
	await member.create_dm()
	await member.dm_channel.send(
		f'Hi {member.name}, welcome to the Poshmark Discord server!')

@client.event
async def on_member_remove(member):
	print(f'{member} has left a server.')

client.run(TOKEN)
