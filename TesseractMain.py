import cv2
import os
import numpy as np

import CameraModule as cm
import MotorModule as mt
from TfLiteInterpreter import Interpreter

#### Configuration ####################################
steering_sensitivity = 1.9
max_throttle = 0.35
motor = mt.Motor(18, 11, 13, 15, 16, 22)
tflite_modelpath = 'model_v1.tflite'
#######################################################

def preprocess(img):
    img = img[174:,:,:]
    img = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    img = cv2.GaussianBlur(img, (3,3), 0)
    img = cv2.resize(img, (200, 66))
    img = img / 255
    return img


try:
    interpreter = Interpreter(tflite_modelpath)

    while True:
        img = cm.get_img(False, size=[480,240])
        img = preprocess(img)
        img = np.array([img], dtype=np.float32)
        steering = interpreter.interpret(img)
        print(steering[0][0] * steering_sensitivity)
        motor.move(max_throttle, -steering * steering_sensitivity)
        cv2.waitKey(1)
finally:
    motor.cleanup()
