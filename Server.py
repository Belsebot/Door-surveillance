import socket

serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
serversocket.bind(('192.168.0.100',10000))
serversocket.listen(5)

try:
	print "Waiting connection"
	while True:							#loop
		connection, address = serversocket.accept()
		buf = connection.recv(1024)				
		if len(buf) > 0:					#getting message from client
			print 'Connected by:',address[0],buf		#printing address and message to screen

except KeyboardInterrupt:
	print "Serveri sammutetaan"
	serversocket.close()

print "Serveri sammui"
