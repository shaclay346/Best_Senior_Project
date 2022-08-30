# widgets.py
# File of external function to pull from for virtual assistant (fetch the caf menu, fetch the weather, etc.)

from bs4 import BeautifulSoup 
import requests as rq
import datetime, random, os, io, re, pdb


def get_menu():
	'''Returns today's menu at the Caf as a list of strings (to allow for more specific selections in the main app'''
	# Note: Sometimes this straight up won't work because the caf menu is extremely inconsistent with their formatting
	link = 'https://www.flsouthern.edu/campus-offices/dining-services/daily-menu.aspx'
	
	# Get Menu Content
	content = rq.get(link).text
	
	# Soupify
	soup = BeautifulSoup(content, "html.parser")

	# Extract Menu
	menu = soup.find("div", {"style":"text-align: center;"})
	menu = [a for a in menu.stripped_strings]

	# Get and Format Today's Date
	today = datetime.date.today()
	tomorrow = today + datetime.timedelta(days=1)

	today = f"{today.month}/{today.day}/{str(today.year)}"
	tomorrow = f"{tomorrow.month}/{tomorrow.day}/{str(tomorrow.year)}"

	# Caf Menu is Inconsistent, sometimes saying '/2022' and sometimes saying '/22'
	today = [today, today[:-4] + today[-2:]]
	tomorrow = [tomorrow, tomorrow[:-4] + tomorrow[-2:]]

	# Extract Today's Menu
	out = []
	seen = False
	for line in menu:
		if seen:
			if any(b in line for b in tomorrow):
				break

			out.append(line)

		else:
			if any(a in line for a in today):
				seen = True
				out.append(line)

	return out



def coin_flip():
	'''Randomly returns either 'heads' or 'tails'''
	ops = ['heads','tails']
	return random.choice(ops)







def main():
	# print("This file isn't meant to be run as part of the final project.") # uncomment later: leave while testing
	pdb.set_trace()


if __name__ == '__main__':
	main()