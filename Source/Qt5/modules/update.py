#!/usr/bin/python
# -*- coding: utf-8 -*-


def main():
	#Load modules
	try:
		import pygit2
		import sys
	except ImportError:
		print("Error: Faild to import modules.")
		sys.exit(1)
		
	pygit2.status()
	
def gitInfo():
	pass
	
def modList():
	return(['pygit2', 'sys'])
	
		
	
	

	
