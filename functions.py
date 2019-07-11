#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#--Generic functions for working with email addresses and phone numbers--#
	#"Hello"
def addString(given,label,filename):
	strings = given.split(',') #seperate every string added into list
	
	#append file with string
	f = open(filename,'a')
	for i in range(len(strings)):
		f.write(strings[i]+'\n')
	f.close()
	
	#--update displayed list of strings--#
	if(filename=='/home/pi/Alert_System/emails.txt'):
		string_list = getEmailList()
	elif(filename=='/home/pi/Alert_System/phone_numbers.txt'):
		string_list = getPhoneNumbers()
	updateDisplay(label,string_list)

def delString(given,label,filename):
	from time import sleep
	strings = given.split(',') #seperate every string given into list
	
	#--update displayed list of strings--#
	if(filename=='/home/pi/Alert_System/emails.txt'):
		string_list = getEmailList()
	elif(filename=='/home/pi/Alert_System/phone_numbers.txt'):
		string_list = getPhoneNumbers()
	
	length = len(string_list)

	for i in range(len(strings)):
		for j in range(length): 
			if(strings[i]==string_list[j]):
				string_list[j]=' '			#--lazy delete
	
	string_list = filter(lambda x: not x.isspace(),string_list) #--removes blank lines, i.e. deletes		
		
	f = open(filename,'w') 
	for i in range(len(string_list)):
		f.write(string_list[i]+'\n') #--update list
	
	#--update displayed list of strings--#
	updateDisplay(label,string_list)

def updateDisplay(label,string_list):
	
	stringsText = [""]*100
	for i in range(len(string_list)):
		stringsText[i] = string_list[i]
	
	index=0
	for i in range(2): 
		for j in range(4):
			label[index]['text']=stringsText[index] 
			index=index+1


def getAlertMessage(error_list):
	#get location
	with open("/home/pi/Alert_System/location.txt",'r') as file:
		location = file.read()

	error_list_final=[0,0,0,0]
	for i in range(4):
		error_list_final[i] = error_list[i]
		
	for i in range(4):
		if(error_list_final[i]==1 or error_list_final[i]==2):
			if(i==0):
				#get error 1
				with open("/home/pi/Alert_System/error_1.txt",'r') as file:
					error_list_final[0] = file.read()
			elif(i==1):
				#get error 2
				with open("/home/pi/Alert_System/error_2.txt",'r') as file:
					error_list_final[1] = file.read()
			elif(i==2):
				#get error 3
				with open("/home/pi/Alert_System/error_3.txt",'r') as file:
					error_list_final[2] = file.read()
				
			elif(i==3):
				#get error 4
				with open("/home/pi/Alert_System/error_4.txt",'r') as file:
					error_list_final[3] = file.read()
		else:
			error_list_final[i] = "$%gAd.2"
	
	#Make clarfication for pins with no errors
	for i in range(4):
		if(error_list_final[i]=="$%gAd.2"):
			error_list_final[i]="No error."
			
			
	message = "At " + location + " there are the following problems:" + '\n\n' \
			"Error 1: " + error_list_final[0] + '\n\n' + "Error 2: " + error_list_final[1] + '\n\n' \
			"Error 3: " + error_list_final[2] + '\n\n' + "Error 4: " + error_list_final[3]

	return message

def updateFile(string,filename):
	
	file = open(filename,'w')

	file.write(string)

	file.close()
	
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#--Functions for dealing with Phone Numbers and Text Messaging--#

def readBody(file_name):
#--Returns text from specified file--#
	with open(file_name, 'r') as file:
		body = file.read()

	return body

def getPhoneNumbers():
#--Returns list of phone numbers--#
	with open('/home/pi/Alert_System/phone_numbers.txt', 'r') as file:
		phone_numbers = file.readlines()

	#cleaning up the list	
	for i in range(len(phone_numbers)):
		phone_numbers[i] = phone_numbers[i].rstrip('\n')

	while '' in phone_numbers: phone_numbers.remove('')
		
	return phone_numbers

def sendText(error_list):
#--Sends text message using Twilio API--#
#--returns array of 1's if message is successfully sent and an array of 0's if it isn't--#
	import os
	import datetime
	from twilio.rest import Client
	from collections import OrderedDict

	#Account Sid and Auth Token
	account_sid = ""
	auth_token = ""
	client = Client(account_sid, auth_token)

	#phone numbers
	phone_numbers = getPhoneNumbers()

	#current date and time
	now = datetime.datetime.now()

	#sending text
	if phone_numbers:
		for i in range(len(phone_numbers)):

			try:
				message = client.messages \
					.create(
					body= getAlertMessage(error_list),
					from_ = "",
					to=phone_numbers[i]
					)
     		
				return [1,1,1,1]
     		     		
			except:
				f = open('/home/pi/Alert_System/error.txt','a')
				f.write("Cannot send text...."+str(now)+'\n') #--write time of error to text file
				f.close()
				print("Circuit is open. Cannot send text. May be disconnected from WiFi") #--error
				return [0,0,0,0]

	else:
		return [0,0,0,0]
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#--Functions for dealing with emails and emailing.--#

def getSenderInfo():
#--Opens info.txt and returns its important data--#

	f = open('/home/pi/Alert_System/info.txt','r') #--opens file to read
	data = f.readlines()
	f.close()
	return data[0],data[1]#--in format: sender_email, sender_email_password

def sendEmail(error_list):
#--Sends email--#
#--returns array of 1's if message is successfully sent and an array of 0's if it isn't--#

	import smtplib
	import datetime
	
	now = datetime.datetime.now() #--current date and time
	
	sender_email, sender_email_password = getSenderInfo()
	email_list = getEmailList()
	try:
		s = smtplib.SMTP('smtp.gmail.com',587) #--create session: server location, port 
		
		s.starttls() #--tls is for security, blocked otherwise

		s.login(sender_email, sender_email_password)

		message = getEmailMessage(error_list) 

		s.sendmail(sender_email, email_list, message) #--send message
			
		s.close() #--end session
		
		return [1,1,1,1]
	
	except:
		f = open('/home/pi/Alert_System/error.txt','a')
		f.write("Cannot send email...."+str(now)+'\n') #--write time of error to text file
		f.close()
		print("Circuit is open. Cannot send email. May be disconnected from WiFi") #--error
		return [0,0,0,0]
	

def getEmailMessage(error_list):
#--Gets text for email from subject.txt and body.txt and returns it--#

	import email.message as e
	sender_email, sender_email_password = getSenderInfo()
	#receiver_email = getEmailList
	
	#getting subject of email
	with open('/home/pi/Alert_System/subject.txt') as f:
		subject = f.read()
	#getting body of email
	body = getAlertMessage(error_list)
		
	msg = e.Message()
	
	msg['Subject'] = subject
	msg['From'] = sender_email
	msg.set_payload(body)
	
	return msg.as_string()

def getEmailList():	
	#read from file
	f = open('/home/pi/Alert_System/emails.txt','r')
	email_list = f.readlines()
	#remove newline
	for i in range(len(email_list)):
		email_list[i] = email_list[i].rstrip('\n')
	#close file pointer
	f.close()
	
	return email_list
