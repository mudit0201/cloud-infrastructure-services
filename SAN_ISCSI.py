#!/usr/bin/python
import os
import time
import commands
import socket
import thread
def iscsi(ip,port):
	s=socket.socket()
	s.connect((ip,port))
	hd=commands.getoutput("dialog --inputbox 'Enter the HD size (in MB)' 10 30  --stdout")
	s.send(hd)
	os.system("dialog --pause 'connecting to the san-network......' 10 40 5")
	x=s.recv(30)
	if x=="ready" :
		#installing service iscsi-initiator-utils
		if commands.getstatusoutput("rpm -q iscsi-initiator-utils")[0] == 0:
			pass
		else:
			commands.getoutput("yum install iscsi-initiator-utils  &> /dev/null")
		s.send("yo")
		os.system("dialog --pause 'checking basic dependency on your system......' 10 40 5")
		os.system("iscsiadm --mode discoverydb --type sendtargets --portal "+ip+":3260 --discover &>/dev/null")
		b=s.recv(30)
		os.system("iscsiadm --mode node --targetname "+b+"  --portal "+ip+":3260 --login &>/dev/null")
		commands.getoutput("dialog --infobox 'make partitions ,format, and mount ur hard disk' 10 30  --stdout")
		time.sleep(2)
		p=os.system("dialog  --yesno 'do u wish to take more disks' 10 40")
		if p==0:
			s.send("re")
			iscsi(ip,port)
		else:
			s.send("nore")
		'''p=os.system("dialog  --yesno 'do u wish to set up snapshots' 10 40")
		if p==0:
			snap=commands.getoutput("dialog --inputbox 'Enter the size (in MB) of ur snapshot' 10 30  --stdout")
			s.send("snap")'''

	else:
		os.system("dialog --infobox 'technical error try later.....' 10 30 ")
		time.sleep(5)

