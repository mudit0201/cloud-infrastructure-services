#!/usr/bin/python
import os
import time
import commands
import socket
import thread
def prox(ip,port):
	s=socket.socket()
	s.connect((ip,port))
	osname=commands.getoutput("dialog --menu 'select ur os' 20 50 4  1 'Red Hat' 2 'Fedora' 3 'Back Track' 4 'ubuntu' --stdout")
	if osname=='1':
		s.send("Red Hat")
		ostype=commands.getoutput("dialog --menu 'select the version u want' 20 50 3  1 'rhel6' 2 'rhel5' 3 'rhel4' --stdout")
		s.send("rhel"+ostype)
	if osname=='2':
		s.send("Fedora")
		ostype=commands.getoutput("dialog --menu 'select the version u want' 20 50 3  1 'fed14' 2 'fed15' 3 'fed16' --stdout")
		s.send("fed"+ostype)

	ram=commands.getoutput("dialog --inputbox 'Enter ram size (MB)' 10 30  --stdout")
	s.send(ram)


	cpu=commands.getoutput("dialog --inputbox 'Enter cpu core' 10 30  --stdout")
	s.send(cpu)


	hdsize=commands.getoutput("dialog --inputbox 'Enter HD size (GB)' 10 30  --stdout")
	s.send(hdsize)
	ipaddr=s.recv(11)
	p=os.system("dialog  --yesno 'Wanna connect to live installation' 10 40")
	vncp=s.recv(4)
	if p==0:
		os.system("vncviewer "+ip+":"+vncp)
	else :
		pass
	b=s.recv(30)
	if b=="2":
		s.send("fine")
		os.system("dialog --infobox 'os has been successfully installed......' 10 30 ")
		time.sleep(5)
	else :
		os.system("dialog --infobox 'sorry your requested configuration had some technical issues......' 10 30 ")
		time.sleep(5)
		p=os.system("dialog  --yesno 'do u wish to install again' 10 40")
		if p==0:
			s.send("reinstall")
			prox(ip,port)
		else:
			s.send("fine")

	cnnct=commands.getoutput("dialog --menu 'what protocol u would like to choose to connect to ur pc' 20 50 3 1 'SSH' 2 'RDP' 3 'VNC' --stdout")
	if cnnct=='1':
		key=commands.getoutput("dialog --menu 'ssh-key option' 20 50 2 1 'import key' 2 'wanna upload ur own' --stdout")
		if key=='1':
			s.send("key")
			b=s.recv(30)
		else:
			pass

	elif cnnct=='2':
		s.send("rd")
		os.system("dialog --pause 'checking basic dependency on your system......' 10 40 5")
		if commands.getstatusoutput("rpm -q rdesktop")[0] == 0:
				pass
		else:
			commands.getoutput("yum install rdesktop -y &> /dev/null")
		
		os.system("rdesktop "+ipaddr)
	else:
		s.send("fine")
		os.system("vncviewer "+ipaddr+":"+vncp)
	while True:
		adv=commands.getoutput("dialog --menu 'advanced options' 20 50 4 1 'Add volume' 2 'security add' 3 'create another instance' 4 'none go' --stdout")
		if adv=='1':
			os.system("dialog  --infobox 'welcome to the storage services' 10 40")
			time.sleep(2)
			a=commands.getoutput("dialog --menu 'advanced options' 20 50 2 1 'NAS(Object storage)' 2 'SAN(block storage)'  --stdout")
			if int(a)==1 :
				s.send("11")
				import NAS_nfs
				NAS_nfs.nas(ip,port)
			else :
				s.send("12")
				import SAN_ISCSI
				SAN_ISCSI.iscsi(ip,port)
			continue

		elif adv=='2':
			hd=commands.getoutput("dialog --inputbox 'Enter the name of ur security group' 10 30  --stdout")
			sec=commands.getoutput("dialog --menu 'which security u wanna employ' 20 50 3 1 'ssh' 2 'telnet' 3 'icmp' 4 'ftp' --stdout")
			if sec=='1':
				os.system("iptables -I INPUT -p tcp --dport 22 -j REJECT")
			elif sec=='2':
				os.system("iptables -I INPUT -p tcp --dport 23 -j REJECT")
			elif sec=='3':
				os.system("iptables -I INPUT -p icmp -j DROP")
			else:
				os.system("iptables -I INPUT -p tcp --dport 21 -j REJECT")
			continue
		elif adv=='3':
			s.send("3")
			prox(ip,port)
		else:
			break









