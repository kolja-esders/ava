import RPi.GPIO as GPIO
import time


GPIO_NUMBER = 14

short_delay = 0.000265
long_delay = 0.000865

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_NUMBER, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)


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

        #waiting 10ms between data stream
        time.sleep(0.010)


def send_command(device, action):
    
    GPIO.output(14, device)
    GPIO.output(15, action)

    time.sleep(0.5)


#send_command(1, 0)
