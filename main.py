# main.py
# Main File for Virtual Assistant
# Do the following to properly run this script:
# brew install portaudio
# pip install 'speechrecognition', 'pyaudio', and 'pyttsx3' before running
import speech_recognition as sr
import widgets
import pyttsx3
import threading
import pdb
import timer
import keyboard
import multiprocessing
import time
from threading import Thread


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrapper


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('volume', 0.7)
    # changed the speed of the VA, default was 200 wpm, too fast imo
    engine.setProperty("rate", 175)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def stop_speaker():
    print("here")
    global term
    term = True
    t.join()


@threaded
def manage_process(p):
    global term
    while p.is_alive():
        if term:
            p.terminate()
            term = False
        else:
            continue


def get_keyboard_input():
   # kill the speaking thread here

    while True:
        if keyboard.is_pressed('space'):
            print("Virtual Assistant started")
            break


# this is what you call when you want to give the VA something to say now
def say(text):
    '''Uses tts to speak the given text'''
    global t
    global term
    term = False
    p = multiprocessing.Process(target=speak, args=(text,))
    p.start()
    t = manage_process(p)


def main():
    print("Press Space Bar to start the virtual assistant")
    get_keyboard_input()

    # Voice Recognizer
    recognizer = sr.Recognizer()

    # TTS Initialization
    # converter = pyttsx3.init()
    # converter.setProperty('volume', 0.7)

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

                response = ""
                if("timer" in text):
                    if("cancel" in text):
                        print("cancelling timer ")
                        widgets.cancel_timer()
                    else:
                        widgets.set_timer(text)
                if("time" in text):
                    response = widgets.get_time()

                print(f"Recognized: {text}")

                # print something like press space to give a new command
                if(response != ""):
                    say(response)
                    print("press space to say another command")
                    get_keyboard_input()
                else:
                    print("press space to say another command")
                    get_keyboard_input()

        except sr.UnknownValueError:
            # print("Error")
            # recognizer = sr.Recognizer()
            continue


if __name__ == '__main__':
    main()
