# Importing Libraries
import serial
import time
from tkinter import *
arduino = serial.Serial(port='COM6', baudrate=115200, timeout=.1)


def write_reads(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def traduction(algo):
    temp = ""
    for move in algo:
        if move == 'R':
            temp += '1'
        elif move == "R'":
            temp += '2'
        elif move == 'U':
            temp += '3'
        elif move == "U'":
            temp += '4'
        elif move == 'L':
            temp += '5'
        elif move == "L'":
            temp += '6'
        elif move == 'F':
            temp += '7'
        elif move == "F'":
            temp += '8'

    return temp

def main(algo):

    sommet = [letter.replace("'","P").upper().replace('P', "'" ) for letter in algo if letter.islower()]
    sommets = traduction(sommet)
    middl = [letter for letter in algo if letter.isupper()]
    middle = traduction(middl)

    message_sommet = "9"
    for l in sommets :
        message_sommet += l


    message_face = "0"
    for l in middle:
        message_face += l
    # time.sleep(1.5)
    temp = ["r'", "U"]
    print(message_sommet)
    write_reads(message_sommet)
    time.sleep(1*len(sommet))
    print(message_face)
    write_reads(message_face)
    time.sleep(1 * len(middl))



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
