# widgets.py
# File of external function to pull from for virtual assistant (fetch the caf menu, fetch the weather, etc.)
from robobrowser import RoboBrowser
import threading  # Built-in method
from playsound import playsound  # New pip install
import random
import time
import math
import json
import pdb
import re
import io
import os
import datetime
import requests as rq
from bs4 import BeautifulSoup
from googlesearch import search
import werkzeug
from timer import Timer
import urllib
import pandas as pd  # pip install pandas


# Global variables
alarmSound = 'alarms/mixkit-retro-game-emergency-alarm-1000.wav'
timerSound = 'alarms/mixkit-scanning-sci-fi-alarm-905.wav'
timer = None


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


def get_weather():
    '''Returns the weather at the specified location.'''
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


def coin_flip():
    '''Randomly returns either 'heads' or 'tails'''
    ops = ['heads', 'tails']
    return random.choice(ops)


def dice_roll():
    '''Returns the result of rolling a die'''
    return random.randint(1, 6)


def get_time():
    '''Returns current time.'''
    # datetime object containing current date and time
    now = datetime.datetime.now()
    output = now.strftime("%H:%M")

    return output


def get_date():
    '''Returns current date in 'day month, year' format.'''
    date_time = datetime.datetime.now()

    output = date_time.strftime("%B %d, %Y")
    return output


def get_schedule(username='USERNAME', password='PASSWORD'):
    '''Returns user's class schedule.'''

    # Check to stop function if credentials are still default values
    if username == 'USERNAME' or password == 'PASSWORD':
        return ['Incomplete login credentials given.']

    # Creates a RoboBrowser Object and Logs into Portal
    br = RoboBrowser()
    br.open("https://portal.flsouthern.edu/ICS/Students/")

    form = br.get_form()

    # Login Credentials for Portal Login
    form['userName'] = username
    form['password'] = password

    br.submit_form(form)

    src = str(br.parsed())

    soup = BeautifulSoup(src, 'html.parser')

    # Get All Courses
    table = soup.find('table', {'id': 'tblCoursesSched'})
    table = table.find_all('tr', {'id': re.compile('[trItems$]')})

    # Split Courses
    courses = []

    for item in table:
        row = item.find_all('td')
        course = [re.sub(';', '', a.text).strip() for a in row if row and 'No grade' not in a.text]

        # Append Only if Course Found (fixes small bug)
        if course: courses.append(course)

    return courses


def set_timer(text):
    '''sets a timer for a given period of time'''
    seconds = 0
    if("and" in text):
        # handle this seperately
        pass
    else:
        time = ""

        for i in range(len(text)):
            if(text[i].isdigit()):
                time += text[i]

        seconds = int(time)
        if("hour" in text):
            seconds *= 3600
        elif("minute" in text):
            seconds *= 60

    # create thread for timer and start it
    global timer
    timer = Timer(seconds, timerSound)
    timer.start()


def cancel_timer():
    '''cancels the timer by killing the thread'''
    # call the stop method on timer thread
    print("timer is", timer)
    if(timer != None):
        timer.stop()
    else:
        print("No active timers")


def calculate():
    pass


def set_alarm(altime, message):
    '''Set an alarm that, when the given time passes, activates an alarm sound'''
    # Test variable (Delete Later)
    # Change to wanted time (year, month, day, hour(24 base), minute, second)
    altime = datetime.datetime(2022, 9, 1, 22, 24)
    message = "Hello There, I'm working"

    # Add the alarm with the time (dateTime object) and message (string)
    alarm = [altime, message]

    # Wait for the alarm to go off (Testing Only)
    # Add "daemon = True" to make the thread end when the main program ends
    t1 = threading.Thread(target=check_alarm, args=(alarm, ))
    t1.start()


def check_alarm(alarm):
    '''Check the current alarms. If the time matches one of the alarms, activate an alarm sound'''
    # Check if the current time matches the first alarm in the alarms array
    while True:
        time.sleep(1)
        print("waiting for {0}, now {1}".format(
            alarm[0].date(), datetime.datetime.now().date()))
        if datetime.datetime.now().date() == alarm[0].date():  # Check the date
            while True:
                time.sleep(1)
                print("waiting for {0}, now {1}".format(
                    alarm[0].minute, datetime.datetime.now().minute))
                # Check the time
                if datetime.datetime.now().hour == alarm[0].hour and datetime.datetime.now().minute == alarm[0].minute:
                    print(alarm[1])
                    playsound(alarmSound)
                    break
            break


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

    except rq.exceptions.RequestException as e:
        print(e)

    # parse the data we want from the page
    return parse_results(response)


def main():
    # print("This file isn't meant to be run as part of the final project.") # uncomment later: leave while testing
    pdb.set_trace()
    # set_timer("set a timer for 5 seconds")


if __name__ == '__main__':
    main()
