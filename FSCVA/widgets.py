# widgets.py
# File of widgets called by main (fetch the caf menu, fetch the weather, etc.)
import werkzeug

werkzeug.cached_property = (
    werkzeug.utils.cached_property
)  # Fixes roboBrowser error I (William) was getting
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
from requests_html import HTMLSession
from timer import Timer
import urllib
import multiprocessing
import ssl

# needs to be added to build
# don't want to mess anything up so I'm not adding it command was 'pip install selenium'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# New imports
import wave
import pyaudio

# Constants/Global variables
alarmSound = "alarms/mixkit-retro-game-emergency-alarm-1000.wav"
soundFile = wave.open(alarmSound, "rb")
audio = pyaudio.PyAudio()
timerSound = "alarms/mixkit-scanning-sci-fi-alarm-905.wav"
timer = None
alarm = None
alarmPros = multiprocessing.Process()
ROOT = os.path.dirname(os.path.abspath(__file__))


def get_upcoming_assignments(text, username="USERNAME", password="PASSWORD"):
    """Gets the users upcoming assignments by webscraping Canvas"""
    # Load login credentials from login_credentials.txt
    username, password = load_login_creds("sso")

    # Stop function if credentials are still default values
    if username == "USERNAME" or password == "PASSWORD":
        return "Incomplete login credentials given."

    chrome_options = Options()
    chrome_options.add_argument("--headless")

    # path = "./chromedriver.exe"

    driver = webdriver.Chrome()
    # driver = webdriver.Chrome(executable_path=path, options=chrome_options)

    # https://id.quicklaunch.io/authenticationendpoint/login.do?commonAuthCallerPath=%2Fpassivests&forceAuth=false&passiveAuth=false&tenantDomain=flsouthern.edu&wa=wsignin1.0&wct=2022-10-30T15%3A23%3A20Z&wctx=rm%3D0%26id%3Dpassive%26ru%3D%252fcas%252flogin%253fservice%253dhttps%25253A%25252F%25252Fsso.flsouthern.edu%25252Fadmin%25252Fsecured%25252F414%25252Fapi%25252Fauth%25253Furl%25253Dhttps%25253A%25252F%25252Fsso.flsouthern.edu%25252Fhome%25252F414&wtrealm=https%3A%2F%2Fcas-flsouthern.quicklaunch.io%2F&sessionDataKey=cf5a8855-b88e-4b66-a427-fc216714d8a1&relyingParty=https%3A%2F%2Fcas-flsouthern.quicklaunch.io%2F&type=passivests&sp=flsouthernedu&isSaaSApp=false&authenticators=BasicAuthenticator:LOCAL
    driver.get(
        r"""https://id.quicklaunch.io/authenticationendpoint/login.do?commonAuthCallerPath=%2Fpassivests&forceAuth=false&passiveAuth=false&tenantDomain=flsouthern.edu&wa=wsignin1.0&wct=2022-10-21T13%3A15%3A25Z&wctx=rm%3D0%26id%3Dpassive%26ru%3D%252fcas%252flogin%253fservice%253dhttps%25253A%25252F%25252Fsso.flsouthern.edu%25252Fadmin%25252Fsecured%25252F414%25252Fapi%25252Fauth%25253Furl%25253Dhttps%25253A%25252F%25252Fsso.flsouthern.edu%25252Fhome%25252F414&wtrealm=https%3A%2F%2Fcas-flsouthern.quicklaunch.io%2F&sessionDataKey=0f8b7a5d-4491-4530-9fc1-61c3da9512c3&relyingParty=https%3A%2F%2Fcas-flsouthern.quicklaunch.io%2F&type=passivests&sp=flsouthernedu&isSaaSApp=false&authenticators=BasicAuthenticator:LOCAL"""
    )

    time.sleep(4)

    driver.find_element(By.ID, "branding-username").send_keys(username)
    driver.find_element(By.ID, "branding-password").send_keys(password)

    # id = branding-sumbit-button
    login_button = driver.find_element(By.ID, "branding-sumbit-button")
    login_button.click()

    time.sleep(3)


