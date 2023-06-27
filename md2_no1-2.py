import RPi.GPIO as GPIO
import ADC0834
import time
import math
from datetime import datetime

data = []

def init():
	ADC0834.setup()

def loop():
	while True:
		analogVal = ADC0834.getResult()
		Vr = 5 * float(analogVal) / 255
		Rt = 10000 * Vr / (5 - Vr)
		temp = 1/(((math.log(Rt / 10000)) / 3950) + (1 / (273.15+25)))
		Cel = temp - 273.15
		now = datetime.now()
		dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
		data.append(dt_string + ',Celsius: %.2f' % Cel)
		print (dt_string + ' Celsius: %.2f' % Cel)
		time.sleep(1)

def save_csv():
	with open("atmospheric_temperature.csv",mode="w") as file:
		for i in range(len(data)):
			file.writelines(data[i] + '\n')

if __name__ == '__main__':
	init()
	try:
		loop()
	except KeyboardInterrupt:
		save_csv()
		ADC0834.destroy()
