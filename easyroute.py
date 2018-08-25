#!/usr/bin/env python

from netmiko import ConnectHandler
from netaddr import *
import getpass

iosv_l3 = {
   'device_type': 'cisco_ios',
   'ip': raw_input("enter the ip address: "),
   'username': raw_input("enter the username: "),
   'password': getpass.getpass("enter the vty password: "),
	}

print "+##############################################################+"
print "|                  routing configuration                       |"
print "+##############################################################+"

print "choisir le protocole de routage\n"
print 	"  1- rip version 1"
print   "  2- rip version 2"
print	"  3- ospf"
print	"  4- eigrp (pour les peripherique cisco)"
print   "  5- route statique "
print   "  6- back up \n"
choix= input("entrez votre protocole: ")
print "\n"
## fonction  connectio n et protocole
def route(devices):
         ##possible routes
	 net_connect = ConnectHandler(**devices)
         output = net_connect.send_command('show ip route')
	 f =open("route","w")
         f.write(output)
         f.close()
	 print " ****les routes possibles**** \n" 
	 s="/"
	 k="C"
	 f=open("route","r")
	 lines =f.readlines()
	 c=0
	 ligne=0
	 routes=""
	 for a in lines:
   	   if s in a:	     
            if k in a:  
              ligne=ligne+1
	      print "   "+str(ligne)+"-"+lines[c].split()[1]
	      routes+=lines[c].split()[1]+"\n"
           c=c+1
	 f.close()

         f =open("route","w")
         f.write(routes)
         f.close()

	 f =open("route","r")
	 lines =f.readlines()
	 f.close()
	 print "\n"
#rip version 1 configuration  function 
def rip(devices):
    print " rip version 1 configuration \n"
    print  " configuring ...  \n"
    net_connect = ConnectHandler(**devices)
    f =open("route","r")
    lines =f.readlines()
    f.close()
    for i in range(len(lines)):
      print "network "+lines[i][:-4]+"\n"
      config_commands = ['router rip','no auto-summary','network '+lines[i][:-4]]
      net_connect.send_config_set(config_commands)
    stat=raw_input("voulez vous redistribuer les routes statiques via RIP yes/no")
    if stat=="yes" or stat=="oui" or stat=="y" or stat=="o":
      config_commands = ['router rip','redistribute static']
      net_connect.send_config_set(config_commands)
    else:
       print ""

    de=raw_input("ajouter une route par defaut yes or no ")
    if de=="yes" or de=="oui" or de=="y" or de=="o":
         gw=raw_input("entrez ip next hope")
         config_commands = ['ip default-network'+str(gw),'router rip','redistribute static']
         net_connect.send_config_set(config_commands)
    else:
       print ""
    output=net_connect.send_command('sh run | s rip')
    print output 
#rip version 2 basic configuration 
def rip2(devices):
    print " rip version 1 configuration \n"
    print  " configuring ...  \n"
    net_connect = ConnectHandler(**devices)
    f =open("route","r")
    lines =f.readlines()
    f.close()
    for i in range(len(lines)):
      print "network "+lines[i][:-4]+"\n"
      config_commands = ['router rip','version 2','no auto-summary','network '+lines[i][:-4]]
      net_connect.send_config_set(config_commands)
    
    stat=raw_input("voulez vous redistribuer les routes statiques via RIP version 2 yes/no")
    if stat=="yes" or stat=="oui" or stat=="y" or stat=="o":
        config_commands = ['router rip','redistribute static']
        net_connect.send_config_set(config_commands)
    else:
        print ""

    de=raw_input("ajouter une route par defaut yes or no ")
    if de=="yes" or de=="oui" or de=="y" or de=="o":
         gw=raw_input("entrez ip next hope")
         config_commands = ['ip default-network'+str(gw),'router rip','redistribute static']
         net_connect.send_config_set(config_commands)
    else:
        print ""
    output=net_connect.send_command('sh run | s rip')
    print output

