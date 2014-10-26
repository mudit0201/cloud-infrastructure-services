#!/usr/bin/python
import socket
import os
import time
import services
import SAAS
import NAS_nfs
import SAN_ISCSI
import IAAS
import commands
socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s=socket.socket()
if commands.getstatusoutput("rpm -q dialog")[0] == 0:
	pass
else:
	commands.getoutput("yum install dialog -y &> /dev/null")
try:
	def proxy():
		ip=commands.getoutput("dialog --inputbox  'Enter the IP you wanna connect' 10 40  --stdout")
		port=commands.getoutput("dialog  --inputbox 'Enter the port you wanna connect to' 10 40  --stdout")
		os.system("dialog --pause 'connecting to the server......' 10 40 5")

		#can check how many wrong time user has entered by len(l)/2
		if (int(port) ==5445):
			s.connect((ip,int(port)))
			os.system("dialog --infobox 'Authentication Required ......' 10 40 ")
			time.sleep(1)
			def log():
				s.send("proxy")
				user=commands.getoutput("dialog  --inputbox 'Enter Username' 10 40  --stdout")
				s.send(user)

				pas=commands.getoutput("dialog  --inputbox 'Enter Password' 10 40  --stdout")
				s.send(pas)
				b=s.recv(20)
				if b=="ok":
					os.system("dialog --infobox 'successfully logged in......' 10 30 ")
					time.sleep(2)
					#importing service file and taking what service user wants
					x=services.serv()
					s.send(x)
					os.system("dialog --infobox 'connecting to your service......' 10 30 ")
					time.sleep(5)
					if x=='11' :
						NAS_nfs.nas(ip,int(port))
					elif x=='12':		
						SAN_ISCSI.iscsi(ip,int(port))
					elif x=='2':		
						SAAS.saas(ip,int(port))
					elif x=='3':		
						IAAS.prox(ip,int(port))
					elif x=='4':		
						os.system("dialog --infobox 'oh very trivial thing not taught......' 10 30 ")
						time.sleep(5)
					
				#incorrect login retry
				elif b=="retry":
					os.system("dialog --infobox 'Incorrect username or password......' 10 30 ")
					time.sleep(2)
					p=os.system("dialog  --yesno 'Wanna try again..??' 10 40")
					if p==0 :
						log()
					else:
						s.send("close")
						os.system("dialog --infobox 'you are logged out......' 20 20 ")
						time.sleep(2)
						s.close()
						os.system("exit")
			log()
		else:
			os.system("dialog --infobox 'Incorrect ip or port address ......' 20 20 ")
			time.sleep(2)
			proxy()
	proxy()
except socket.error:
	os.system("dialog --infobox '.....Invalid choice.....' 10 40")
	time.sleep(1)
finally:
	os.system("dialog --infobox '.....Hope you enjoyed our services.....' 10 40")
	time.sleep(1)
