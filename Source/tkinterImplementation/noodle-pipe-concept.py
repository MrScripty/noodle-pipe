#!/usr/local/bin/python3.3
try:
	##Python 3	
	from tkinter import *
except ImportError:
	##Python 2
	from Tkinter import *
	
try:
	import re
except ImportError:
	print("Could not locate 're' module")
	

class App:
	def __init__(self, tk, master=None):
		
		print("")
		print("noodle-pipe start")
		print("-----------------")
		
		GUI(name="Main")
		can.focus_force()
		
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
				self.gridFill="#262626"
			else:		
				chunkCount -= 1
				self.gridFill = gridFill
			self.canvas.create_line(hLength, 0, hLength, self.y, fill=self.gridFill, width="1")
			hLength += self.gridSpace
			self.canvas.create_line(0, vLength, self.x, vLength, fill=self.gridFill, width="1")
			vLength += self.gridSpace
					
		#Create quit button
		quit_button = Button(self.frame, text="End", command=self.end)
		quit_button.grid(row=1, column=0, sticky=(S,E))
		
		#pack
		self.frame.pack(fill=BOTH, expand=True)
		self.initial = (0, 0)
		
		#create right click
		#Note: lambda is required to pass a arg in add_command
		self.nodeMenu = Menu(self.frame)
		self.nodeMenu.add_command(label="Devel-01", command=(lambda:Node(name="testOne")))
		self.nodeMenu.add_command(label="Devel-02", command=(lambda:Node(name="testTwo")))
		
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
	def __init__(self, name, anchorIn=4, anchorOut=2, anchorScale=12, anchorSpace=10, anchorFill="#DFCA35", bodyFill="#9B9B9B", nodeXY=(100, 100, 200, 300), headerHeight=15):
		#variables
		self.name = name
		self.anchorIn = anchorIn
		self.anchorOut = anchorOut
		self.anchorSpace = anchorSpace
		self.anchorScale = anchorScale
		self.nodeXY = nodeXY
		self.headerHeight = headerHeight
		self.stop = [0, 0]
		self.noodle = None
		self.noodleTag = None
		self.nodeBody = None
		self.noodlesIn, self.noodlesOut = [], []
		self.anchorInXY, self.anchorOutXY = [], []
		self.noodleInStartXY, self.noodleOutStartXY = [], []
		
		self.name = self.checkName(nodeName=self.name, nameType=0)
		
		if self.name != None:
			#create GUI
			#Body
			bodyTag = self.name + "_body"
			self.nodeBody = can.create_rectangle((nodeXY[0], nodeXY[1]), (nodeXY[2], nodeXY[3]), fill=bodyFill, outline="#9d9d9d", activefill="#9d9d9d", tag=(self.name, bodyTag))
			can.tag_bind(bodyTag, "<Button-1>", self.clickNode)
			can.tag_bind(bodyTag, "<B1-Motion>", self.dragNode)
			can.tag_bind(bodyTag, "<Double-Button-1>", self.deleteNode)
		
			#scriptEditor
			#self.canvas.bind("<Tab>", self.onShift)
		
			#Header
			can.create_rectangle((self.nodeXY[0], self.nodeXY[1]), (self.nodeXY[2], (self.nodeXY[1] + self.headerHeight)), fill="#646464", outline="#646464", tag=(self.name, "header"))
			can.create_text(self.nodeXY[0], self.nodeXY[1], anchor="nw", text=self.name, tag=self.name)

			#anchors
			while self.anchorIn > 0:
				startX = self.nodeXY[0] - (self.anchorScale / 2)
				startY = self.nodeXY[1] + self.headerHeight + ((self.anchorSpace * (self.anchorIn - 1) + self.anchorSpace) + (self.anchorScale * (self.anchorIn - 1)))
				endPos = startY + self.anchorScale
				
				anchorInTag = self.name + "_anchorIn_" + str(self.anchorIn)
				can.create_oval((startX, startY), (startX + self.anchorScale, endPos), fill=bodyFill, outline="#000000", activefill="#DFCA35", tag=(self.name, anchorInTag))
				can.tag_bind(anchorInTag, "<Button-1>", self.clickAnchor)
				can.tag_bind(anchorInTag, "<B1-Motion>", self.dragAnchor)
				#can.tag_bind(anchorInTag, "<ButtonRelease-1>", self.releaseAnchor)
				self.anchorIn -= 1
	
			while self.anchorOut > 0:
				startX = self.nodeXY[2] - (self.anchorScale / 2)
				startY = self.nodeXY[1] + self.headerHeight + ((self.anchorSpace * (self.anchorOut - 1) + self.anchorSpace) + (self.anchorScale * (self.anchorOut - 1)))
				endPos = startY + self.anchorScale

				anchorOutTag = self.name + "_anchorOut_" + str(self.anchorOut)
				can.create_oval((startX, startY), (startX + self.anchorScale, endPos), fill=bodyFill, outline="#000000", activefill="#DFCA35", tag=(self.name, anchorOutTag))
				can.tag_bind(anchorOutTag, "<Button-1>", self.clickAnchor)
				can.tag_bind(anchorOutTag, "<B1-Motion>", self.dragAnchor)
				#can.tag_bind(anchorInTag, "<ButtonRelease-1>", self.releaseAnchor)
				self.anchorOut -= 1
		
	
	#can.find_all
	#print(can.find_withtag(all))
	def checkName(self, nodeName, nameType=0):
		#non type specific errors
		length = len(nodeName)
		if (length <= 3) or (length > 64):
			Report(msg="Name length out of bounds", caller="Node.checkName")
			return(None)
			pass
		elif re.match('^[\w-]+$', self.name) is None:
			Report(msg="Name contains non alphanumeric characters", caller="Node.checkName")
			return(None)
			pass
		#Type specific errors
		elif nameType is 0:
			if len(can.find_withtag(nodeName)) > 0:
				conflict = True
				count = 1
				while conflict is True:
					nameOut = nodeName + "_" + str(count)
					count += 1
					if len(can.find_withtag(nameOut)) == 0:
						return(nameOut)
						conflict = False
			else:
				nameOut = nodeName
				return(nameOut)
		#Anchor	
		elif nameType is 1:
			pass
		elif nameType is 2:
			pass
		
	
	def deleteNode(self, event):
		can.delete(self.name)
	
					
	def clickNode(self, event):
		can.tag_raise(self.name)
		#get XY of event
		self.startX, self.startY = event.x, event.y
		
		#create a list of anchorIns and anchorOuts
		nodeBodyXY = can.coords(self.nodeBody)
		idList = can.find_overlapping(nodeBodyXY[0], nodeBodyXY[1], nodeBodyXY[2], nodeBodyXY[3])
		for items in idList:
			if "anchorIn" in can.itemcget(items, "tag"):
				self.anchorInXY.append(items)
			if "anchorOut" in can.itemcget(items, "tag"):
				self.anchorOutXY.append(items)
		
		#Required to find relations across nodes
		#Determine which in and outs have a noodle and store the noodle id
		for anchors in self.anchorInXY:
			anchorXY = can.coords(anchors)
			idList = can.find_overlapping(anchorXY[0], anchorXY[1], anchorXY[2], anchorXY[3])
			#anchors will not handel properly if outside node body
			for items in idList:
				item = can.itemcget(items, "tag")
				if "noodle" in item:
					self.noodlesIn.append(items)
		for anchors in self.anchorOutXY:
			anchorXY = can.coords(anchors)
			idList = can.find_overlapping(anchorXY[0], anchorXY[1], anchorXY[2], anchorXY[3])
			for items in idList:
				item = can.itemcget(items, "tag")
				if "noodle" in item:
					self.noodlesOut.append(items)
		
		#Required to drag noodles with node			
		#Get start positions of noodles
		for noodles in self.noodlesIn:
			self.noodleInStartXY.append(can.coords(noodles))
		for noodles in self.noodlesOut:
			self.noodleOutStartXY.append(can.coords(noodles))


	def dragNode(self, event):
		#Move node
		offsetXY = ((event.x - self.startX), (event.y - self.startY))
		can.move(self.name, offsetXY[0], offsetXY[1])
		self.startX = event.x
		self.startY = event.y
		
		#move noodles
		noodleCount = len(self.noodlesIn)
		if noodleCount > 0:
			count = 0
			for noodles in self.noodlesIn:
				print(event.x)
				print(self.noodleInStartXY[count][1])
				can.coords(noodles, self.noodleInStartXY[count][0], self.noodleInStartXY[count][1], (self.noodleInStartXY[count][2] - event.x), (self.noodleInStartXY[count][3] - event.y))
				#self.noodleInStartXY[count][2] -= event.x
				#self.noodleInStartXY[count][3] -= event.y
				count += 1
			for noodles in self.noodlesOut:
				pass
				
			
	def clickAnchor(self, event):
		#Set start XY
		self.start = can.coords(can.find_closest(event.x, event.y))
		self.start[0] += self.anchorScale / 2
		self.start[1] += self.anchorScale / 2
		
		#Generate noodle name
		self.noodleTag = self.name + "_noodle_" + str(can.find_withtag("current")[0])
		self.noodelTag = self.checkName(nodeName=self.noodleTag, nameType=0)
		
		#create noodle
		self.noodle = can.create_line(self.start[0], self.start[1], event.x, event.y, fill="#737373", width="2", tag=self.noodleTag)
		
		
	def dragAnchor(self, event):
		#get id's of items under cursor
		idList = can.find_overlapping(event.x, event.y, event.x, event.y)
		#idList = can.find_closest(event.x, event.y)
		#Test if id is a anchorIn and return xy
		if len(idList) > 0:
			for items in idList:
				item = can.itemcget(items, "tag")
				for tags in item:
					#Fixes a problem where time delay allows the cursor to momentarly be ontop of the noodle
					if self.noodleTag in item:
						pass
					#The not prevents nodes from feeding into themselves
					elif ("anchorIn" in item) and not (self.name in item):
						#Get coords of anchor
						self.stop = can.coords(items)
						#Snap noodle to center of anchor
						self.stop[0] += (self.anchorScale / 2)
						self.stop[1] += (self.anchorScale / 2)
						can.itemconfig(self.noodle, fill="#62735B")
						can.coords(self.noodle, self.start[0], self.start[1], self.stop[0], self.stop[1])
						break
					else:
						can.itemconfig(self.noodle, fill="#735E5B")
						can.coords(self.noodle, self.start[0], self.start[1], event.x, event.y)
						break
		else:
			can.itemconfig(self.noodle, fill="#737373")		
			can.coords(self.noodle, self.start[0], self.start[1], event.x, event.y)
		
		
	def releaseAnchor(self, event):
		idList = can.find_overlapping(event.x, event.y, event.x, event.y)
		print(idList)
		print("yes")
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
		
		#can.coords("noodle", self.start[0], self.start[1], self.stop[0], self.stop[1])
		
		
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
#tk.geometry("1080x720")
#node_001 = Node(name="Devel")
#print(node_001.name)
App(None)

tk.mainloop()

##root.destroy()


