import time
from tkinter import *
import control_motor as ras
from gpiozero import Button
from signal import pause

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


def main(algo, button):
    ras.arduino("909")
    sommet = [letter.replace("'", "P").upper().replace('P', "'") for letter in algo if letter.islower()]
    sommets = traduction(sommet)
    middl = [letter for letter in algo if letter.isupper()]
    middle = traduction(middl)

    message_sommet = "9"
    for l in sommets:
        message_sommet += l

    message_face = "0"
    for l in middle:
        message_face += l
    # time.sleep(1.5)
    message = message_sommet + message_face
    while (True):
        if button.is_pressed:
            ras.arduino(message)
            ras.arduino("9")
            break


def servo_manually():
    for i in range(1):
        ras.arduino('9') #9472508248373546374831324142


if __name__ == "__main__":
    servo_manually()
    while (True):
        button = Button(2)
        button.when_pressed = servo_manually
        pause()