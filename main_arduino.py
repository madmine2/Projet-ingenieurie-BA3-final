
import time
from tkinter import *
import raspberrypi_instead_of_arduino as ras
from gpiozero import Button
from signal import pause




def write_reads(x):
    ras.arduino(bytes(x, 'utf-8'))


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
            print(message_sommet)
            write_reads("")
            time.sleep(2)
            write_reads(message)
            break


def servo_manually():
    for i in range(2):
        ras.arduino('012345678')
        time.sleep(2)


if __name__ == "__main__":
    while (True):
        button = Button(2)
        button.when_pressed = servo_manually
        pause()
