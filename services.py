#!/usr/bin/python
import os
import time
import socket
import commands
try:
	def serv():
		ser=commands.getoutput("dialog --menu 'What kind of service you are looking for' 20 50 4  1 'Storage As A Service' 2 'Software As A Service' 3 'IAAS' 4 'PAAS'  --stdout ")
		if int(ser) == 1:
			os.system("dialog  --infobox 'welcome to the storage services' 10 40")
			time.sleep(2)
			a=commands.getoutput("dialog --menu 'advanced options' 20 50 2 1 'NAS(Object storage)' 2 'SAN(block storage)'  --stdout")
			if int(a)==1 :
				#nas
				return "11"
			else :
				#iscsi
				return "12"
		else:
			return ser
except IOError:
	os.system("dialog --infobox '.....Invalid choice.....' 10 40")
	time.sleep(1)
except ValueError:
	os.system("dialog --infobox '.....Invalid choice.....' 10 40")
	time.sleep(1)
