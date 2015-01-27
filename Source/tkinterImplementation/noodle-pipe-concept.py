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
		
		Report(msgType=0, caller="App", msg="Test")
		Report(msgType=1)
		Report(msgType=2)
		
		GUI(name="Main")
		
		#Create node
		
		node_001 = Node(name="Devel")
		node_002 = Node(name="Spam")
		node_003 = Node(name="Gotcha")
		

class GUI:
	def __init__(self, name, x=1280, y=720, canvasFill="#393939"):
		#variables
		global can
		self.x = x
		self.y = y
		self.canvasFill = canvasFill
		
		#Create canvas
		self.frame = Frame(tk)
		can = self.canvas = Canvas(self.frame, width=self.x, height=self.y, bg=self.canvasFill)
		self.canvas.grid(row=0, column=0)
		
		#Draw grid
		segments = 20
		chunks = 4
		dimentions = [int(self.canvas.cget("width")), int(self.canvas.cget("height"))]
		chunkCount = 0
		segCount = segments
		while segCount > 0:
			if chunkCount == 0:
				chunkCount = chunks
				self.canvas.create_line((dimentions[0] / segments * segCount), dimentions[1], (dimentions[0] / segments * segCount), 0, fill="#292929", width="2")
				self.canvas.create_line(dimentions[0], (dimentions[1] / segments * segCount), 0, (dimentions[1] / segments * segCount), fill="#292929", width="2")
				pass
			else:
				self.canvas.create_line((dimentions[0] / segments * segCount), dimentions[1], (dimentions[0] / segments * segCount), 0, fill="#2f2f2f", width="1")
				self.canvas.create_line(dimentions[0], (dimentions[1] / segments * segCount), 0, (dimentions[1] / segments * segCount), fill="#2f2f2f", width="1")
				segCount = segCount - 1 
				chunkCount = chunkCount - 1
		
		#Create quit button
		quit_button = Button(self.frame, text="End", command=self.end)
		quit_button.grid(row=1, column=0, sticky=(S,E))
		
		#pack
		self.frame.pack(fill=BOTH, expand=True)
		self.initial = (0, 0)
		
		
		#create right click menu
		self.nodeMenu = Menu(self.frame)
		self.nodeMenu.add_command(label="Devel-01", command=self.onMouseWheel)
		self.nodeMenu.add_command(label="Devel-02", command=self.onMouseWheel)
		self.canvas.bind("<Button-3>", self.rightClickMenu)
		
		#Bind canvas
		self.canvas.bind("<Button-1>", self.start_line)
		self.canvas.bind("<B1-Motion>", self.draw_line)
		self.canvas.bind("<MouseWheel>", self.onMouseWheel)



	def onMouseWheel(self):
		print("You used the scroll wheel!")
		
		
	def rightClickMenu(self, event):
		self.nodeMenu.post(event.x_root, event.y_root)
	
	
	def start_line(self, event):
		self.initial = (event.x, event.y)


	def draw_line(self, event):
		self.canvas.create_line((self.initial[0], self.initial[1]), (event.x, event.y))
		self.initial = (event.x, event.y)
	

	def end(self):
		self.frame.quit()

	
class Node:
	def __init__(self, name, anchorIn=1, anchorOut=1, colorFill="#9B9B9B"):
		#variables
		self.name = name
		self.anchorIn = anchorIn
		self.anchorOut = anchorOut
		
		#check if valid name
		length = len(self.name)
		if (length <= 3) or (length > 64):
			print("Error: name length out of bounds")
			pass
		elif re.match('^[\w-]+$', self.name) is None:
			print("Error: name contains non alphanumeric characters")
			pass
		else:
			#create GUI
			can.create_rectangle((100, 100), (300, 300), fill=colorFill, outline="#9d9d9d", activefill="#9d9d9d", tag=self.name)
			can.tag_bind(self.name, "<Button-1>", self.clickNode)
			can.tag_bind(self.name, "<B1-Motion>", self.dragNode)
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


