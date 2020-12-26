import RPi.GPIO as GPIO


class Gpio:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

    @staticmethod
    def set_digital(port, output):
        GPIO.setup(port, GPIO.OUT)
        if output == 1:
            GPIO.output(port, GPIO.HIGH)
        elif output == 0:
            GPIO.output(port, GPIO.LOW)
