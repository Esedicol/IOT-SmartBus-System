import time
import nexmo
import datetime
import os
import bluetooth

from tinydb import TinyDB, Query
db = TinyDB('iot.json')
query = Query
max = TinyDB('count.json')

foundAddr = [] 
curr = datetime.datetime.now()


#Comapare bluetooth address of device found to the pre-stored address in database
def comapare(foundAddr):
	#clear the console
	os.system('clear')
	print ('''
		============================================
			   Presence Detection
		============================================
		  ''')

	#prints current Time
	print("\t\t\t[ Current Time: ", curr.hour,"hr",  " : " , curr.minute,"min", " : ", curr.second, "sec ]\n\n\n\n")
	
	#access the databse 
	for i in db.all():
		#assign x to the address
		x = i['addr']

		#compare x into the found address in the bluetooth detection
		if x in foundAddr:
			#get name
			name = i['name']

			#print that 'name' is on the bus
			print ("-> [ ",name , " is on the Bus ]\n")

	#this is just a 5 sec delay before the system send messages
	for x in range(0, 10):
		time.sleep(.1)


	print("\n\t< -------------------  Seding message ..... ------------------- >\n\n")

	#another delay so it doesnt happen to fast and the viewer will have a chance to read output
	for x in range(0, 10):
		time.sleep(.5)

	#access databse
	for i in db.all():
		x = i['addr']

		#if the registered account are not found during detection
		if x not in foundAddr:
			name = i['name']
			no = i['no']

			#send alert messages
			sendMessage(no, name)
			
			
#send message to those who are missing on the bus
def sendMessage(sendTo, name):

	#get acces to nexmo using your own credentials
	c = nexmo.Client(key='4179aed7', secret='B6ED8JS3Kap5bIsI')
	c.send_message({
			#you can customize what the reciver will see when they receive the text message
		    'from': 'Nexmo',
		    #the number u want to send the message to
		    'to': str(sendTo),
		    #text message output
		    'text': '%s missed the bus on (%d/%d/%d.)' % (name, curr.month, curr.day, curr.year)
		})

	#print on console balance
	print ("--> [ ",name, " not Present! ...... ]\n--> [  Message sent --- Current Balance : ", c.get_balance()['value'] ,"]\n")


#main method
def main():
	os.system('clear')

	#delay
	for x in range(0, 5):
		time.sleep(.5)
	print ('''
		============================================
			 Parental Monitor Application
		============================================
		  ''')

	print("\n\t< -------------------  Detecting ..... ------------------- >\n")
	#delay
	for x in range(0, 5):
		time.sleep(.5)

	#method for detecting bluetooth devices
	nearby_devices = bluetooth.discover_devices(lookup_names=True)
	#print number of deviced found using len() method
	print("\n--> Number of devices found [ %d ]\n" % len(nearby_devices))

	#retrieve name and addrress of the devices found
	for addr, name in nearby_devices:
		#print name and addr on screen for viewer to see
		print("--> [ Device Name : ",name," ]\n--> [ Bluetooth Address : ", addr, " ]\n\n")
		#add only the address in the array
		foundAddr.append(addr)

	#another delay
	for x in range(0, 11):
		time.sleep(1)

	# check for the last time for any incoming children before closing door
	print("\n\n--> Last check if theres more children to get in the bus")
	lastCheck = bluetooth.discover_devices(lookup_names=True)

	#compare the length of last detection to the array of found address in the first detection
	if(len(lastCheck) > len(foundAddr)):
		#calculate length of the newly found addresses 
		found = len(lastCheck) - len(foundAddr)
		#print number of child found in the last chack
		print("\n --> ", found, " Child found!....")

		#another delay
		for x in range(0, 11):
			time.sleep(1)

		#clear screen
		os.system('clear')
		print("\t<-- Listing All Devices -->\n\n")

		#empty foundAddr array to avoid duplication
		foundAddr.clear()
		#retrive the address and name in the last detection
		for addr, name in lastCheck:
			print("--> [ Device Name : ",name," ]\n--> [ Bluetooth Address : ", addr, " ]\n\n")
			#add newly found address
			foundAddr.append(addr)

	#countdown of 10 s for the bus to close
	for x in range(0, 11):
		time.sleep(.5)
		print ("	Bus Closing in => ", (10 - x ))

	print("\n <---------  BUS CLOSED ---------> ")

	
	comapare(foundAddr)
	for x in range(0,11):
		time.sleep(1)

	countemptySeat(foundAddr)

def countemptySeat(foundAddr):
	os.system('clear')
	print ('''
		============================================
			Number of Available Seats
		============================================
		  ''')
	
	numberOfPeople = len(foundAddr)
	
	for i in max.all():
		count = i['seats']
		x = count - numberOfPeople
		print("\t\tNumber of Available seats in the Bus : [", x, "]\n\n\n\n\n\n\n")
		max.purge()
		max.insert({'seats' : x})

main()


































