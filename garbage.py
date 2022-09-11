import keyboard  # using module keyboard
while True:  # making a loop
    # try:  # used try so that if user pressed other than the given key error will not be shown
    if keyboard.is_pressed('space'):  # if key 'q' is pressed
        print('Space has been pressed')
        break  # finishing the loop
    # except:
    #     break  # if user pressed a key other than the given key the loop will break
