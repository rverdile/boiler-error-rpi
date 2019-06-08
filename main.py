import functions as fn
import RPi.GPIO as GPIO
from time import sleep


pos_terminal_1 = 40 #--value of physical pin +circuit is connected to for error 1
pos_terminal_2 = 38
pos_terminal_3 = 36
pos_terminal_4 = 32


def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pos_terminal_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) #posTerminal1 set to input pullup
	GPIO.setup(pos_terminal_2, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pos_terminal_3, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pos_terminal_4, GPIO.IN,pull_up_down=GPIO.PUD_UP)

def run():
	
	error_1=0
	error_2=0
	error_3=0
	error_4=0

	while True:
		
		if(GPIO.input(pos_terminal_1)==1 and error_1==0):
			error_1=1
		elif(GPIO.input(pos_terminal_1)==0):
			error_1=0
			
		if(GPIO.input(pos_terminal_2)==1 and error_2==0):
			error_2=1
		elif(GPIO.input(pos_terminal_2)==0):
			error_2=0
			
		if(GPIO.input(pos_terminal_3)==1 and error_3==0):
			error_3=1
		elif(GPIO.input(pos_terminal_3)==0):
			error_3=0
			
		if(GPIO.input(pos_terminal_4)==1 and error_4==0):
			error_4=1
		elif(GPIO.input(pos_terminal_4)==0):
			error_4=0
			
		if error_1==1 or error_2==1 or error_3==1 or error_4==1:
			sleep(1)
			fn.sendAlert(error_1,error_2,error_3,error_4)
			error_1=2
			error_2=2
			error_3=2
			error_4=2
		
def close():
	GPIO.cleanup()
	


if __name__ == '__main__':
	setup()
	try:
		run()
	except KeyboardInterrupt: #terminate program with ctrl c
		close()

			
