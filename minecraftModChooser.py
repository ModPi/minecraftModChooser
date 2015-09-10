import mcpi.minecraft as minecraft
import mcpi.block as block
import getkeypress as keyboard
import time
import os

def printWelcome():
  mc = minecraft.Minecraft.create() #connect to minecraft instance
  mc.postToChat("Mods detected!")
  mc.postToChat("Press 'r' to relist your mods.")
  mc.postToChat("Press 'q' to stop running all mods.")
  mc.postToChat("Press 'm' to show these instructions again.")
  mc.postToChat("Loading mods in 3..")
  time.sleep(1)
  mc.postToChat("2..")
  time.sleep(1)
  mc.postToChat("1..")
  time.sleep(1)


def printMenu():
  mc = minecraft.Minecraft.create() #connect to minecraft instance
  mc.postToChat("Press 'r' to relist your mods.")
  mc.postToChat("Press 'q' to stop running all mods.")
  mc.postToChat("Press 'F11' to make some mods!")

def printMods():
  mc = minecraft.Minecraft.create() #connect to minecraft instance
  pathPrefix = "/home/pi/userMods/"
  f2 = os.popen("ls /home/pi/userMods/*.txt")
  pyPaths = f2.read()
  pyPathsFormatted = pyPaths.replace(" ", "\ ")#format spaces for later execution
  pyPathsList = pyPathsFormatted.split("\n")#get a list of all absolute paths to mods for later execution
  pyMods = pyPaths.replace(pathPrefix, "")  #remove path from mods
  pyNames = pyMods.replace(".txt", "") #remove .py from the names
  pyNamesList = pyNames.split("\n");
  numOfMods = len(pyNamesList) - 1
  #list all the mods
  count = 0
  for name in pyNamesList:
    count = count + 1
    if name != "" and count < 10:
      mc.postToChat("Press " + "F" + str(count) + " for " + name)
    if count == 10:
      mc.postToChat("Not showing more than first 9 mods")

def printError():
  mc = minecraft.Minecraft.create() #connect to minecraft instance
  mc.postToChat("There was an error running your mod!")

#pyPaths - string containing absolute path to mods separated by \n
#pyMods  - string containing mod names separated by \n
#pyNames - string containing names of mods without the .py extension, sep by \n
mc = minecraft.Minecraft.create() #connect to minecraft instance

#boolean for which mode
minecraftWindow = True

#print Welcome Message
######################
printWelcome()

# to be iterated through earlier to see which mod should be run
modKeys = ['<F1>', '<F2>', '<F3>','<F4>', '<F5>', '<F6>', '<F7>', '<F8>', '<F9>']
pathPrefix = "/home/pi/userMods/"

f2 = os.popen("ls /home/pi/userMods/*.txt")
pyPaths = f2.read()

pyPathsFormatted = pyPaths.replace(" ", "\ ")#format spaces for later execution
pyPathsList = pyPathsFormatted.split("\n")#get a list of all absolute paths to mods for later execution

pyMods = pyPaths.replace(pathPrefix, "")  #remove path from mods
pyNames = pyMods.replace(".txt", "") #remove .py from the names


count = 0
pyNamesList = pyNames.split("\n");
numOfMods = len(pyNamesList) - 1

for name in pyNamesList:
  count = count + 1
  if name != "" and count < 10:
    mc.postToChat("Press " + "F" + str(count) + " for " + name)
  if count == 10:
    mc.postToChat("Not showing more than first 9 mods")


error = 0
while True:
  key = keyboard.getkeypress()
  #wait for key to be pressed
  while key != '<F1>' and key != '<F2>' and key != '<F3>' and key != '<F4>' and key != '<F5>' \
      and key != '<F6>' and key != '<F7>' and key != '<F8>' and key != '<F9>' and key != 'q' and key != 'r' and key != 'm' and key != '<F11>':
        key = keyboard.getkeypress()


  #the following nine conditionals in loop handle the mod selection choice by the user, in case of continuously running scripts,
  #there is a check to ensure the mod isn't already being run before execution
  for i in range(0,9):
    if key == modKeys[i]:
      #get current mod list
      f2 = os.popen("ls /home/pi/userMods/*.txt")
      pyPaths = f2.read()
      pyPathsFormatted = pyPaths.replace(" ", "\ ")#format spaces for later execution
      pyPathsList = pyPathsFormatted.split("\n")#get a list of all absolute paths to mods for later execution
      pyMods = pyPaths.replace(pathPrefix, "")  #remove path from mods
      pyNames = pyMods.replace(".txt", "") #remove .py from the names
      count = 0
      pyNamesList = pyNames.split("\n");
      numOfMods = len(pyNamesList) - 1
      #end get current mod list

      processID = os.popen("ps -elaf | grep -m 1 \"" + pyPathsList[i] + "\" | grep -v 'grep' | cut -c 15-18") #get PID
      PID = processID.read().split('\n')[0]
      if PID == '': #if the script isn't being run
        error = os.system("python " + pyPathsList[i] + " &")

  if key == 'm':
    #print menu
    printMenu()

  if key == 'r':
    #reprint mods
    printMods()

  if key == 'q':
    #quit all running mods
    for path in pyPathsList:
      if path != "":
        processID = os.popen("ps -elaf | grep -m 1 \"" + path + "\" | cut -c 15-18") #get PID
        PID = processID.read().split('\n')[0]
        if PID != '':
          os.system("kill " + PID)

  if key == '<F11>':
    print "F11 pressed"
    if minecraftWindow is True:
      os.system("su pi -c '/home/pi/configScripts/toggleBlockly.sh'")
      minecraftWindow = False
    else:
      os.system("su pi -c '/home/pi/configScripts/toggleMinecraft.sh'")
      minecraftWindow = True


  if error != 0:
    printError()
    error = 0

