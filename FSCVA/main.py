# main.py
# Main File for Virtual Assistant
# Do the following to properly run this script:
# brew install portaudio
# pip install 'speechrecognition', 'pyaudio', and 'pyttsx3' before running
from threading import Thread
import speech_recognition as sr
import classifier as clf
import widgets
import pyttsx3
import threading
import pdb
import timer
import keyboard
import datetime
import multiprocessing
import time


# threaded function to allow quick stopping of VA
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


# function that actually starts the speech of the virtual assisstant
def speak(text):
    converter = pyttsx3.init()
    converter.setProperty("volume", 0.7)
    converter.setProperty(
        "rate", 175
    )  # changed the speed of the VA, default was 200 wpm, too fast imo

    # String to Speak
    if isinstance(text, str):
        converter.say(text)
        converter.runAndWait()

    # List to Speak
    else:
        for item in text:
            converter.say(text)
            converter.runAndWait()

    converter.stop()


# called to stop the VA mid speech
def stop_speaker():
    global t
    global term
    term = True
    # t.join()


@threaded
def manage_process(p):
    global term
    while p.is_alive():
        if term:
            p.terminate()
            term = False
        else:
            continue


# this is what you call when you want to give the VA something to say now
def say(text):
    """Uses tts to speak the given text"""
    global t
    global term
    term = False
    # use multiprocessing to start the speach of VA
    p = multiprocessing.Process(target=speak, args=(text,))
    p.start()
    t = manage_process(p)


def get_keyboard_input():
    # wait for user to press space to start the VA
    while True:
        if keyboard.is_pressed("space"):
            stop_speaker()
            print("Virtual Assistant listening")
            break
        elif keyboard.is_pressed("Esc"):
            print("exiting program")
            exit()


def main():
    # Load the SVM in classifier.py
    print("Loading...\r", end="")
    clf.load_svm_corpus()

    # Give it a Dummy Query (the first one is slow for some reason)
    clf.predict("The cake is a lie.")

    # Dictionary of Intent Functions for Easy Calling
    intents = {
        "get_weather": widgets.get_weather,
        "get_time": widgets.get_time,
        "get_date": widgets.get_date,
        "get_menu": widgets.get_menu,
        "get_balance": widgets.get_balance,
        "flip_coin": widgets.flip_coin,
        "roll_dice": widgets.roll_dice,
        "manage_alarm": widgets.manage_alarm,
        "manage_timer": widgets.manage_timer,
        "define_word": widgets.define_word,
        "get_schedule": widgets.get_schedule,
        "calculate": widgets.calculate,
    }

    print("Press Space Bar to start the virtual assistant")
    get_keyboard_input()
    response = ""

    # Voice Recognizer
    recognizer = sr.Recognizer()

    # for index, name in enumerate(sr.Microphone.list_microphone_names()):
    # print("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))

    # Variables setup required for widgets (ex. alarms for the Alarm widget)
    alarm = []

    while True:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                # Use Google's STT and Get Text Back
                text = recognizer.recognize_google(audio)
                text = text.lower()
                text = str(text)

                print(f"Recognized: {text}")

                # Predict Intent
                intent = clf.predict(text)

                # Call Corresponding Widget from Predicted Intent
                response = intents[intent](text)

                if response != "" and response != None:
                    say(response)

                # Format Widget Response
                print(f"Intent: {intent}")
                print(f"Response: {response}")

                # response = f'I detected a {intent} query.' # testing

                print("\nPress [Space] to say another command\n")

                get_keyboard_input()

        except sr.UnknownValueError:
            # print("Error")
            # recognizer = sr.Recognizer()
            continue


if __name__ == "__main__":
    main()
