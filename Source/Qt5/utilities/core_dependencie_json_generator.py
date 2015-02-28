#!/usr/bin/python
# -*- coding: utf-8 -*-

import json


def main():
	
	dependencies = {
	'__init__' : ['syscheck', 'gui', 'sys', 'imp', 'os', 'time', 'json'],
	'gui' : ['node', ]
	 }
	 
	
	data = dependencies 
	with open('dependencies.json', 'w') as outfile:
		json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)
		
		
main()

