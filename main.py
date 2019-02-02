##pip3 install urllib3 colorama requests wmi pywin32 

#import urllib3
#urllib3.disable_warnings()

#import requests
#import json
import sys
import wmi
import winreg
import socket

from colorama import init as coloramainit
from colorama import Fore, Back, Style
coloramainit()
"""
Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
Style: DIM, NORMAL, BRIGHT, RESET_ALL
"""

class LoLDirectory(object):
  LolDir = None #It's defined - less bugs
  try: #First check Windows Registry
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Riot Games, Inc\League of Legends")
    LolDir = winreg.QueryValueEx(key, "Location")[0] #We need only first value from array
  except:
    print("League of Legends not found in registry! Trying to find info in process")
    try:
      Found = False
      for process in wmi.WMI().Win32_Process (name="LeagueClient.exe"):
        print("Process found! Trying to get it's path")
        if process.ExecutablePath:
          LolDir = process.ExecutablePath
          LolDir = LolDir.rsplit('\\', 7)[0] #remove file name from directory and move to main folder
          Found = True
        else:
          print("Cannot access process path information! (Launcher was probably launched as administrator or) ")
      if Found is False:
        print("Program is probably not launched")
    except:
      print("It didn't work. Asking user...")
  if LolDir is None:
    ##Ask user about dir, temporaly using hardcoded value
    LolDir = 'C:/Program Files/Riot Games/League of Legends'

  LolDir = LolDir.replace('\\', '/') #Linux-like slashes rulez!

class Credentials(object):
  Port = None
  Pass = None
  try:
    lockfile = open(LoLDirectory.LolDir + "/lockfile", "r") #Open 'lockfile' inside LoL Directory as read-only

    for line in lockfile: 
        fields = line.split(":")    #Split fields seperated by ":" in lockfile to array
        Port = fields[2]            #Port number is 3rd information in lockfile
        Pass = fields[3]            #and Password is 4th

    lockfile.close()                #Make memory FREE! :D 
  except(FileNotFoundError):
    print("File not Found! Launcher is not opened or can't access it's lockfile (maybe directory is wrong?) ")


if (Credentials.Port is None) or (Credentials.Pass is None):
    print(Fore.RED + "Cannot find informations about connection to League of Legends Launcher. Exiting..." + Fore.RESET)
    sys.exit()

print("Port: " + Credentials.Port)
print("Password: "+ Credentials.Pass)
   
print("Your Computer Name is: " + socket.gethostname())    
print("Your Computer IP Address is: " + socket.gethostbyname(socket.gethostname()))    



# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = "0.0.0.0"
port = 25565                                          

# bind to the port
serversocket.bind((host, port))                                  

# queue up to 5 requests
serversocket.listen(5)                                           


# establish a connection
clientsocket,addr = serversocket.accept()      

print("Credientals send to %s" % str(addr))

msg = Credentials.Port + "\r\n" + Credentials.Pass
clientsocket.send(msg.encode('ascii'))
clientsocket.close()