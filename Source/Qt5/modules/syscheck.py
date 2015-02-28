#!/usr/bin/python
# -*- coding: utf-8 -*-

#Load modules
try:
	import imp
	import sys
	import os
	import time
	import prefcheck
	import gui
	#import update
	
	import json
except ImportError:
	raise Exception("Error: Faild to import critical modules.")
	sys.exit(1)


def sysCheck():
	#start writing to sysCheck.log
	unlog = sys.stdout
	sysCheckLog = open("sysCheck.log", 'w')
	sys.stdout = sysCheckLog

	print("\nNote : Doing system check...")

	#Print OS and time
	print("Note : Timestamp %s, %s" %(time.strftime("%d/%m/%Y"), time.strftime("%H:%M:%S")))
	print("Note : Running on platform '%s'" %(sys.platform))

	#Test Python Version
	pyVersion = sys.hexversion
	if (pyVersion < 0x04000000) or (pyVersion > 0x03000000):
		print("Note : Running Python version '%s' " %(pyVersion))
	else:
		print("Error: Running Python version '%s'. Python 3.x is required " %(pyVersion))
		sys.exit(1)
		
	print("Note : Rolling updates enabled, '%s'" %('no'))
	print("Note : noodle-pipe release version '%s'" %('0.0.0'))

	#Check core dependencies
	jsonFile = open('../modules/data/dependencies.json', 'r')
	jsonData = json.load(jsonFile)
	jsonFile.close()
	
	for keys, values in jsonData.items():
		for items in jsonData[keys]:
			try:
				imp.find_module(items)
			except:
				print("Error: Found core module '%s', no" %(items))
				raise Exception("Found core module '%s', no" %(items))
				sys.exit(1)
			else:
				print("Note : Found core module '%s', yes" %(items))
				
	#Check plugin dependencies
	dirList = os.listdir('../plugins/')
	fileList = []
	plugModules = []
	for items in dirList:
		print("Note : Found plugin '%s' in '%s'" %(items, "../plugins/%s/" %(items)))
		if os.path.isfile("../plugins/%s/data" %(items)):
			jsonFile = open("../plugins/%s/data" %(items), 'r')
			jsonData = json.load(jsonFile)
			jsonFile.close
	
			for keys, values in jsonData.items():
				for items in jsonData[keys]:
					try:
						imp.find_module(items)
					except:
						print("Error: Found plugin module '%s', no" %(items))
					else:
						print("Note : Found plugin module '%s', yes" %(items))	
		else:
			print("Warn : Found dependencies.json for plugin '%s', no" %(items))
			#raise Exception("Found dependencies.json for plugin '%s', no" %(items))
				
	#Stop writing to sysCheck.log
	sys.stdout = unlog
	sysCheckLog.close()
	print("Note : Read sysCheck.log for details")

#Queryies all noodle-pipe modules for a list of dependencie modules	
def modGather():
	if os.path.isdir("../modules/data/"):
		print("Note : Found path '../modules/data/', yes")
	else:
		print("Warn : Found path '../modules/data/', no")
		print("Warn : Can't determine core module dependencies")
		
	#get list of noodle-pipe core modules
	dirList = os.listdir('../modules/')
	coreModules = []
	for items in dirList:
		if items[-2:] == 'py':
			coreModules.append(items[:-3])
		
	#get list of plugin modules
	dirList = os.listdir('../plugins/')
	fileList = []
	plugModules = []
	for items in dirList:
		fileList.append(os.listdir("../plugins/%s/data" %(items)))
		#if items[-2:] == 'py':
		#	modules.append(items[:-3])
	print(fileList)

#Determines what modules are availible and which arnt	
def modCheck(modules=None):
	if (modules is None) or (modules < 1):
		raise Exception("Expected type 'List' with length > 0")
	else:
		moduleDic = {}
		for mods in modules:
			try:
				imp.find_module(mods)
			except:
				moduleDic[str(mods)] = False
			else:
				moduleDic[str(mods)] = True
	return(moduleDic)

#Prints the results of modCheck() to the terminal
def modPrint(modules=None):
	if (modules is None) or (modules < 1):
		raise Exception("Expected type 'List' with length > 0")
	else:
		for keys, values in modules.items():
			if values is False:
				print("Error: Found module '%s', no" %(keys))
			else:
				print("Note : Found module '%s', yes" %(keys))


if __name__ == '__main__':
	print("Error: Improper usage of 'syscheck', See documentaion for proper usage")
	raise Exception("Improper usage of 'syscheck', See documentaion for proper usage")

