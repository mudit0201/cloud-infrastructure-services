#!/usr/bin/python
import socket
import os
import commands
import thread
os.system("setenforce 0")
os.system("iptables -F")
i=0
def soc(i):
	socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s=socket.socket()
	port=5445+i #assigning ports for multiple user
	s.bind(("",port))
	print 'port:',port,' activated'
	s.listen(5)
	c,addr=s.accept()
	def p():
		job(i,s,c)
	i+=1
	thread.start_new_thread(p,()) #separate job threads for each client
	thread.start_new_thread(soc(i),()) #starting another port for next client
def job(i,s,c):
	l=[]
	while True:
		a=c.recv(30)
		print a
		l.append(a)
		if l[-1]=="close":
			break
		#checking authentication
		elif l[-1]=="proxy" :
			a=c.recv(30)
			print a
			l.append(a)
			a=c.recv(30)
			print a
			l.append(a)
			if (l[-2]=="viki" and l[-1]=="123"):
				c.send("ok")
			else :
				c.send("retry")

		#STAAS object-storage
		elif l[-1]=="11":
			c,addr=s.accept()
			#starting service nfs
			if commands.getstatusoutput("rpm -q nfs-utils")[0] == 0:
				pass
			else:
				commands.getoutput("yum install nfs-utils -y &> /dev/null")
			#creating logical volume 
			a=c.recv(30)
			d=a
			print a
			x=" /dev/vg/lvnas4 "
			y="/mnt/staas4 "
			c.send(y)
			os.system("lvcreate --size "+a+"M" +" --name lvnas4 vg ") #note:take care on vg lv name
			os.system("mkfs.ext4 "+x)
			os.system("mkdir "+y)
			os.system("mount "+x+y)
			fh=open("/etc/exports","w")
			fh.write("/mnt/staas4 *(rw,no_root_squash)")#note:mount point should be y
			fh.close()
			os.system("chmod 777 "+y)
			os.system("service nfs restart")
			#resize hard disk if user wants'''
			while True:
				a=c.recv(30)
				print a
				if a=="done":
					break
				else :
					if (a[0]=='+') :
						os.system("lvextend --size " + a+"M" + x)
						os.system("resize2fs "+x)
					else:
						d=int(d)+int(a)
						e=str(d)
						os.system("umount "+y)
						os.system("e2fsck -fy "+x)
						os.system("resize2fs "+x+ e+"M")
						os.system("lvreduce  "+x +" --size " + e+"M -fy")
						os.system("mount "+x+y)
						fh=open("/etc/exports","w")
						fh.write("/mnt/staas4 *(rw,no_root_squash)")#note:should be y
						fh.close()
						os.system("chmod 777 "+y)
						os.system("service nfs restart")

		#STAAS block-storage
		elif l[-1]=='12':
			#installing service scsi-target-utils
			if commands.getstatusoutput("rpm -q scsi-target-utils")[0] == 0:
				pass
			else:
				commands.getoutput("yum install scsi-target-utils -y &> /dev/null")
			os.system("service tgtd restart")
			j=20
			def start1(j):
				c,addr=s.accept()
				k=str(j)
				os.system("tgtadm  --lld iscsi --mode target --op  new --tid "+k+ " --targetname mycloudsan"+k)
				#creating hard disk size as per user 
				a=c.recv(30)
				lv="lviscsi"+k
				
				os.system("lvcreate --size " +a+"M" +" --name "+lv+" vg ")
				os.system("mkfs.ext4 /dev/vg/"+lv)
				os.system("tgtadm --lld iscsi --mode logicalunit --op new --lun 1 --tid "+k+" --backing-store /dev/vg/"+lv)
				os.system("tgtadm --lld iscsi --mode target --op bind --tid "+k+" --initiator-address "+addr[0])
				os.system("tgt-admin --dump")
				c.send("ready")
				a=c.recv(30)
				c.send("mycloudsan"+k)
				a=c.recv(30)
				if a=="re":
					j+=1
					start1(j)
				else:
					pass
				
				'''if a=="snap":
					os.system("lvcreate --name lvsnap --size " +a+"M" +"  --snapshot /dev/vg/lvisci ")'''
			start1(j)
		#SAAS....
		elif l[-1]=='2':
			c,addr=s.accept()
			#installing basic softwares
			if commands.getstatusoutput("rpm -q openssh-server")[0] == 0:
				pass
			else:
				commands.getoutput("yum install openssh-server -y &> /dev/null")
			os.system("service sshd restart")
			

		#IAAS....
		elif l[-1]=='3':
			c,addr=s.accept()
			#installing basic softwares
			if commands.getstatusoutput("rpm -q qemu-kvm libvirt virt-manager libvirt-python ")[0] == 0:
				pass
			else:
				commands.getoutput("yum install qemu-kvm libvirt virt-manager libvirt-python -y &> /dev/null")
			os.system("libvirtd restart")
			def start():
				osname=c.recv(100)
				print osname
				ostype=c.recv(100)
				print ostype
				ram=c.recv(100)
				print ram
				cpu=c.recv(100)
				print cpu
				hdsize=c.recv(100)
				print hdsize

				ip=1+i
				ipaddr="192.168.0."+str(ip)
				c.send(ipaddr)
				mac=23+i
				macaddr="52:54:00:00:00:"+str(mac)
				port=5911+i
				vncport=str(port)
				c.send(vncport)
				
				if ostype == "rhel1" :
					p=os.system("/usr/sbin/virt-install --vnc --vncport=" + vncport + " --vnclisten=0.0.0.0  --noautoconsole --name=" + osname + " --ram=" + ram + " --arch=x86_64 --vcpus=" + cpu + "  --os-type=linux --os-variant=" + ostype  + " --hvm --accelerate --disk=/tmp/rhel6new,size=" + hdsize + " -m  " + macaddr  + " --location=/kickstart/rhel6.iso --extra-args='ks=nfs:localhost.localdomain:/share/ks.cfg ip=" +  ipaddr  + " netmask=255.255.255.0 gateway=192.168.0.254 dns=192.168.0.254 noipv6' ")			
					c.send("2")
				
				re=c.recv(30)  
				print re
				if re=="reinstall":
					start()
				cnnct=c.recv(30)
				if cnnct=='rd':
					if commands.getstatusoutput("rpm -q xrdp")[0] == 0:
						pass
					else:
						commands.getoutput("yum install xrdp -y &> /dev/null")
					os.system("service xrdp restart")
					os.system("chkconfig xrdp on")
				else:
					pass
			start()	

		
		else:
			pass
	c.close()
	s.close()
thread.start_new_thread(soc(i),())
while 1:
	pass
