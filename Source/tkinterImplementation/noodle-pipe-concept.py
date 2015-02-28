#!/usr/local/bin/python3.3
try:
	import sys
	import re
	from tkinter import *
	#from os import path
except ImportError:
	print("Faild to import modules.")
	sys.exit(1)

if (sys.hexversion < 0x03030000) or (sys.hexversion > 0x03050000):
	print("noodle-pipe requires Python 3.3.5 or equivilant")
	sys.exit(1)


class App:
	def __init__(self, tk, master=None):
		print("")
		print("noodle-pipe start")
		print("-----------------")

		GUI(name="Main")
		can.focus_force()

		#Add a default node for testing
		Node(name="developer")


class GUI:
	def __init__(self, name, x=None, y=None, canvasFill="#393939", gridSpace=17, gridFill="#2f2f2f"):
		#variables
		global can
		self.canvasFill = canvasFill
		self.gridSpace = gridSpace
		self.gridFill = gridFill
		if x or y is None:
			pass
			self.x, self.y = (tk.winfo_screenwidth(), tk.winfo_screenheight())
		else:
			self.x = x
			self.y = y

		#Create canvas
		self.frame = Frame(tk)
		can = self.canvas = Canvas(self.frame, width=self.x, height=self.y, bg=self.canvasFill, scrollregion=(0, 0, 1000, 1000))
		self.canvas.grid(row=0, column=0)

		#Draw grid
		chunks = 4
		chunkCount = 0
		hLength = 0
		vLength = 0
		while (hLength <= self.x) or (vLength <= self.y):
			if chunkCount == 0:
				chunkCount = chunks
				self.gridFill = "#262626"
			else:
				chunkCount -= 1
				self.gridFill = gridFill
			self.canvas.create_line(hLength, 0, hLength, self.y, fill=self.gridFill, width="1")
			hLength += self.gridSpace
			self.canvas.create_line(0, vLength, self.x, vLength, fill=self.gridFill, width="1")
			vLength += self.gridSpace

		#Create quit button
		quit_button = Button(self.frame, text="End", command=self.end)
		quit_button.grid(row=1, column=0, sticky=(S, E))

		#pack
		self.frame.pack(fill=BOTH, expand=True)
		self.initial = (0, 0)

		#create right click
		#Note: lambda is required to pass a arg in add_command
		self.nodeMenu = Menu(self.frame)
		self.nodeMenu.add_command(label="Devel-01", command=(lambda: Node(name="testOne", anchorIn=6, anchorOut=4)))
		self.nodeMenu.add_command(label="Devel-02", command=(lambda: Node(name="testTwo", anchorIn=2, anchorOut=1)))

		#Bind canvas
		self.canvas.bind("<Button-3>", self.rightClickMenu)
		#self.canvas.bind("<Button-1>", self.start_line)
		#self.canvas.bind("<B1-Motion>", self.draw_line)
		self.canvas.bind("<MouseWheel>", self.onMouseWheel)
		#self.canvas.bind("<Shift_L>", self.onShift)

	def onShift(self, event):
		print("Shifty")

	def onMouseWheel(self, event):
		print("This doesnt work")

	def rightClickMenu(self, event):
		#self.canvas.focus_force()
		self.nodeMenu.tk_popup(event.x_root, event.y_root)

	def start_line(self, event):
		self.initial = (event.x, event.y)

	def draw_line(self, event):
		self.canvas.create_line((self.initial[0], self.initial[1]), (event.x, event.y))
		self.initial = (event.x, event.y)

	def end(self):
		self.frame.quit()


