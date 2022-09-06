import threading
import time
import main


class MyThread(threading.Thread):
    # Default called function with mythread.start()
    def run(self):
        # self._running = True
        # "Thread-x started!"
        # while(self._running):
        print("{} started!".format(self.getName()))

        # get the amount of seconds to sleep for
        name = self.getName()
        x = "-"
        res = name.split(x, 1)
        seconds = int(res[1])

        print(seconds)

        print("timer started for ", seconds, " seconds")
        time.sleep(seconds)

    def stop(self):
        print("stopping thread")
        # self._running = False
        try:
            self._stop_event.set()
        except:
            print("asdf")


# helper to start a thread that will run the timer
def main(seconds):
    # give the thread the time to run for
    mythread = MyThread(name="Thread-{}".format(seconds))
    # start the thread
    mythread.start()

    time.sleep(2)
    cancel_timer()

    mythread.join()
    print("timer has gone off.")

    # call something in main.py to make timer go off
    # or have a speak object say something in this file


# find a way to make the thread die
def cancel_timer():
    MyThread().stop()
    pass


if __name__ == '__main__':
    main(8)
