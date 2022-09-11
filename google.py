import requests
import urllib
import pandas as pd  # pip install pandas
from requests_html import HTML  # pip install requests_html
from requests_html import HTMLSession


def parse_results(response):
    # google uses these css identifiers on all of their results
    css_identifier_result = ".tF2Cxc"

    # CSS identifiers to
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    # save the results from the google page
    results = response.html.find(css_identifier_result)

    output = []

    for result in results:

        item = {
            'title': result.find(css_identifier_title, first=True).text,
            'link': result.find(css_identifier_link, first=True).attrs['href'],
            # 'yXK7lf', 'MUxGbd', 'yDYNvb', 'lyLwlc', 'lEBKkf
            'text': result.find(css_identifier_text, first=True).text
        }

        output.append(item)

    for i in range(len(output)):
        print("Title: {}".format(output[i]["title"]))
        print("Link: {}".format(output[i]["link"]))
        print("Text: {}\n".format(output[i]["text"]))

    return output


def google_search(query):
    '''Does a google search on a command, returns title and link to results.
    example command: How old is Ryan Reynolds?
                    How many ounces in a cup
    '''

    # parse the query
    query = urllib.parse.quote_plus(query)
    url = "https://www.google.co.uk/search?q=" + query

    response = ""

    # get the source code for the page
    try:
        session = HTMLSession()
        response = session.get(url)

    except requests.exceptions.RequestException as e:
        print(e)

    # parse the data we want from the page
    return parse_results(response)


results = google_search("How many ounces in a cup")

# for i in range(len(results)):
#     print("Title: {}".format(results[i]["title"]))
#     print("Link: {}".format(results[i]["link"]))
#     print("Text: {}\n".format(results[i]["text"]))
