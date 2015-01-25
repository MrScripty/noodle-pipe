#!/usr/local/bin/python3.3
try:
	##Python 3	
	from tkinter import *
except ImportError:
	##Python 2
	from Tkinter import *


class App:
	def __init__(self, app, master=None):
		global top

		#Create canvas
		self.frame = Frame(app)
		top = self.canvas = Canvas(self.frame, width=1080, height=720, bg="#393939")
		top.grid(row=0, column=0)
		
		#Draw grid
		segments = 20
		chunks = 4
		dimentions = [int(top.cget("width")), int(top.cget("height"))]
		
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
		
		#create node
		self.draw_rect()
		
		#Bind canvas
		self.canvas.bind("<Button-1>", self.start_line)
		self.canvas.bind("<B1-Motion>", self.draw_line)
		
		#Create quit button
		quit_button = Button(self.frame, text="End", command=self.end)
		quit_button.grid(row=1, column=0, sticky=(S,E))

		#create right click menu
		self.nodeMenu = Menu(self.frame, tearoff=False)
		self.nodeMenu.add_command(label="Devel", command=self.draw_rect())
		
		self.canvas.bind("<Button-3>", self.rightClickMenu)
		
		self.frame.pack(fill=BOTH, expand=True)
		
		self.initial = (0, 0)
		
		
	def rightClickMenu(self, event):
		self.nodeMenu.post(event.x_root, event.y_root)
	
	def start_line(self, event):
		self.initial = (event.x, event.y)

	def draw_line(self, event):
		self.canvas.create_line((self.initial[0], self.initial[1]), (event.x, event.y))
		self.initial = (event.x, event.y)


	def draw_rect(self):
		top.create_rectangle((100, 300), (30, 40), fill="#9B9B9B", outline="#9d9d9d", activefill="#9d9d9d", tag="node1")
		#app.bind("<Button-1>", self.click)
		top.tag_bind("node1", "<Button-1>", self.clickNode)
		top.tag_bind("node1", "<B1-Motion>", self.dragNode)
		#top.tag_bind("node1", "<ButtonRelease-1>", self.releaseNode)


	def clickNode(self, event):
        	self.startX = event.x
        	self.startY = event.y


	def dragNode(self, event):
		x, y, _, _ = self.canvas.coords('node1')
		self.canvas.move('node1', (event.x - self.startX), (event.y - self.startY))
		self.startX = event.x
		self.startY = event.y


	def end(self):
		self.nodeFrame.quit()


if __name__ == '__main__':
	app = Tk()
	
app.title("Node Editor")
app.configure(bg = "#393939")
##app.geometry("1080x720")
App(None)

app.mainloop()
##root.destroy()


'''
Create nodes
Draw line between two points
Add anchors on nodes
node name textbox

'''
