# widgets.py
# File of external function to pull from for virtual assistant (fetch the caf menu, fetch the weather, etc.)

from bs4 import BeautifulSoup
import requests as rq
import datetime
import os
import io
import re
import pdb
import json
import math


def get_menu():
    '''Returns today's menu at the Caf as a list of strings (to allow for more specific selections in the main app'''
    # Note: Sometimes this straight up won't work because the caf menu is extremely inconsistent with their formatting
    link = 'https://www.flsouthern.edu/campus-offices/dining-services/daily-menu.aspx'

    # Get Menu Content
    content = rq.get(link).text

    # Soupify
    soup = BeautifulSoup(content, "html.parser")

    # Extract Menu
    menu = soup.find("div", {"style": "text-align: center;"})
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


def getWeather():
    openWeatherKey = 'b139d88edbb994bbe4c2026a8de2ed12'

    # for now fetch weather in Lakeland, later on maybe allow other cities
    city = 'lakeland'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openWeatherKey}'
    response = rq.get(url)

    # convert the response object to json, so its easy to parse
    json_data = json.loads(response.text)

    # get data from response
    type_ = json_data['weather'][0]['main']
    description = json_data['weather'][0]['description']
    temperature = json_data['main']['temp']
    feels_like = json_data['main']['feels_like']

    # (K − 273.15) × 9/5 + 32
    temperature = math.floor((temperature - 273.15) * 9 // 5 + 32)
    feels_like = math.floor((feels_like - 273.15) * 9 // 5 + 32)

    # might want to change response but will do for now
    output = f'the weather is {type_} and the temperature is {temperature}, but feels like {feels_like}.'

    if(type_ == "Rain"):
        output += ' I recommend you bring an umbrella with you today.'

    return output


def main():
    # print("This file isn't meant to be run as part of the final project.") # uncomment later: leave while testing
    pdb.set_trace()


if __name__ == '__main__':
    main()