#eigrp basic configuation
def eigrp(devices):
    print " eigrp configuration \n"
    print  "     configuring ...  \n"
    net_connect = ConnectHandler(**devices)
    f =open("route","r")
    lines =f.readlines()
    f.close()
    SA=input(" entrez le numero ( 1 - 65535 ) du systme-autonome  ")
    for i in range(len(lines)):
      print " configuring network "+lines[i].rstrip('\n')+"\n"
      ip=IPNetwork(lines[i].rstrip('\n'))
      h=ip.hostmask
      k=ip.ip
      adress = "network "+ str(k) + " " + str(h)
      config_commands = ['router eigrp ' +str(SA),'no auto-summary',adress]
      net_connect.send_config_set(config_commands)
    
    stat=raw_input("voulez vous redistribuer les routes statiques via EIGRP yes/no")
    if stat=="yes" or stat=="oui" or stat=="y" or stat=="o":
        config_commands = ['router eigrp ' +str(SA),'redistribute static']
        net_connect.send_config_set(config_commands)
    else:
        print ""

    de=raw_input("ajouter une route par defaut yes or no ")
    if de=="yes" or de=="oui" or de=="y" or de=="o":
         gw=raw_input("entrez ip next hope")
         config_commands = ['ip route 0.0.0.0 0.0.0.0'+str(gw),'router eigrp ' +str(SA),'redistribute static']
         net_connect.send_config_set(config_commands)
    else:
        print ""

    output=net_connect.send_command('sh run|s eigrp')
    print output

#ospf basic confguration
def ospf(devices):
    print " ospf configuration \n"
    net_connect = ConnectHandler(**devices)
    f =open("route","r")
    lines =f.readlines()
    f.close()
    zone=input(" entrez le numero de la zone ospf   ")
    SA=input(" entrez le numero ( 1 - 65535 ) du systme-autonome  ")
    for i in range(len(lines)):
      print " configuring network "+lines[i].rstrip('\n')+"\n"
      ip=IPNetwork(lines[i].rstrip('\n'))
      h=ip.hostmask
      k=ip.ip
      adress = "network "+ str(k) + " " + str(h) +" area " + str(zone)
      config_commands = ['router ospf '+str(SA),'no auto-summary',adress]
      net_connect.send_config_set(config_commands)
    stat=raw_input("voulez vous redistribuer les routes statiques via OSPF yes or no")
    if stat=="yes" or stat=="oui" or stat=="y" or stat=="o":
        config_commands = ['router ospf '+str(SA),'redistribute static']
        net_connect.send_config_set(config_commands)
    else:
        print ""

    de=raw_input("ajouter une route par defaut yes or no ")
    if de=="yes" or de=="oui" or de=="y" or de=="o":
         gw=raw_input("entrez ip next hope")
         config_commands = ['ip route 0.0.0.0 0.0.0.0'+str(gw),'router ospf '+str(SA),'redistribute static']
         net_connect.send_config_set(config_commands)
    else:
        print ""

    output=net_connect.send_command('sh run | s ospf ')
    print output 
#static route configuration 
def static(devices):
    print " configuration static route \n"
    net_connect = ConnectHandler(**devices)
    add=raw_input("entrez address ip sous la forme A.B.C.D/Mask: ")
    ip=IPNetwork(add.rstrip('\n'))
    h=ip.netmask
    k=ip.ip
    GW= raw_input("entrez address ip de la gateway: ")
    adress = "ip route " +str(k) + " " +str(h) + "  " + str(GW)
    config_commands = [adress]
    net_connect.send_config_set(config_commands)
    output=net_connect.send_command('sh ip route')
    print output

def backup(devices):
        net_connect = ConnectHandler(**devices)
	#net_connect.find_prompt()
	print "#####################################################################"
	print "#               backauping " +devices.get("ip")+ " configuration  \#"
	print "#####################################################################"

	output = net_connect.send_command('sh run')
	file=open(devices.get("ip")+ "_backup.txt",'w')
	file.write(output)
	file.close()

#first connection function
def connect(devices,protocole):
	print "connecting to "+iosv_l3.get("ip")+"...\n"
	net_connect = ConnectHandler(**devices)
	if protocole==1:
	   print "we are going to configure rip version 1 \n "
           route(devices)
	   rip(devices)
	elif protocole==2:
	   print "we are going to configure rip version 2 \n "
           route(devices)
           rip2(devices)
	elif protocole==3:
	   print "we are going to configure ospf \n "
           route(devices)
           ospf(devices)
	elif protocole==4:
           print "we are going to configure eigrp \n "
	   route(devices)
           eigrp(devices)
	elif protocole==5:
           print "we are going to configure static route \n "
           static(devices)
        elif protocole==6:
           backup(devices)
        else:
	   print "no protocole defined"
	print "\n"

connect(iosv_l3,choix)