def get_menu(text):
    """Returns today's menu at the Caf as a list of strings (to allow for more specific selections in the main app"""
    # Note: Sometimes this straight-up won't work because the caf menu is extremely inconsistent with their formatting
    link = "https://www.flsouthern.edu/campus-offices/dining-services/daily-menu.aspx"

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
    dishes = []
    seen = False
    for line in menu:
        if seen:
            if any(a in line for a in tomorrow):
                break

            dishes.append(line)

        else:
            if any(a in line for a in today):
                seen = True
                dishes.append(line)

    # Fail Answwers
    fanswers = [
        "Sorry, I can't find the menu.",
        "They formatted it weird, so I have no idea.",
        "Figure it out.",
    ]
    # Safety Check in case Menu is Formatted Incorrectly
    if not dishes:
        return random.choice(fanswers)

    # Check for Specific Meal Query
    if "breakfast" in text:
        # Bad Menu Check
        if "BREAKFAST" not in dishes or "LUNCH" not in dishes:
            return random.choice(fanswers)

        meal = "breakfast"
        dishes = dishes[dishes.index("BREAKFAST") + 1 : dishes.index("LUNCH")]
    elif "lunch" in text:
        # Bad Menu Check
        if "LUNCH" not in dishes or "DINNER" not in dishes:
            return random.choice(fanswers)

        meal = "lunch"
        dishes = dishes[dishes.index("LUNCH") + 1 : dishes.index("DINNER")]
    elif "dinner" in text:
        # Bad Menu Check
        if "DINNER" not in dishes:
            return random.choice(fanswers)

        meal = "dinner"
        dishes = dishes[dishes.index("LUNCH & DINNER") + 1 :]
    else:
        dishes = dishes[1:]

    # Remove Useless Information from dishes
    rnames = set(
        [
            "Wright at Home",
            "Portabello's",
            "World Tour",
            "BREAKFAST",
            "LUNCH",
            "LUNCH & DINNER",
            "DINNER",
        ]
    )

    dishes = list(set(dishes) - rnames)

    # Output
    response = (
        "Today"
        if not any([a in text for a in ["breakfast", "lunch", "dinner"]])
        else f"For {meal}"
    )
    response += f", the Caf will be serving {', '.join(dishes[:-1])}, and {dishes[-1]}."

    return response


def get_balance(text):
    """Returns the student's Snake Bite Balance."""
    return "Still working on this."


