import threading
import time
from playsound import playsound

timerSound = 'alarms/sci-fi.wav'

# class for Timer Thread


class Timer(threading.Thread):
    def run(self):
        # get the amount of seconds to sleep for
        seconds = int(self.time)

        # rather than doing this could do a loop that decrements a counter by 1 each iteration
        # and sleeps for a second each iteration
        while(seconds >= 0 and not self.__stopper):
            # print(seconds)
            time.sleep(1)
            seconds -= 1

            if(seconds == 0):
                playsound(self.sound)

    def __init__(self, time, timerSound, name=None):
        super(Timer, self).__init__()
        self.time = time
        self.sound = timerSound
        self.name = name
        self.__stopper = False

    def set_time(self, time):
        self.time = time

    def set_name(self, name):
        self.name = name

    def stop(self):
        print("stopping timer")
        self.__stopper = True


def create_timer(time, sound):
    # use this to start a timer
    Timer(time, sound).start()


def main():
    # print("This file isn't meant to be run as part of the final project.") # uncomment later: leave while testing
    create_timer()


if __name__ == '__main__':
    main()
