# voice.py
# Handles the TTS functionality of the VA
from threading import Thread
import multiprocessing
import threading
import pyttsx3

# threaded function to allow quick stopping of VA
def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


# actually starts the speech of the virtual assisstant
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
    p.start() # it says "The process has forked and you cannot use this CoreFoundation functionality safely. You MUST exec()." and crashes python when this line is uncommented.
    t = manage_process(p)
    pass


def main():
	pass


if __name__ == '__main__':
	main()
