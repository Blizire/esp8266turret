
import requests
from xbox import XboxController
from time import sleep

class Servo:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.xServoPos = 90
        self.yServoPos = 90

    def validate_pos(self):
        if(self.xServoPos > 180):
            self.xServoPos = 180
        if(self.xServoPos < 0):
            self.xServoPos = 0
        if(self.yServoPos > 180):
            self.yServoPos = 180
        if(self.yServoPos < 0):
            self.yServoPos = 0

    def servo_center(self):
            self.xServoPos = 90
            self.yServoPos = 90
            self.validate_pos()
            requests.get(f'http://{self.ip}:{self.port}/x/{self.yServoPos}')
            requests.get(f'http://{self.ip}:{self.port}/y/{self.yServoPos}')

    def servo_control(self, servo, pos):
        if servo == 'x':
            self.xServoPos -= pos
            #self.xServoPos *= -1
            self.validate_pos()
            requests.get(f'http://{self.ip}:{self.port}/{servo}/{self.xServoPos}')
        if servo == 'y':
            self.yServoPos -= pos
            #self.yServoPos *= -1
            self.validate_pos()
            requests.get(f'http://{self.ip}:{self.port}/{servo}/{self.yServoPos}')

    def servo_sweep(self):
        for i in range(181):
            self.servo_control('x', i)
            self.servo_control('y', i)
        for i in range(180,-1, -1):
            self.servo_control('x', i)
            self.servo_control('y', i)     


if __name__ == '__main__':

    servo = Servo('192.168.0.250', 5050)
    joy = XboxController()
    mult = 20
    for i in range(4):
        servo.servo_center()
        sleep(0.1)
    while True:
        x, y, a, b, rb = joy.read()
        print(f'xPos : {servo.xServoPos}\nyPos : {servo.yServoPos}')
        servo.servo_control('x', x * mult )
        servo.servo_control('y', y * mult)
        sleep(0.01)
        

