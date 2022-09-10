# from googlesearch import search

# query = "how old is Ryan Gosling?"

# for result in search(query, num=3, stop=3):
#     print(result)
import requests
import urllib
import pandas as pd  # pip install pandas
from requests_html import HTML  # pip install requests html
from requests_html import HTMLSession


def get_results(query):

    query = urllib.parse.quote_plus(query)
    response = get_source("https://www.google.co.uk/search?q=" + query)

    return response


def get_source(url):
    """Return the source code for the provided URL. 

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """

    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)


def parse_results(response):

    css_identifier_result = ".tF2Cxc"
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    results = response.html.find(css_identifier_result)

    output = []

    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            'text': result.find(css_identifier_text, first=True)
        }

        output.append(item)

    return output


def google_search(query):
    response = get_results(query)
    return parse_results(response)


results = google_search("How old is Ryan Gosling")

for i in results:
    print(i)
