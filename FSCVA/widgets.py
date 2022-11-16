# widgets.py
# File of widgets called by main (fetch the caf menu, fetch the weather, etc.)
import pyaudio
import wave
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import ssl
import multiprocessing
import urllib
from timer import Timer
from requests_html import HTMLSession
from googlesearch import search
from bs4 import BeautifulSoup
import requests as rq
import datetime
import os
import io
import re
import pdb
import json
import math
import time
import random
from playsound import playsound  # New pip install
import threading  # Built-in method
from robobrowser import RoboBrowser
import werkzeug

werkzeug.cached_property = (
    werkzeug.utils.cached_property
)  # Fixes roboBrowser error I (William) was getting

# Constants/Global variables
timer = None
alarm = None
alarmPros = multiprocessing.Process()
ROOT = os.path.dirname(os.path.abspath(__file__))
alarmSound = os.path.join(ROOT, "alarms/retro.wav")
timerSound = os.path.join(ROOT, "alarms/sci-fi.wav")
soundFile = wave.open(alarmSound, "rb")
audio = pyaudio.PyAudio()


def get_assignments(text, username="USERNAME", password="PASSWORD"):
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
        dishes = dishes[dishes.index("BREAKFAST") + 1: dishes.index("LUNCH")]
    elif "lunch" in text:
        # Bad Menu Check
        if "LUNCH" not in dishes or "DINNER" not in dishes:
            return random.choice(fanswers)

        meal = "lunch"
        dishes = dishes[dishes.index("LUNCH") + 1: dishes.index("DINNER")]
    elif "dinner" in text:
        # Bad Menu Check
        if "DINNER" not in dishes:
            return random.choice(fanswers)

        meal = "dinner"

        if "LUNCH & DINNER" in dishes:
            dishes = dishes[dishes.index("LUNCH & DINNER") + 1:]
        else:
            dishes = dishes[dishes.index("DINNER") + 1:]
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

    return f"It's currently {output}PM." if flag else f"It's currently {output}AM."


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

    # Get Today
    days = {0: "Mon", 1: "Tue", 2: "Wed",
            3: "Thu", 4: "Fri", 5: "Sat", 6: "Sun"}
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
    lowercase_words = ["and", "as", "if", "at", "but", "by", "for", "from", "only", "in", "into", "like", "near", "of", "off",
                       "on", "once", "onto", "or", "out", "over", "so", "that", "than", "to", "up", "upon", "with", "when"]
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
        try:
            output = set_timer(text)
            return output
        except:
            return "Please try setting your timer again."


def get_times(text):
    """gets the hours and minutes for timer if the user said something like
    'set a timer for 2 hours and 15 minutes'"""
    hours = ""
    minutes = ""
    seconds = 0
    index = 0
    output = ""

    if("half" in text):
        tempTime = ""

        for i in range(len(text)):
            if text[i].isdigit():
                tempTime += text[i]
                break

        if("hour" in text):
            hours += tempTime
            # minutes = 30

            seconds = int(hours) * 3600
            seconds += 30 * 60

            output = f"{hours} hours and {minutes} minutes"
            return [seconds, output]
        else:
            minutes += tempTime
            seconds = 30

            seconds += int(minutes) * 60

            output = f"{minutes} minutes and {30} seconds"
            return [seconds, output]

    # they said something like 5 minutes and 15 seconds
    if("seconds" in text):
        for i in range(len(text)):
            if text[i].isdigit():
                minutes += text[i]
                index = i
                break

        index = text.find("and", 0)
        temp = ""
        for j in range(index, len(text)):
            if text[j].isdigit():
                temp += text[j]

        seconds += int(temp)
        seconds += int(minutes) * 60

        output = f"{minutes} minutes and {temp} seconds"

        return [seconds, output]

    # hours and minutes
    else:
        for i in range(len(text)):
            if text[i].isdigit():
                hours += text[i]
                index = i
                break

        index = text.find("and", 0)
        for j in range(index, len(text)):
            if text[j].isdigit():
                minutes += text[j]

        seconds = int(hours) * 3600
        seconds += int(minutes) * 60

        output = f"{hours} hours and {minutes} minutes"
        return [seconds, output]


