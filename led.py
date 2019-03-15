import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(14,GPIO.OUT)

while True:
    print "LED on"
    GPIO.output(14,GPIO.HIGH)
    time.sleep(0.015)
    print "LED off"
    GPIO.output(14,GPIO.LOW)
    time.sleep(0.015)
