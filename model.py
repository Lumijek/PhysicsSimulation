from math import sin, cos, atan, pi, sqrt
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt

del_t = 0.000001

time_elapsed = 0

gravity = 9.81

mu = 0.2

s_traveled_one = 17.9027136533 * 2

prev_v = None

def x(param):
	'''
	X-coordinate function of the parametric curve
	'''
	return 10 * (5/8) * cos(2 * param) * cos(param)

def y(param):
	'''
	Y-coordinate function of the parametric curve
	'''
	return 10 * sin(param) * cos(2 * param)

def xprime(param):
	'''
	First derivative of the X-coordinate function of the parametric curve
	'''
	return (25/4) * (-2 * sin(2 * param) * cos(param) - sin(param) * cos(2 * param))

def yprime(param):
	'''
	First derivative of the Y-coordinate function of the parametric curve
	'''
	return 10 * (-5 * cos(param) + 6 * (cos(param) ** 3))

def dsquaredydxsquared(param):
	'''
	Second derivative of the Y-coordinate with respect to the X-coordinate
	'''
	numerator = 128 * (3 * cos(4*param) - 13)
	denominator = 125 * (sin(param) + 3 * sin(3 * param)) ** 3
	return numerator / denominator

def slope(param):
	'''
	Slope of the parametric equation at point param.
	'''
	return yprime(param) / xprime(param)

def angle(param):
	'''
	Angle of the tangent vector on the curve at the point of the parameter
	'''

	angle = atan(slope(param))
	if x(param) == 0 and y(param) > 1:
		angle = pi/2

	elif x(param) == 0 and y(param) < 1:
		angle = 3 * pi/2

	elif x(param) < 0:

		angle += pi

	return angle

def norm(param):
	'''
	Finds the magnitude of the tangent vector at (x, y)
	'''
	return sqrt(xprime(param) ** 2 + yprime(param) ** 2)

def radius(param):
	'''
	Radius of curvature given at a specific point on the parametric curve
	'''
	return ((1 + slope(param) ** 2) ** (3/2)) / abs(dsquaredydxsquared(param))

def change_velocity(param, speed):
	'''
	Calculates a small change in velocity during the time period defined, del_t
	'''

	fn = (speed ** 2) / radius(param) + gravity * cos(angle(param))

	del_v = (gravity * sin(angle(param)) - fn * mu) * del_t

	speed += del_v

	return speed

def falls_off(param, v):
	if gravity * cos(angle(param)) > (v ** 2 / radius(param)) and param > 0:
		return True
	return False


def loop_once(initial_velocity):
	'''
	Main loop to model the motion of the object
	'''


	falls_off_track = False
	current_velocity = initial_velocity
	s = 0
	param = -pi/4
	time_elapsed = 0
	x1 = []
	y1 = []

	while (s < s_traveled_one and current_velocity > 0) and not falls_off_track:
		x1.append(x(param))
		y1.append(y(param))
		time_elapsed += del_t
		current_velocity = change_velocity(param, current_velocity)
		param = param + (current_velocity * del_t) / norm(param)
		s += current_velocity * del_t
		falls_off_track = falls_off(param, current_velocity)

		if param >= pi/4:
			param = -pi/4
			x1 = []
			y1 = []
	print("Initial velocity:", initial_velocity)
	print("Falls off track:", falls_off_track)
	print("Distance traveled:", s)
	print("Parameter value:", param)
	plt.plot(x1, y1)
	plt.show()
	return current_velocity
 
print("Final velocity:", loop_once(57.60143))
#velocity such that we travel around the loop once without falling off 57.60143 m/s
