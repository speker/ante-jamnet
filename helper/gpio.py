import RPi.GPIO as GPIO


class Gpio:

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def set_digital(self, port, output):
        GPIO.setup(port, GPIO.OUT)
        GPIO.output(12, output)

