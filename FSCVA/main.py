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


def get_keyboard_input():
    print("Press Space Bar to start the virtual assistant")

    while True:
        if keyboard.is_pressed('space'):
            print("Virtual Assistant started")
            break


def main():
    get_keyboard_input()

    # Voice Recognizer
    recognizer = sr.Recognizer()

    # TTS Initialization
    converter = pyttsx3.init()
    converter.setProperty('volume', 0.7)

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

                if("timer" in text):
                    if("cancel" in text):
                        print("cancelling timer ")
                        widgets.cancel_timer()
                    else:
                        widgets.set_timer(text)

                print(f"Recognized: {text}")

        except sr.UnknownValueError:
            # print("Error")
            # recognizer = sr.Recognizer()
            continue


def speak(text, converter):
    '''Uses tts to speak the given text'''
    converter.say(text)
    converter.runAndWait()


if __name__ == '__main__':
    main()
