
import time
from tkinter import *
from gpiozero import Button
from signal import pause
# !/usr/bin/env python3
# -- coding: utf-8 --
import RPi.GPIO as GPIO
import time
from RpiMotorLib import RpiMotorLib

################################
# RPi and Motor Pre-allocations
################################
#
# define GPIO pins for servo moteurs
GPIO.setmode(GPIO.BCM)  # Use Board numerotation mode
GPIO.setwarnings(False)  # Disable warnings
pwm_gpio = 26
frequence = 50
GPIO.setup(pwm_gpio, GPIO.OUT)
pwm = GPIO.PWM(pwm_gpio, frequence)

# define GPIO pins for step moteurs (nema17)
# même directions pour les 4 moteurs, car ils ne tournent pas en même temps
directio n= 22 # Direction (DIR) GPIO Pin
# un step par moteur
step1 = 23 # Step GPIO Pin
step2 = 27 # Step GPIO Pin
step3 = 24 # Step GPIO Pin
step4 = 17 # Step GPIO Pin



# Declare a instance of class pass GPIO pins numbers and the motor type
moteur1 = RpiMotorLib.A4988Nema(direction, step1, (21 ,21 ,21), "A4988")
moteur2 = RpiMotorLib.A4988Nema(direction, step2, (21 ,21 ,21), "A4988")
moteur3 = RpiMotorLib.A4988Nema(direction, step3, (21 ,21 ,21), "A4988")
moteur4 = RpiMotorLib.A4988Nema(direction, step4, (21 ,21 ,21), "A4988")




def arduino(command):
    print(command)
    pwm.start(angle_to_percent(0))
    delay = .0125
    nombreStep = 67
    waitTime = 0.5
    for letter in command:
        if letter == '0':
            pwm.ChangeDutyCycle(angle_to_percent(0))
            time.sleep(1)
        if letter == '9':
            pwm.ChangeDutyCycle(angle_to_percent(33))
            time.sleep(1)
        if letter == '1':
            moteur1.motor_go(False,  # True=Clockwise, False=Counter-Clockwise
                             "Full",  # Step type (Full,Half,1/4,1/8,1/16,1/32)
                             nombreSte p *2,  # number of steps
                             delay,  # step delay [sec]
                             False,  # True = print verbose output
                             .05)  # initial delay [sec]
            time.sleep(waitTime)
        if letter == '2':
            moteur1.motor_go(False,  "Full", nombreStep, delay, False, .05)
            time.sleep(waitTime)
        if letter == '3':
            moteur2.motor_go(False, "Full", nombreSte p *2, delay, False, .05)
            time.sleep(waitTime)
        if letter == '4':
            moteur2.motor_go(False, "Full", nombreStep, delay, False, .05)
            time.sleep(waitTime)
        if letter == '5':
            moteur3.motor_go(False, "Full", nombreSte p *2, delay, False, .05)
            time.sleep(waitTime)
        if letter == '6':
            moteur3.motor_go(False, "Full", nombreStep, delay, False, .05)
            time.sleep(waitTime)
        if letter == '7':
            moteur4.motor_go(False, "Full", nombreSte p *2, delay, False, .05)
            time.sleep(waitTime)
        if letter == '8':
            moteur4.motor_go(False, "Full", nombreStep, delay, False, .05)
            time.sleep(waitTime)

    pwm.ChangeDutyCycle(0)

    # Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0:
        return False

    start = 4
    end = 12.5
    ratio = (end - start ) /180  # Calcul ratio from angle to percent

    angle_as_percent = angle * ratio

    return start + angle_as_percent











