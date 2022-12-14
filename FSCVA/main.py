# main.py
# Main/Application File for Virtual Assistant
import nltk

# Check if First-Time NLTK Install is Needed
try:
    import nltk.corpus
except KeyError:
    import importCheck

    print(
        "nltk download needed; press [Space] when the download has completed.")
    time.sleep(1)
    importCheck.firstTimenltk()
    while True:
        if keyboard.is_pressed("space"):
            break

# silence robobrowser warnings
from urllib3.exceptions import InsecureRequestWarning
import speech_recognition as sr
import argparse
import datetime
import keyboard
import requests
import time
import timer
import pdb

# Our Imports
import classifier as clf
import widgets
import voice

# Argument Parsing
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--present',
                    help='presentation mode', action='store_true')


def get_keyboard_input():
    """Wait for the user to press [Space] to start the VA"""
    while True:
        if keyboard.is_pressed("space"):
            voice.stop_speaker()
            print("Virtual Assistant Listening...\r")
            break
        elif keyboard.is_pressed("Esc"):
            print("Exiting program...")
            exit()


def main(args):
    # Disable Robobrowser Warning since Portal is Bad™
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

    # Load the SVM in classifier.py
    print("Loading...\r", end="")
    clf.load_svm_corpus()

    # Give it a Dummy Query (the first one is slow for some reason)
    clf.predict("The cake is a lie.")

    # Dictionary of Intent Functions for Easy Calling
    intents = {
        "calculate": widgets.calculate,
        "define_word": widgets.define_word,
        "flip_coin": widgets.flip_coin,
        "get_assignments": widgets.get_assignments,
        "get_balance": widgets.get_balance,
        "get_date": widgets.get_date,
        "get_menu": widgets.get_menu,
        "get_schedule": widgets.get_schedule,
        "get_time": widgets.get_time,
        "get_weather": widgets.get_weather,
        "google_search": widgets.google_search,
        "manage_alarm": widgets.manage_alarm,
        "manage_timer": widgets.manage_timer,
        "roll_dice": widgets.roll_dice,
        "unknown": widgets.unknown,
        "wake_up": widgets.wake_up,
    }

    print("Press [Space] to start the virtual assistant.")
    get_keyboard_input()
    response = ""

    # Voice Recognizer
    recognizer = sr.Recognizer()

    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    # print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name)) # debug if microphone isn't recognized

    while True:
        try:
            with sr.Microphone() as mic:
                # duration is the length of silence it will accept before continuing
                recognizer.adjust_for_ambient_noise(mic, duration=0.3)
                audio = recognizer.listen(mic)

                # Use Google's STT and Get Text Back
                text = recognizer.recognize_google(audio)
                text = str(text.lower())

                print(f"\rRecognized: {text}")

                # Predict Intent
                intent = clf.predict(text)

                # Call Corresponding Widget from Predicted Intent
                response = intents[intent](text)

                if response:
                    voice.say(response)

                # Format Widget Response
                # print(f"Intent: {intent}")
                print(f"> {response}")

                print("\nPress [Space] to say another command\n")

                get_keyboard_input()

        # STT throws errors if it can't transcribe what it hears; this catches them.
        except sr.UnknownValueError:
            continue


if __name__ == "__main__":
    main(parser.parse_args())