class Node:
	def __init__(self, name, bodyFill="#9B9B9B", nodeXY=(100, 100, 200, 300), headerHeight=15, anchorIn=3, anchorOut=3, anchorScale=12, anchorSpace=10, anchorFill="#DFCA35"):
		#variables
		self.name = name
		self.bodyFill = bodyFill
		self.anchorIn = anchorIn
		self.anchorOut = anchorOut
		self.anchorSpace = anchorSpace
		self.anchorScale = anchorScale
		self.anchorFill = anchorFill
		self.nodeXY = nodeXY
		self.headerHeight = headerHeight
		self.stop = [0, 0]
		self.noodle = None
		self.nodeBody = None
		self.noodleAnchorInDic, self.noodleAnchorOutDic = {}, {}
		self.inOut = True
		self.noodleTagDic = {}

		self.newNode(name=self.name)
		#self.anchor(anchorIn=-1, anchorOut=0)

	def newNode(self, name=None):
		#print(id(self))
		self.name = self.checkName(nodeName=name, nameType=0)
		if self.name is not None:
			#create GUI
			#Body
			bodyTag = self.name + "_body"
			self.nodeBody = can.create_rectangle((self.nodeXY[0], self.nodeXY[1]), (self.nodeXY[2], self.nodeXY[3]), fill=self.bodyFill, outline="#9d9d9d", activefill="#9d9d9d", tag=(self.name, bodyTag))
			can.tag_bind(bodyTag, "<Button-1>", self.clickNode)
			can.tag_bind(bodyTag, "<B1-Motion>", self.dragNode)
			can.tag_bind(bodyTag, "<Double-Button-1>", self.deleteNode)

			#scriptEditor
			#self.canvas.bind("<Tab>", self.onShift)

			#Header
			can.create_rectangle((self.nodeXY[0], self.nodeXY[1]), (self.nodeXY[2], (self.nodeXY[1] + self.headerHeight)), fill="#646464", outline="#646464", tag=(self.name, "header"))
			can.create_text(self.nodeXY[0], self.nodeXY[1], anchor="nw", text=self.name, tag=self.name)

			self.anchor(anchorIn=self.anchorIn, anchorOut=self.anchorOut)
			#anchor(anchorIn=self.anchorIn, anchorOut=self.anchorOut, anchorScale=self.anchorScale, anchorSpace=self.anchorSpace, anchorFill="#9B9B9B")

	def anchor(self, anchorIn, anchorOut):
		#Create inputs
		while anchorIn > 0:
			#get XY of anchor
			startX = self.nodeXY[0] - (self.anchorScale / 2)
			startY = self.nodeXY[1] + self.headerHeight + ((self.anchorSpace * (anchorIn - 1) + self.anchorSpace) + (self.anchorScale * (anchorIn - 1)))
			endPos = startY + self.anchorScale

			#Generate a unique tag
			anchorInTag = self.name + "_anchorIn_" + str(self.anchorIn)

			#Create anchor and add to dictionary
			self.noodleAnchorInDic[can.create_oval((startX, startY), (startX + self.anchorScale, endPos), fill = self.bodyFill, outline = "#000000", activefill = "#DFCA35", tag = (self.name, anchorInTag))] = []
			#Add key bindings
			can.tag_bind(anchorInTag, "<Button-1>", self.clickAnchor)
			can.tag_bind(anchorInTag, "<B1-Motion>", self.dragAnchor)
			anchorIn -= 1

		#Remove inputs
		while anchorIn < 0:
			anchorIn += 1

		#Create outputs
		while anchorOut > 0:
			startX = self.nodeXY[2] - (self.anchorScale / 2)
			startY = self.nodeXY[1] + self.headerHeight + ((self.anchorSpace * (anchorOut - 1) + self.anchorSpace) + (self.anchorScale * (anchorOut - 1)))
			endPos = startY + self.anchorScale

			#Generate a unique tag
			anchorOutTag = self.name + "_anchorOut_" + str(self.anchorOut)

			self.noodleAnchorOutDic[can.create_oval((startX, startY), (startX + self.anchorScale, endPos), fill = self.bodyFill, outline = "#000000", activefill = "#DFCA35", tag = (self.name, anchorOutTag))] = []
			can.tag_bind(anchorOutTag, "<Button-1>", self.clickAnchor)
			can.tag_bind(anchorOutTag, "<B1-Motion>", self.dragAnchor)
			anchorOut -= 1

		#Remove outputs
		while anchorOut < 0:
			anchorOut += 1

	def checkName(self, nodeName, nameType=0):
		#non type specific errors
		length = len(nodeName)
		if (length <= 3) or (length > 64):
			Report(msg="Name length out of bounds", caller="Node.checkName")
			return(None)
			pass
		elif re.match('^[\w-]+$', nodeName) is None:
			Report(msg="Name contains non alphanumeric characters", caller="Node.checkName")
			return(None)
			pass
		#Type specific errors
		elif nameType is 0:
			newName = nodeName
			nodeName = nodeName + "_001"
			number = 0
			while can.find_withtag(nodeName):
					number += 1
					#Add pading to string until its 3 digits long
					if number < 10:
						nodeName = newName + "_00" + str(number)
					if (number < 100) and (number > 9):
						nodeName = newName + "_0" + str(number)
					if (number > 99) and (number < 1000):
						nodeName = newName + "_" + str(number)
			return(nodeName)

		#Anchor
		elif nameType is 1:
			pass
		elif nameType is 2:
			pass

	def deleteNode(self, event):
		can.delete(self.name)

	def clickNode(self, event):
		#can.tag_raise(self.name)
		#Set motion vector
		self.startX = event.x
		self.startY = event.y

		def anchorDicUpdate(dic):
			#Test if noodle is atached to anchor and add noodle to dic if true
			for keys, values in dic.items():
				#get coords of anchor
				coords = can.coords(keys)
				#reduce area to check for overlap
				coords[0] += self.anchorScale / 2 + 1
				coords[1] += self.anchorScale / 2 + 1
				coords[2] -= self.anchorScale / 2 + 1
				coords[3] -= self.anchorScale / 2 + 1
				#Get overlapping
				overlap = can.find_overlapping(coords[0], coords[1], coords[2], coords[3])
				for widgets in overlap:
					#Test if widget is a noodle
					if "normalNoodle" in can.itemcget(widgets, "tag"):
						widgetCoords = can.coords(widgets)
						#Test if widget is located on anchor
						if (widgetCoords[0] < coords[0]) and (widgetCoords[1] < coords[1]):
							#Add noodle to dic
							widgets = [widgets]
							#list set will remove duplicate entrys
							dic[keys] = list(set(values + widgets))

		anchorDicUpdate(self.noodleAnchorInDic)
		anchorDicUpdate(self.noodleAnchorOutDic)

	def dragNode(self, event):
		#Move node
		offsetXY = ((event.x - self.startX), (event.y - self.startY))
		can.move(self.name, offsetXY[0], offsetXY[1])

		#Move noodles
		#noodleIn
		for keys, values in self.noodleAnchorInDic.items():
			if len(values) > 0:
				for noodle in values:
					#Get xy for noodle and anchor
					noodleCoords = can.coords(noodle)
					anchorCoords = can.coords(keys)
					#Get center position of anchor
					anchorCoords[2] -= self.anchorScale / 2
					anchorCoords[3] -= self.anchorScale / 2
					#update noodle coords
					can.coords(noodle, noodleCoords[0], noodleCoords[1], anchorCoords[2], anchorCoords[3])

		#noodleOut
		for keys, values in self.noodleAnchorOutDic.items():
			if len(values) > 0:
				for noodle in values:
					#Get xy for noodle and anchor
					noodleCoords = can.coords(noodle)
					anchorCoords = can.coords(keys)
					#Get center position of anchor
					anchorCoords[0] += self.anchorScale / 2
					anchorCoords[1] += self.anchorScale / 2
					#update noodle coords
					can.coords(noodle, anchorCoords[0], anchorCoords[1], noodleCoords[2], noodleCoords[3])

		#Update motion vector
		self.startX, self.startY = event.x, event.y

	def clickAnchor(self, event):
		#Get anchor id
		self.caller = can.find_withtag("current")[0]

		#Test if input or output
		if "anchorOut" in can.itemcget(self.caller, "tag"):
			self.inOut = True
		else:
			self.inOut = False

		#Get anchor coords
		self.start = can.coords(self.caller)[0:2]
		self.start[0] += self.anchorScale / 2
		self.start[1] += self.anchorScale / 2

		#Create tag
		self.noodleTagDic = {"parent": self.name, "kind": "normalNoodle", "anchorOut": self.caller, "anchorIn": None}
		#create noodle and add to dictionary
		self.noodleAnchorOutDic[self.caller] = [can.create_line(self.start[0], self.start[1], event.x, event.y, fill="#737373", width="2", tag=self.noodleTagDic)]

	def dragAnchor(self, event):
		#get id of noodle
		noodle = self.noodleAnchorOutDic[self.caller][0]
		#find items under cursor
		widgetList = can.find_overlapping(event.x, event.y, event.x, event.y)
		if len(widgetList) > 0:
			for widgets in widgetList:
				widgetTags = can.itemcget(widgets, "tag")
				#Fixes a problem where time delay allows the cursor to momentarly be ontop of the noodle
				if self.noodleTagDic["kind"] in widgetTags:
						pass
				#Prevent node from feeding into itself
				elif (self.noodleTagDic["parent"] in widgetTags):
					#Set noodle color red
					can.itemconfig(noodle, fill="#735E5B")
					#Remove anchor from noodleDic
					self.noodleTagDic["anchorIn"] = None
					#move noodle
					if self.inOut is True:
						can.coords(noodle, self.start[0], self.start[1], event.x, event.y)
					else:
						can.coords(noodle, event.x, event.y, self.start[0], self.start[1])
				#Check if widget is an input anchor
				elif ("_anchorIn_" in widgetTags) and ("_anchorOut_" in can.itemcget(self.noodleTagDic["anchorOut"], "tag")):
					#Get xy of anchor
					anchorXY = can.coords(widgets)[0:2]
					anchorXY[0] += self.anchorScale / 2
					anchorXY[1] += self.anchorScale / 2
					#set noodle color green
					can.itemconfig(noodle, fill="#62735B")
					#Add anchor to noodleDic
					self.noodleTagDic["anchorIn"] = widgets
					#move noodle
					if self.inOut is True:
						can.coords(noodle, self.start[0], self.start[1], anchorXY[0], anchorXY[1])
					else:
						can.coords(noodle, anchorXY[0], anchorXY[1], self.start[0], self.start[1])

				#Check if widget is output anchor
				elif "_anchorOut_" in widgetTags:
					#Set noodle color red
					can.itemconfig(noodle, fill="#735E5B")
					#Remove anchor from noodleDic
					self.noodleTagDic["anchorIn"] = None
					#move noodle
					if self.inOut is True:
						can.coords(noodle, self.start[0], self.start[1], event.x, event.y)
					else:
						can.coords(noodle, event.x, event.y, self.start[0], self.start[1])

				#The widget is not an anchor
				else:
					#set noodle color grey
					can.itemconfig(noodle, fill="#737373")
					#Remove anchor from noodleDic
					self.noodleTagDic["anchorIn"] = None
					if self.inOut is True:
						can.coords(noodle, self.start[0], self.start[1], event.x, event.y)
					else:
						can.coords(noodle, event.x, event.y, self.start[0], self.start[1])

		#If the list is of zero length
		else:
			#set noodle color grey
			can.itemconfig(noodle, fill="#737373")
			#Remove anchor from noodleDic
			self.noodleTagDic["anchorIn"] = None
			if self.inOut is True:
				can.coords(noodle, self.start[0], self.start[1], event.x, event.y)
			else:
				can.coords(noodle, event.x, event.y, self.start[0], self.start[1])

	def releaseAnchor(self, event):
		idList = can.find_overlapping(event.x, event.y, event.x, event.y)
		if len(idList) > 0:
			for items in idList:
				item = can.itemcget(items, "tag")
				for tags in item:
					if ("anchorIn" not in item) or ("anchorOut" not in item):
						can.delete(self.noodle)

		pass

	def getNoodleConnect(self):
		print("getNoodleEvent")
		pass

	def getAnchorDic(self):
		return[self.noodleAnchorOutDic, self.noodleAnchorInDic]


class Report:
	def __init__(self, caller=None, msgType=0, msg=None):
		if (msg is None) or (caller is None):
			pass
		else:
			message = ""
			if msgType == 0:
				message += "Error : "
			elif msgType == 1:
				message += "Warning : "
			else:
				message += "Notice : "
			message += caller + ", "
			message += msg

			print(message)


if __name__ == '__main__':
	tk = Tk()
	tk.title("Node Editor")
	tk.configure(bg = "#393939")
	App(None)
	tk.mainloop()
