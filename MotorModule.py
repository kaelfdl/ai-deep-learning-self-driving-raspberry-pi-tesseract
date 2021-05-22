import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

class Motor():
	'''
	This class defines a motor object that
	controls two motors using an L298N H-bridge
	motor controller.
	'''
	def __init__(self, EnA, In1A, In2A, In1B, In2B, EnB):
		self.EnA = EnA
		self.In1A = In1A
		self.In2A = In2A
		self.In1B = In1B
		self.In2B = In2B
		self.EnB = EnB
		GPIO.setup(self.EnA, GPIO.OUT)
		GPIO.setup(self.In1A, GPIO.OUT)
		GPIO.setup(self.In2A, GPIO.OUT)
		GPIO.setup(self.In1B, GPIO.OUT)
		GPIO.setup(self.In2B, GPIO.OUT)
		GPIO.setup(self.EnB, GPIO.OUT)
		self.pwmA = GPIO.PWM(self.EnA, 100)
		self.pwmA.start(0)
		self.pwmB = GPIO.PWM(self.EnB, 100)
		self.pwmB.start(0)

	def move(self, speed=0.5, turn=0, t=0):
		'''
		Control the motors with the given parameters
		'''
		speed *= 100
		turn *= 100
		left_speed = speed - turn
		right_speed = speed + turn

		if left_speed > 100:
			left_speed = 100
		elif left_speed < -100:
			left_speed = -100

		if right_speed > 100:
			right_speed = 100
		elif right_speed < -100:
			right_speed = -100

		self.pwmA.ChangeDutyCycle(abs(left_speed))
		self.pwmB.ChangeDutyCycle(abs(right_speed))

		if left_speed > 0:
			GPIO.output(self.In1A, GPIO.LOW)
			GPIO.output(self.In2A, GPIO.HIGH)
		else:
			GPIO.output(self.In1A, GPIO.HIGH)
			GPIO.output(self.In2A, GPIO.LOW)

		if right_speed > 0:
			GPIO.output(self.In1B, GPIO.LOW)
			GPIO.output(self.In2B, GPIO.HIGH)
		else:
			GPIO.output(self.In1B, GPIO.HIGH)
			GPIO.output(self.In2B, GPIO.LOW)

		sleep(t)

	def stop(self, t=0):
		'''
		Stops both motors
		'''
		self.pwmA.ChangeDutyCycle(0)
		self.pwmB.ChangeDutyCycle(0)
		sleep(t)

	def cleanup(self):
		'''
		Resets the state of the GPIO pins.
		Usually called with a try - finally statement
		'''
		GPIO.cleanup()
