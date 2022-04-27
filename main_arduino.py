# Importing Libraries
import serial
import time
from tkinter import *
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)


def write_reads(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data



def main(algo):
    sommets = [letter for letter in algo if letter.islower()]
    middle = [letter for letter in algo if letter.isupper()]
    message = ""
    for l in algo :
        message += l
    # time.sleep(1.5)

    print("oui",write_reads(message))



def servo_manually():
    # set up GUI
    root = Tk()

    # draw a nice big slider for servo position
    scale = Scale(root,
                  command=write_reads,
                  to=175,
                  orient=HORIZONTAL,
                  length=400,
                  label='Angle')
    scale.pack(anchor=CENTER)

    # run Tk event loop
    root.mainloop()

if __name__ == "__main__":
  servo_manually()
