"""import functions as fn
import RPi.GPIO as GPIO
from time import sleep


posTerminal1 = 40 #--value of physical pin +circuit is connected to for error 1
posTerminal2 = 38
posTerminal3 = 36
posTerminal4 = 32



def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(posTerminal1, GPIO.IN,pull_up_down=GPIO.PUD_UP) #posTerminal1 set to input pullup
	GPIO.setup(posTerminal2, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(posTerminal3, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(posTerminal4, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def run():
	emailSent = 0 #--binary value to stop multiple emails from being sent
	while True:
		if GPIO.input(posTerminal1)==1: #--1 represents no voltage to pin
			if(emailSent==0):
				fn.sendEmail()
				fn.sendText()
				emailSent = 1
				sleep(2)
		else:
			emailSent = 0


def close():
	GPIO.cleanup()
	
	
if __name__ == '__main__':
	setup()
	try:
		run()
	except KeyboardInterrupt: #terminate program with ctrl c
		close()"""

import functions as fn

fn.sendText(1)
