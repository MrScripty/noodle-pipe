#!/usr/bin/python
# -*- coding: utf-8 -*-



def main():
	#Load modules
	try:
		import imp
		import sys
	except ImportError:
		print("Error: Faild to import modules.")
		print("Error: Exiting application")
		sys.exit(1)
	
	#Test if modules availible
	testMods = ['sys', 're', 'time', 'PyQt5', 'node']
	for mods in testMods:
		try:
			imp.find_module(mods)
		except:
			print("Error: Could not find '%s' module" %(mods))
			print("Error: Exiting application")
			sys.exit(1)
		else:
			print("Note : Found module '%s'" %(mods))

	#Test Python Version
	pyVersion = sys.hexversion
	if (pyVersion < 0x04000000) or (pyVersion > 0x03000000):
		print("Note : Running Python version '%s' " %(pyVersion))
	else:
		print("Error: Running Python version '%s'. Python 3.x is required " %(pyVersion))
		sys.exit(1)
		
def modList():
	return(['imp', 'sys'])
	