def set_timer(text):
    """sets a timer for a given period of time"""
    # all time will be converted to seconds
    seconds = 0
    output = "timer set for "

    # if the user says set a timer for 2 and a half hours
    if "and" in text:
        data = get_times(text)
        seconds = data[0]
        output += data[1]
    else:
        time = ""

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
        else:
            output += " seconds"

    # create thread for timer and start it
    global timer
    print("seconds", seconds)
    timer = Timer(seconds, timerSound)
    timer.start()

    return output


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
    if "+" in text:
        result = operands[0] + operands[1]
    elif "-" in text:
        result = operands[0] - operands[1]
    elif "*" in text:
        result = operands[0] * operands[1]
    elif "/" in text:
        result = operands[0] // operands[1]

    return str(result)


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
        alarm = getAlarmTime(text)
        alarmPros = multiprocessing.Process(target=set_alarm, args=(alarm,))
        alarmPros.start()
        return "Alarm Set"


def getAlarmTime(text):
    '''Extract the wanted time from the given text'''

    # Search through the given text for a time, returning None if there is no time specified
    timeStartIndex = -1
    for i in range(len(text)):
        if text[i].isnumeric():
            timeStartIndex = i
            break
    if timeStartIndex == -1:
        return None

    # Using the starting index of the wanted time, determine the format of it (single number, time format, etc.)
    timeString = text[timeStartIndex]
    currIndex = timeStartIndex + 1
    timeFormat = "numeric"  # Single number (ex. 6)
    while currIndex < len(text):
        if text[currIndex].isnumeric():
            timeString += text[currIndex]
            currIndex += 1
            continue
        # Time format (ex. 12:30)
        if text[currIndex] == ":" and timeFormat != "time":
            timeString += text[currIndex]
            timeFormat = "time"
            currIndex += 1
            continue
        break

    # Check if the given time is in an acceptable time form
    if timeFormat == "numeric":
        if int(timeString) < 0 or int(timeString) > 24:
            return "Thats not a time"
    else:
        checkString = timeString.split(":")
        if int(checkString[0]) < 0 or int(checkString[0]) > 23 or int(checkString[1]) < 0 or int(checkString[1]) > 59:
            return "Thats not a time"

    # Check if the text specifies am or pm for the time for 24 hour conversion, and if need be ask for one
    currentFix = None
    currentFix = checkFix(text)
    if currentFix == None and timeFormat != "time" and int(timeString) < 13:
        fixStr = input("a.m. or p.m.?: ")
        currentFix = checkFix(fixStr)

    # Convert the given time to a datetime time object
    timeStringList = ["00", "00", "00"]
    if timeFormat == "numeric":
        timeString = adjustForFix(currentFix, timeString)
        timeStringList[0] = timeString
    else:
        splitTimeString = timeString.split(":")
        splitTimeString[0] = adjustForFix(currentFix, splitTimeString[0])
        timeStringList[0] = splitTimeString[0]
        timeStringList[1] = splitTimeString[1]
    if len(timeStringList[0]) == 1:
        timeStringList[0] = "0" + timeStringList[0]
    return datetime.time.fromisoformat(":".join(timeStringList))


def checkFix(text):
    '''Check if there is a time postfix (a.m. or p.m.) in the given text'''
    if text.__contains__("a.m."):
        return "am"
    elif text.__contains__("p.m."):
        return "pm"
    return None


def adjustForFix(currentFix, text):
    '''Adjust the hour given for the 24-hour format datetime uses'''
    if currentFix == "pm":
        if text != "12":
            text = str(int(text) + 12)
    if currentFix == "am" and text == "12":
        text = "00"
    return text


def set_alarm(alarm):
    """Set an alarm that, when the given time passes, activates an alarm sound"""
    # Set alarm and play the alarm sound when the time comes
    # print("Setting Alarm, press tab to cancel it")
    check_alarm(alarm)
    play_alarm()


def check_alarm(alarm):
    """Check the current alarm. If the current time matches the alarm, return"""
    # Check if the current time matches the alarm time
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
            link = results[i].find(css_identifier_link,
                                   first=True).attrs["href"]
        except:
            title = results[i].find(css_identifier_title, first=True).text
            link = results[i].find(css_identifier_link,
                                   first=True).attrs["href"]
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
    pdb.set_trace()


if __name__ == "__main__":
    main()
