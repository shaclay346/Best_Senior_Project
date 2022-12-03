# widgets.py
# File of widgets called by main (fetch the caf menu, fetch the weather, etc.)
import werkzeug
import threading
from playsound import playsound
import random, voice, time, math, json, pdb, sys, re, io, multiprocessing, datetime, os
from robobrowser import RoboBrowser
import pyaudio, wave
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import ssl, urllib
from timer import Timer
from requests_html import HTMLSession
from googlesearch import search
from bs4 import BeautifulSoup
import requests as rq
werkzeug.cached_property = (
    werkzeug.utils.cached_property
)

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

    # chrome_options = Options()
    # chrome_options.headless = True

    # Change Chromedriver File Depending on OS
    if sys.platform == 'darwin':  # MacOS
        path = os.path.join(ROOT, 'chromedriver')
    elif sys.platform in ['win32', 'win64', 'cygwin']:  # Windows
        path = os.path.join(ROOT, 'chromedriver.exe')
    else:  # Other
        return f"Unsupported OS. Our implementation of chromedriver is not supported on your os, {sys.platform}"

    chrome_options = Options()
    # opt = webdriver.ChromeOptions()-=[p mn]]]"HNJB;.\[b8u pl\ bl 6yyyyyyyyyvg;plo"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-logging")
    chrome_options.add_argument("--disable-crash-reporter")

    driver = webdriver.Chrome(options=chrome_options)

    # have chrome open the SSO page
    driver.get("https://sso.flsouthern.edu/home/414")

    time.sleep(3.5)

    driver.find_element(By.ID, "branding-username").send_keys(username)
    driver.find_element(By.ID, "branding-password").send_keys(password)

    # id = branding-sumbit-button
    login_button = driver.find_element(By.ID, "branding-sumbit-button")
    login_button.click()

    time.sleep(4)

    # if a security question gets asked this handles it, at least for me (Shane)
    try:
        # //*[@id="mfaDivId"]/form/div[2]/div[2]/div[2]/a
        security_button = driver.find_element(
            By.XPATH, r"""/html/body/div[4]/div/div[3]/div/div/form/div[2]/div[2]/div[2]"""
        )
        security_button.click()

        question = ""

        while True:
            question = driver.find_element(
                By.XPATH,
                r"""//*[@id="securityQuestionModal"]/div[3]/div/div/div[2]/div[2]/form/div[1]/div/p""",
            ).text

            if "movie" in question:
                break

            skip_button = driver.find_element(
                By.XPATH,
                r"""//*[@id="securityQuestionModal"]/div[3]/div/div/div[2]/div[2]/form/div[2]/button[2]""",
            )
            skip_button.click()

            time.sleep(2)

        # id for Answer: securityAnswer
        driver.find_element(By.ID, r"""securityAnswer""").send_keys("hot rod")
        time.sleep(3)

        submit_button = driver.find_element(
            By.XPATH,
            r"""//*[@id="securityQuestionModal"]/div[3]/div/div/div[2]/div[2]/form/div[2]/button[4]""",
        )
        submit_button.click()

        time.sleep(6)
        canvas_card = driver.find_element(
            By.XPATH,
            r"""//*[@id="contentDiv"]/div[7]/div/div/div[1]""",
        )
        canvas_card.click()

    # sometimes a security question won't be asked, so just click on the access canvas card
    except:
        time.sleep(3)

        canvas_card = driver.find_element(
            By.XPATH,
            r"""//*[@id="contentDiv"]/div[7]/div/div/div[1]""",
        )
        canvas_card.click()

    finally:
        time.sleep(6)

        driver.get("https://flsouthern.instructure.com/")
        time.sleep(4)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        # find info about the assignments by getting items with this class
        tags = soup.find_all("span", class_="ergWt_bGBk")

        length = len(tags)
        output = ""
        # output = f"you have {length} upcoming assignments.\nhere they are:"
        assignments = 0
        for i in range(len(tags) - 1):
            s = str(tags[i].getText())
            if("due" in s):
                assignments += 1
                # assignments.append(tags[i].getText())
        output += f"you have {assignments} upcoming assignments.\nhere they are:"

        for i in range(len(tags)):
            s = str(tags[i].getText())
            if("due" in s):
                temp = tags[i].getText()
                output += f"{temp}\n"

        return output


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

        # Check if LUNCH exists. If not, brunch
        next_meal = "LUNCH" if "LUNCH" in dishes else "BRUNCH"

        dishes = dishes[dishes.index("BREAKFAST") + 1: dishes.index(next_meal)]

    elif "brunch" in text:
        # Bad Menu Check
        if "BRUNCH" not in dishes or "DINNER" not in dishes:
            return random.choice(fanswers)

        meal = "brunch"
        dishes = dishes[dishes.index("BRUNCH") + 1: dishes.index("DINNER")]

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
            "BRUNCH",
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

    # Display Loading Message (Since this is a slow process)
    waiting = show_waiting()

    # Load login credentials from login_credentials.txt
    username, password = load_login_creds("get")

    chrome_options = Options()
    chrome_options.headless = True

    # Change Chromedriver File Depending on OS
    if sys.platform == 'darwin':  # MacOS
        path = os.path.join(ROOT, 'chromedriver')
    elif sys.platform in ['win32', 'win64', 'cygwin']:  # Windows
        path = os.path.join(ROOT, 'chromedriver.exe')
    else:  # Other
        return f"Unsupported OS. Our implementation of chromedriver is not supported on your os, {sys.platform}"

    driver = webdriver.Chrome(path, options=chrome_options)

    url = "https://get.cbord.com/flsouthern/full/login.php"

    driver.get(url)

    time.sleep(1)

    driver.find_element(By.ID, "login_username_text").send_keys(username)
    driver.find_element(By.ID, "login_password_text").send_keys(password)

    login_button = driver.find_element(By.ID, "login_submit")
    login_button.click()

    time.sleep(1)

    table = driver.find_element(By.ID, "get_funds_overview")

    # Get Accounts (Flex, Snake Bites in that order)
    contents = [a for a in table.text.split('\n') if any(
        b in a for b in ['Flex Dollars', 'Snake Bites'])]

    # Be Snarky if You're Kinda Broke
    monies = [a.split()[-1] for a in contents]

    total = sum([float(a[1:]) for a in monies])

    if total < 10:
        return f"Your wallet's looking light. You have {monies[1]} worth of Snake Bites and {monies[0]} worth of Flex Dollars."
    else:
        return f"You have {monies[1]} worth of Snake Bites and {monies[0]} worth of Flex Dollars."


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

    # Convert Cº to Fº (K − 273.15) × 9/5 + 32
    temperature = math.floor((temperature - 273.15) * 9 // 5 + 32)
    feels_like = math.floor((feels_like - 273.15) * 9 // 5 + 32)

    # Output

    # Basic Output
    output = f"Looks like there'll be some {description} today"

    # Rain
    if type_.lower() == 'rain':
        output += ", so I'd recommend you take an umbrella with you"

    # Temperature / Feels Like Temperature
    output += f". It's currently {temperature}ºF"

    if abs(feels_like - temperature) > 3:
        output += f", but it feels like {feels_like}"

    output += "."

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

    # If no table, incorrect credentials were given.
    if not table:
        return "Incorrect login credentials given."

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
        result = 0 if operands[1] == 0 else round(operands[0] / operands[1], 3)

    return str(result)


def manage_alarm(text):
    """Wrapper method for adding/canceling alarms."""
    global alarmPros

    # Check text for what we need to do
    if "cancel" in text: # Cancel alarm
        if alarmPros.is_alive():
            alarmPros.terminate()
            alarmPros = multiprocessing.Process()
            return "Alarm Cancelled"
        return "There is no alarm set"
    else: # Create alarm
        if alarmPros.is_alive():
            return "Alarm already set, cancel the current alarm to make a new one"
        alarm = getAlarmTime(text)
        if type(alarm) == str: #If the alarm couldn't be made because of some error
            return alarm
        alarmPros = multiprocessing.Process(target=set_alarm, args=(alarm,))
        alarmPros.start()
        return "Alarm Set"


def getAlarmTime(text):
    '''Extract the wanted time from the given text'''

    # Search through the given text for a time, returning error string if there is no time specified
    timeStartIndex = -1
    for i in range(len(text)):
        if text[i].isnumeric():
            timeStartIndex = i
            break
    if timeStartIndex == -1:
        return "No time has been given, please make an alarm with a time"

    # Using the starting index of the wanted time, determine the format of it (single number or time)
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
            return "That is not a valid time, please make an alarm with a valid time"
    else:
        checkString = timeString.split(":")
        if int(checkString[0]) < 0 or int(checkString[0]) > 23 or int(checkString[1]) < 0 or int(checkString[1]) > 59:
            return "That is not a valid time, please make an alarm with a valid time"

    # Check if the text specifies am or pm for 24 hour conversion, returning an error if not recognized and needed
    currentFix = None
    currentFix = checkFix(text)
    if currentFix == None and timeFormat != "time" and int(timeString) < 13:
        return "No abbreviation recognized, try again including a.m. or p.m."

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
    '''Check if there is a time abbreviation (a.m. or p.m.) in the given text'''
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
    check_alarm(alarm)
    play_alarm()


def check_alarm(alarm):
    """Check the current time. If the current time matches the alarm, return"""
    while True:
        if (
            datetime.datetime.now().hour == alarm.hour
            and datetime.datetime.now().minute == alarm.minute
        ):
            return


def play_alarm():
    """Play an alarm sound, unless flagged to stop or the sound ends"""
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
    word = ""

    # if they said define _____   extract the second word
    if "define" in text:
        word = text.split(" ", 1)[1].rsplit(" ", 1)[0]
    # otherwise they probably said whats the definition of ____
    else:
        idx = text.rfind(' ')
        for i in range(idx+1, len(text)):
            word += text[i]

    # https://api.dictionaryapi.dev/api/v2/entries/en/<word>
    if word == "":
        return "unable to define that word."

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
    ]
    return random.choice(options)


def show_waiting():
    """Returns and speaks "One moment..." Answer"""
    options = ["One second...\r", "Checking...\r", "Hold on...\r"]
    choice = random.choice(options)

    print(f"{choice}\r")

    # voice.say(choice.strip()) # uncomment for presentation


def load_login_creds(site):
    """Loads portal and SSO credentials for use in
    get_schedule and get_upcoming_assignments."""
    with open(os.path.join(ROOT, "login_credentials.txt"), "r") as f:
        creds = [a.strip()
                 for a in f.readlines() if a and not a.startswith("#")]

    if site == "portal":
        return creds[:2]
    elif site == "sso":
        return creds[2:-2]
    elif site == "get":
        return creds[-2:]
    else:
        return ["", ""]


def main():
    # print("This file isn't meant to be run as part of the final project.") # uncomment later: leave while testing
    print(get_assignments(""))
    # pdb.set_trace()


if __name__ == "__main__":
    main()
