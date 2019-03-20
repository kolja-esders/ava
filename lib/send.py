import RPi.GPIO as GPIO
import time


SET = 4
STATE = 14
BIT_0 = 15
BIT_1 = 17
BIT_2 = 18


short_delay = 0.000265
long_delay = 0.000865

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(SET, GPIO.OUT)
GPIO.setup(STATE, GPIO.OUT)
GPIO.setup(BIT_0, GPIO.OUT)
GPIO.setup(BIT_1, GPIO.OUT)
GPIO.setup(BIT_2, GPIO.OUT)

"""
def send_sync_bit():
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(short_delay)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(long_delay)


def send_zero():
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(short_delay)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(long_delay)
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(short_delay)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(long_delay)


def send_one():
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(short_delay)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(long_delay)
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(long_delay)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(short_delay)


def send_data(input_data):
    bits_count = 12
    input_data = 0b000000111110

    for i in range(0, 10):

        bits_count_work = bits_count
        input_data_work = input_data

        while bits_count_work > 0:

            if input_data_work & (1 << 11):
                send_one()
            
            else:
                send_zero()
            
            bits_count_work -= 1
            input_data_work = input_data_work << 1
        
        send_sync_bit()

        # Waiting 10ms between data packets.
        time.sleep(0.010)
"""

# send_command because just using arduino to transmit data via 433MHz
# RPi -- parallel communication --> Arduino
def send_command(device, action):
    
    # -4 because BIT_2 (4, 2, 1)
    if device - 4 >= 0:
        device -= 4
        GPIO.output(BIT_2, 1)
    
    if device - 2 >= 0:
        GPIO.output(BIT_1, 1)
        device -= 2
    
    if device - 1 >= 0:
        GPIO.output(BIT_0, 1)
        device -= 1

    GPIO.output(STATE, action)
    GPIO.output(SET, 1)

    time.sleep(0.5)

    GPIO.output(SET, 0)
    GPIO.output(STATE, 0)
    GPIO.output(BIT_0, 0)
    GPIO.output(BIT_1, 0)
    GPIO.output(BIT_2, 0)

#send_command(1, 1)
