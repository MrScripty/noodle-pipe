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
		
		Report(msgType=2, caller="App", msg="Test")
		Report(msgType=1)
		Report(msgType=2)
		
		
		
		GUI(name="Main")
		
		Node(name="dfgh")
		Node(name="yesterday")

		
class GUI:
	def __init__(self, name, x=1280, y=720, canvasFill="#393939", gridSpace=17, gridFill="#2f2f2f"):
		#variables
		global can
		self.x = x
		self.y = y
		self.canvasFill = canvasFill
		self.gridSpace = gridSpace
		self.gridFill = gridFill
		
		#Create canvas
		self.frame = Frame(tk)
		can = self.canvas = Canvas(self.frame, width=self.x, height=self.y, bg=self.canvasFill)
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
		
		#create right click menu
		#Note: lambda is required to pass a arg in add_command
		self.nodeMenu = Menu(self.frame)
		self.nodeMenu.add_command(label="Devel-01", command=(lambda:Node(name="yesterday")))
		self.nodeMenu.add_command(label="Devel-02", command=(lambda:Node(name="Shwoola")))
		
		#Bind canvas
		self.canvas.bind("<Button-3>", self.rightClickMenu)
		self.canvas.bind("<Button-1>", self.start_line)
		self.canvas.bind("<B1-Motion>", self.draw_line)
		self.canvas.bind("<MouseWheel>", self.onMouseWheel)
		

	def onMouseWheel(self):
		print("You used the scroll wheel!")
		
		
	def rightClickMenu(self, event):
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
		
		print(len(can.find_withtag(self.name)))
		#check if valid name
		length = len(self.name)
		if (length <= 3) or (length > 64):
			Report(msg="Name length out of bounds", caller="Node")
			pass
		elif re.match('^[\w-]+$', self.name) is None:
			Report(msg="Name contains non alphanumeric characters", caller="Node")
			pass
		elif len(can.find_withtag(self.name)) >= 0:
			Report(msg="Name already exists", caller="Node", msgType=2)
			conflict = True
			count = 1
			while conflict is True:
				name = self.name + "_" + str(count)
				count += 1
				if len(can.find_withtag(name)) == 0:
					self.name = name
					conflict = False

					#create GUI
					#can.find_all
					#print(can.find_withtag(all))
					#Body
					can.create_rectangle((nodeXY[0], nodeXY[1]), (nodeXY[2], nodeXY[3]), fill=bodyFill, outline="#9d9d9d", activefill="#9d9d9d", tag=self.name)
					can.tag_bind(self.name, "<Button-1>", self.clickNode)
					can.tag_bind(self.name, "<B1-Motion>", self.dragNode)
					4
					#Header
					can.create_rectangle((self.nodeXY[0], self.nodeXY[1]), (self.nodeXY[2], (self.nodeXY[1] + self.headerHeight)), fill="#646464", outline="#646464", tag=self.name)
					can.create_text(self.nodeXY[0], self.nodeXY[1], anchor="nw", text=self.name, tag=self.name)
			
					#anchors
					while self.anchorIn > 0:
						startX = self.nodeXY[0] - (self.anchorScale / 2)
						startY = self.nodeXY[1] + self.headerHeight + ((self.anchorSpace * (self.anchorIn - 1) + self.anchorSpace) + (self.anchorScale * (self.anchorIn - 1)))
						endPos = startY + self.anchorScale
			
						can.create_oval((startX, startY), (startX + self.anchorScale, endPos), fill=bodyFill, outline="#000000", activefill="#DFCA35", tag=self.name)
						self.anchorIn -= 1
				
					while self.anchorOut > 0:
						startX = self.nodeXY[2] - (self.anchorScale / 2)
						startY = self.nodeXY[1] + self.headerHeight + ((self.anchorSpace * (self.anchorOut - 1) + self.anchorSpace) + (self.anchorScale * (self.anchorOut - 1)))
						endPos = startY + self.anchorScale
			
						can.create_oval((startX, startY), (startX + self.anchorScale, endPos), fill=bodyFill, outline="#000000", activefill="#DFCA35", tag=self.name)
						self.anchorOut -= 1
				
					#self.canvas.tag_bind("node1", "<ButtonRelease-1>", self.releaseNode)
		
	
	def clickNode(self, event):
        	self.startX = event.x
        	self.startY = event.y


	def dragNode(self, event):
		x, y, _, _ = can.coords(self.name)
		can.move(self.name, (event.x - self.startX), (event.y - self.startY))
		self.startX = event.x
		self.startY = event.y
		
		
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


