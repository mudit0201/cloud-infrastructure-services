#!/usr/bin/python
import os
import time
import commands
import socket
def nas(ip,port):
	s=socket.socket()
	s.connect((ip,port))
	os.system("dialog --textbox 'terms and conditions apply '/root/Desktop/muditproject/t 60 60  --sleep 3")
	hd=commands.getoutput("dialog --inputbox 'Enter the HD size (in MB)' 10 30  --stdout")
	s.send(hd)
	os.system("dialog --pause 'installing basic dependencies......' 10 40 30")
	name=commands.getoutput("dialog --inputbox 'Enter the name of ur hard disk' 10 30  --stdout")
	os.system("mkdir /media/"+name)
	b=s.recv(20)
	os.system("mount "+ip+":"+b +" /media/"+name)
	while True:
		rhd=commands.getoutput("dialog --menu 'Advanced options' 20 50 2  1 'wanna resize' 2 'need no more or less' --stdout")

		if rhd=="1" :
			hd_re=commands.getoutput("dialog --inputbox 'Enter the size wanna add/sub(in + or- MB)' 10 30  --stdout")
			s.send(hd_re)
			os.system("dialog --pause 'resizing your hard disk......' 10 40 50")
			
		else:
			s.send("done")
			os.system("dialog --infobox '...your hard disk size has been fixed successfully...' 10 30 ")
			time.sleep(2)
			os.system("dialog --timebox '...your validity will expire in...' 10 30  10 30 20 ")
			time.sleep(2)
			break



