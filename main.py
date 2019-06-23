import functions as fn
import RPi.GPIO as GPIO
from time import sleep


pos_terminal_1 = 40 #--value of physical pin + circuit is connected to for error 1
pos_terminal_2 = 38
pos_terminal_3 = 36
pos_terminal_4 = 32


def setup():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(pos_terminal_1, GPIO.IN,pull_up_down=GPIO.PUD_UP) #posTerminal1 set to input pullup
	GPIO.setup(pos_terminal_2, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pos_terminal_3, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(pos_terminal_4, GPIO.IN,pull_up_down=GPIO.PUD_UP)
	
def checkPins(errors,text_sent,email_sent):
	
		
		if(GPIO.input(pos_terminal_1)==1 and errors[0]==0):
			errors[0]=1
		elif(GPIO.input(pos_terminal_1)==0):
			errors[0]=0
			text_sent[0]=5
			email_sent[0]=5
			
		if(GPIO.input(pos_terminal_2)==1 and errors[1]==0):
			errors[1]=1
		elif(GPIO.input(pos_terminal_2)==0):
			errors[1]=0
			text_sent[1]=5
			email_sent[1]=5
			
		if(GPIO.input(pos_terminal_3)==1 and errors[2]==0):
			errors[2]=1
		elif(GPIO.input(pos_terminal_3)==0):
			errors[2]=0
			text_sent[2]=5
			email_sent[2]=5
			 
		if(GPIO.input(pos_terminal_4)==1 and errors[3]==0):
			errors[3]=1
		elif(GPIO.input(pos_terminal_4)==0):
			errors[3]=0
			text_sent[3]=5
			email_sent[3]=5
			
		return errors,text_sent,email_sent

def run():
	
	error_text=[0,0,0,0]	#0 is no error, 1 is error, 2 is error already detected
	error_email=[0,0,0,0]
	text_sent=[0,0,0,0]		#5 is no text sent yet, 1 is text successfully sent, 0 is text failed to send except for first run
	email_sent=[0,0,0,0]
	 
	while True:
		
		error_text,text_sent,email_sent = checkPins(error_text,text_sent,email_sent)
		error_email,text_sent,email_sent = checkPins(error_email,text_sent,email_sent)
		
		if 1 in error_text or 0 in text_sent:
			sleep(1)
			text_sent=fn.sendText(error_text)
			if(text_sent==0):
			for i in range(4):
				error_text[i] = 2
				
		if 1 in error_email or 0 in email_sent:
			sleep(1)
			email_sent=fn.sendEmail(error_email)
			for i in range(4):
				error_email[i] = 2
		
def close():
	GPIO.cleanup()
	


if __name__ == '__main__':
	setup()
	try:
		run()
	except KeyboardInterrupt: #terminate program with ctrl c
		close()

			