def get_weather(text):
    """Returns the weather at the specified location."""
    openWeatherKey = "b139d88edbb994bbe4c2026a8de2ed12"

    # for now fetch weather in Lakeland, later on maybe allow other cities
    city = "lakeland"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={openWeatherKey}"
    response = rq.get(url)

    # convert the response object to json, so its easy to parse
    json_data = json.loads(response.text)

    # get data from response
    type_ = json_data["weather"][0]["main"]
    description = json_data["weather"][0]["description"]
    temperature = json_data["main"]["temp"]
    feels_like = json_data["main"]["feels_like"]

    # (K − 273.15) × 9/5 + 32
    temperature = math.floor((temperature - 273.15) * 9 // 5 + 32)
    feels_like = math.floor((feels_like - 273.15) * 9 // 5 + 32)

    output = f"The weather is being described as {description} and the temperature is {temperature}ºF"

    # only add feels like temperature if it is different than actual temp
    if feels_like != temperature:
        output = f"The weather is being described as {description} and the temperature is {temperature}ºF, but feels like {feels_like}ºF."

    if type_ == "Rain":
        output += " I recommend you bring an umbrella with you today."

    return output


def flip_coin(text):
    """Randomly returns either 'heads' or 'tails"""
    results = [
        "It's heads.",
        "Flipping...it's heads.",
        "It's tails.",
        "Flipping...it's tails.",
    ]
    return random.choice(results)


def roll_dice(text):
    """Returns the result of rolling a die"""
    sides = ""
    for i in range(len(text)):
        if text[i].isdigit():
            sides += text[i]

    if sides != "":
        sides = int(sides)
    else:
        sides = 6

    # return random number
    return f"Rolling...it's {random.randint(1, sides)}."


def get_time(text):
    """Returns current time."""
    # datetime object containing current date and time
    now = datetime.datetime.now()
    hours = int(now.strftime("%H"))
    flag = False

    if hours > 12:
        hours = hours % 12
        flag = True
    minutes = now.strftime("%M")
    output = str(hours) + ":" + minutes

    if flag:
        output += "PM"
    else:
        output += "AM"

    return f"It's currently {output}."  ### temp ugly formatting for presentation


def get_date(text):
    """Returns current date in 'day month, year' format."""
    date_time = datetime.datetime.now()

    return date_time.strftime("%B %d, %Y")


def get_schedule(text, username="USERNAME", password="PASSWORD"):
    """Returns user's class schedule."""
    # Load login credentials from login_credentials.txt
    username, password = load_login_creds("portal")

    # Stop function if credentials are still default values
    if username == "USERNAME" or password == "PASSWORD":
        return "Incomplete login credentials given."

    # Creates a RoboBrowser Object and Logs into Portal
    br = RoboBrowser()
    br.open("https://portal.flsouthern.edu/ICS/Students/", verify=False)

    form = br.get_form()

    # Login Credentials for Portal Login
    form["userName"] = username
    form["password"] = password

    br.submit_form(form)

    src = str(br.parsed())

    soup = BeautifulSoup(src, "html.parser")

    # Get All Courses
    table = soup.find("table", {"id": "tblCoursesSched"})
    table = table.find_all("tr", {"id": re.compile("[trItems$]")})

    # Split Courses
    courses = []

    for item in table:
        row = item.find_all("td")
        course = [
            re.sub(";", "", a.text).strip()
            for a in row
            if row and "No grade" not in a.text
        ]

        # Append Only if Course Found (fixes small bug)
        if course:
            courses.append(course)

    ### temp ugly formatting for presentation
    days = {0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
    today = days.get(datetime.datetime.now().weekday())

    schedule = []

    # Check if Class is Today
    for course in courses:
        if today in course[-1]:
            schedule.append(better_title(course[1]))

    # No Classes Today
    if not schedule:
        return f"Looks like you don't have anything planned for today."
    # One or More Classes Today
    else:
        return (
            f"You have {', '.join(schedule[:-1])} and {schedule[-1]} today."
            if len(schedule) > 1
            else f"You have {schedule[0]} today."
        )


def better_title(text):
    """Converts text to real title case, unlike title()"""
    lowercase_words = [
        "and",
        "as",
        "if",
        "at",
        "but",
        "by",
        "for",
        "from",
        "only",
        "in",
        "into",
        "like",
        "near",
        "of",
        "off",
        "on",
        "once",
        "onto",
        "or",
        "out",
        "over",
        "so",
        "that",
        "than",
        "to",
        "up",
        "upon",
        "with",
        "when",
    ]
    text = text.split()
    return " ".join(
        [
            a.title()
            if (a not in lowercase_words and len(a) > 3) or a == text[0]
            else a
            for a in text
        ]
    )


def manage_timer(text):
    """Wrapper method for setting/cancelling timers."""
    if "cancel" in text:
        cancel_timer()
    elif "end" in text:
        cancel_timer()
    elif "stop" in text:
        cancel_timer()
    else:
        output = set_timer(text)
        return output


def set_timer(text):
    """sets a timer for a given period of time"""
    seconds = 0
    if "and" in text:
        # handle this seperately
        pass
    else:
        time = ""
        output = ""

        for i in range(len(text)):
            if text[i].isdigit():
                time += text[i]

        if time != "":
            seconds = int(time)

        output += str(seconds)

        if "hour" in text:
            seconds *= 3600
            output += " hours"
        elif "minute" in text:
            seconds *= 60
            output += " minutes"

    # create thread for timer and start it
    global timer
    timer = Timer(seconds, timerSound)

    if "name" in text:
        name_timer(text)

    timer.start()


def cancel_timer():
    """cancels the timer by killing the thread"""
    # call the stop method on timer thread
    if timer != None:
        timer.stop()
        return "timer cancelled"
    else:
        return "No active timers"


def name_timer(text):
    timer.set_name(text)


def get_operands(text):
    # whats 18 times 20

    left_operand = ""
    right_operand = ""

    flag1 = False
    flag2 = False
    # get left operand
    for i in range(len(text)):
        if flag1:
            break
        if text[i].isdigit():
            for j in range(i, len(text)):
                if text[j].isdigit():
                    left_operand += text[j]
                else:
                    flag1 = True
                    break

    # get right operand
    for i in range(len(text) - 1, -1, -1):
        if flag2:
            break

        if text[i].isdigit():
            for j in range(i, -1, -1):
                if text[j].isdigit():
                    right_operand += text[j]
                else:
                    flag2 = True
                    break
    # reverse right operand
    right_operand = right_operand[::-1]

    return [int(left_operand), int(right_operand)]


def calculate(text):
    operands = get_operands(text)
    result = 0
    if "plus" in text:
        result = operands[0] + operands[1]
    elif "minus" in text:
        result = operands[0] - operands[1]
    elif "times" in text:
        result = operands[0] * operands[1]
    elif "divide" in text:
        result = operands[0] // operands[1]

    return result


def manage_alarm(text):
    """Wrapper method for adding/removing alarms."""
    # Grab global variables
    global alarmPros

    # Check text for what we need to do
    if "cancel" in text:
        if alarmPros.is_alive():
            # Cancel the alarm
            alarmPros.terminate()
            alarmPros = multiprocessing.Process()
            return "Alarm Cancelled"
        return "There is no alarm set"
    else:
        if alarmPros.is_alive():
            return "Alarm already set, cancel the current alarm to make a new one"
        # Testing data (Grab actual time from text later)
        altime = datetime.datetime.now()
        if altime.minute == 59:
            altime = altime.replace(hour=altime.hour + 1, minute=00)
        else:
            altime = altime.replace(minute=altime.minute + 1)
        alarm = altime
        alarmPros = multiprocessing.Process(target=set_alarm, args=(alarm,))
        alarmPros.start()
        return "Alarm Set"


def set_alarm(alarm):
    """Set an alarm that, when the given time passes, activates an alarm sound"""
    # Set alarm and play the alarm sound when the time comes
    # print("Setting Alarm, press tab to cancel it")
    check_alarm(alarm)
    play_alarm()


def check_alarm(alarm):
    """Check the current alarms. If the time matches one of the alarms, activate an alarm sound"""
    # Check if the current time matches the first alarm in the alarms array
    while True:
        # Check the date
        if datetime.datetime.now().date() == alarm.date():
            while True:
                # Check the time
                if (
                    datetime.datetime.now().hour == alarm.hour
                    and datetime.datetime.now().minute == alarm.minute
                ):
                    return


def play_alarm():
    """Play an alarm sound, unless flagged to stop or the sound ends"""
    # Grab global variables
    global soundFile
    global audio
    global alarm

    # Play the alarm sound
    stream = audio.open(
        format=audio.get_format_from_width(soundFile.getsampwidth()),
        channels=soundFile.getnchannels(),
        rate=soundFile.getframerate(),
        output=True,
        stream_callback=alarm_callback,
    )
    stream.start_stream()
    while stream.is_active():
        if False:
            return


def alarm_callback(in_data, frame_count, time_info, status):
    """Callback function for playing alarm sound"""
    data = soundFile.readframes(frame_count)
    return (data, pyaudio.paContinue)


def parse_results(response):
    # google uses these css identifiers on all of their results
    css_identifier_result = ".tF2Cxc"

    # CSS identifiers to
    css_identifier_title = "h3"
    css_identifier_link = ".yuRUbf a"
    css_identifier_text = ".VwiC3b"

    # save the results from the google page
    results = response.html.find(css_identifier_result)

    output = "Here are the results:\n"

    for i in range(3):
        try:
            title = results[i].find(css_identifier_title, first=True).text
            text = results[i].find(css_identifier_text, first=True).text
            link = results[i].find(css_identifier_link, first=True).attrs["href"]
        except:
            title = results[i].find(css_identifier_title, first=True).text
            link = results[i].find(css_identifier_link, first=True).attrs["href"]
            text = "Not available"

        output += f"\nTitle: {title}\nText: {text}\nLink: {link}\n"

    return output


def google_search(query):
    """Does a google search on a command, returns title and link to results.
    example command: How old is Ryan Reynolds?
                    How many ounces in a cup
    """

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


def define_word(text):
    """uses the dictionaryapi to get the dictionary definition of a word"""
    # need to parse the word they want defined

    # if they said define _____   extract the second word
    if "define" in text:
        word = text.split(" ", 1)[1].rsplit(" ", 1)[0]
    # otherwise they probably said whats the definition of ____
    else:
        pass

    # https://api.dictionaryapi.dev/api/v2/entries/en/<word>
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = rq.request("GET", url)
    text = json.loads(response.text)

    # get the important data
    data = text[0]["meanings"][0]
    type_of_speach = data["partOfSpeech"]

    # save the top definition
    definition = data["definitions"][0]["definition"]

    output = f"{word}: {type_of_speach}, {definition}"

    return output


def unknown(text):
    """Returns "I don't know" answer"""
    options = [
        "I didn't get that.",
        "What?",
        "Not sure I understand what you're asking.",
        "Figure it out yourself.",
    ]
    return random.choice(options)


def load_login_creds(site):
    """Loads portal and SSO credentials for use in
    get_schedule and get_upcoming_assignments."""
    with open(os.path.join(ROOT, "login_credentials.txt"), "r") as f:
        creds = [a.strip() for a in f.readlines() if not a.startswith("#")]

    if site == "portal":
        return creds[:2]
    elif site == "sso":
        return creds[2:]
    else:
        return ["", "", ""]


def main():
    # print("This file isn't meant to be run as part of the final project.") # uncomment later: leave while testing
    # pdb.set_trace()
    manage_timer("set a timer for 20 minutes")

    time.sleep(4)
    manage_timer("stop the timer...")


if __name__ == "__main__":
    main()
