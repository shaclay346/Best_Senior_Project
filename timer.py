import threading
import time
from playsound import playsound

timerSound = 'alarms/mixkit-scanning-sci-fi-alarm-905.wav'

# class for Timer Thread


class Timer(threading.Thread):
    # Default called function with mythread.start()
    def run(self):
        print('here', self.time)

        # get the amount of seconds to sleep for
        seconds = int(self.time)

        # rather than doing this could do a loop that decrements a counter by 1 each iteration
        # and sleeps for a second each iteration
        print("timer started for ", seconds, " seconds")
        while(seconds >= 0 and not self.__stopper):
            # print(seconds)
            time.sleep(1)
            seconds -= 1

            if(seconds == 0):
                playsound(self.sound)

    def __init__(self, time, timerSound):
        super(Timer, self).__init__()
        self.time = time
        self.sound = timerSound
        self.__stopper = False

    def set_time(self, time):
        self.time = time

    def stop(self):
        self.__stopper = True
