import RPi.GPIO as GPIO
import time

variable = 0b000001011101
GPIO_NUMBER = 14


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_NUMBER, GPIO.OUT)


def send_sync_bit():
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(0.00045)


def send_zero():
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(0.00045)
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(0.00045)


def send_one():
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(0.00045)
    GPIO.output(GPIO_NUMBER, GPIO.HIGH)
    time.sleep(0.00045)
    GPIO.output(GPIO_NUMBER, GPIO.LOW)
    time.sleep(0.00015)


def send_data(input_data, bits_count):

    for i in range(0, 500):

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