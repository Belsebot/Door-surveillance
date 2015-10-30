import RPi.GPIO as GPIO
import datetime
import time
import socket

host = '192.168.0.100' # server address
port = 10000          # server port

def send_server(str):
	clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		clientsocket.connect((host,port))
		clientsocket.send(str)
	except Exception,e:
		print 'connection failed'

	clientsocket.close()
	return

log = open('ovivalvonta.log','a')	# Open log file where to write
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 18           # raspberry gpio port
check = 0

GPIO.setup(button, GPIO.IN, GPIO.PUD_UP)

def my_callback(channel):
	global check
	now = datetime.datetime.now()
	if GPIO.input(button):		#When door opens 
		print "Ovi aukesi",now.strftime("%d-%m-%Y"),"Kello:",now.strftime("%H:%M") # print date and time on the screen when door opens
		ovi = 'Ovi aukesi:'+ now.strftime("%d-%m-%Y %H:%M")
		send_server(ovi)					#send date and time to server
		log.write('Ovi aukesi ')				#writes door opens to log file
		log.write(now.strftime("%d-%m-%Y %H:%M"))		#writes time to log file
		log.write('\n')
		check = 1

	else:				#when door closes
		if check == 1:
			print "Ovi meni kiinni",now.strftime("%d-%m-%Y"),"Kello:",now.strftime("%H:%M") #print date and time on the screen when door closes
			ovi = 'Ovi meni kiinni:'+ now.strftime("%d-%m-%Y %H:%M")
			send_server(ovi)				#send date and time to server
			log.write('Ovi meni kiinni ')			#writes door closes to log file
			log.write(now.strftime("%d-%m-%Y %H:%M"))	#writes time to log file
			log.write('\n')
			check = 0
			log.flush()					#saves log file

GPIO.add_event_detect(button,GPIO.BOTH,callback=my_callback)		#add event detection to raspberry gpio port

print "Paina CTRL+C lopettaaksesi"
now = datetime.datetime.now()						
ovi = 'Ovenvalvonta ohjelma kaynnistettiin:'+ now.strftime("%d-%m-%Y %H:%M")
send_server(ovi)
try:									#Loop
	print "Waiting keypress"
	while True:
		time.sleep(0.5)

except KeyboardInterrupt:
	GPIO.cleanup()

print "Ohjelma lopetetaan"
now = datetime.datetime.now()
ovi = 'Ovenvalvonta ohjelma lopetettiin:'+ now.strftime("%d-%m-%Y %H:%M") #send message to server that program is closed
send_server(ovi)
GPIO.cleanup()
log.close()
