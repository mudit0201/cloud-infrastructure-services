#!/usr/bin/python
import os
import time
import commands
import socket
def saas(ip,port):
	s=socket.socket()
	s.connect((ip,port))
	os.system("dialog --infobox '...welcome to the software services...' 10 30 ")
	time.sleep(2)
	if commands.getstatusoutput("rpm -q openssh-clients")[0] == 0:
		pass
	else:
		commands.getoutput("yum install openssh-clients -y &> /dev/null")
	while True:
		soft=commands.getoutput("dialog --inputbox 'Enter the service you are looking for' 10 30  --stdout")
		os.system("ssh -X -l "+ip+" "+soft)
		p=os.system("dialog  --yesno 'want any other service..??' 10 40")
		if p=='0':
			continue
		else :
			break

