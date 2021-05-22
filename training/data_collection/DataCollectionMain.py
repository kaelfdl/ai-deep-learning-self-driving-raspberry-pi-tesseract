import os
import sys
base_dir = os.path.abspath(__file__).split('/')[:-3]
base_dir = '/'.join(base_dir)
sys.path.insert(0, base_dir)

import cv2
from time import sleep

import MotorModule as mt
import JoyStickModule as js
import DataCollectionModule as dc
import CameraModule as cm

##### Configuration ######
max_throttle = 0.35
motor = mt.Motor(18, 11, 13, 15, 16, 22)
controller = 'joystick'
#########################

record = 0
try:
    while True:
        if controller == 'joystick':
            js_val = js.get_js()
            steering = js_val['axis1']
            throttle = js_val['axis2'] * max_throttle
            if js_val['options'] == 1:
                if record == 0:
                    print('Recording Started...')
                record += 1
                sleep(0.3)
            if record == 1:
                img = cm.get_img() 
                dc.save_data(img, steering)
            elif record == 2:
                record = 0
                dc.save_log()
            
            motor.move(-throttle, -steering)
            cv2.waitKey(1)
finally:
    motor.cleanup()
