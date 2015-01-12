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

		self.frame = Frame(app)
		top = self.canvas = Canvas(self.frame, width=1080, height=720, bg="#6a6a6a")
		top.grid(row=0, column=0)

		self.draw_rect()

		quit_button = Button(self.frame, text="End", command=self.end)
		quit_button.grid(row=1, column=0, sticky=(S,E))

		self.frame.pack(fill=BOTH, expand=True)

		self.canvas.bind("<Button-1>", self.start_line)
		self.canvas.bind("<B1-Motion>", self.draw_line)
		self.initial = (0, 0)


	def start_line(self, event):
		self.initial = (event.x, event.y)


	def draw_line(self, event):
		self.canvas.create_line((self.initial[0], self.initial[1]), (event.x, event.y))
		self.initial = (event.x, event.y)


	def draw_rect(self):
		top.create_rectangle((100, 300), (30, 40), fill="#4d4d4d", outline="#9d9d9d", activefill="#9d9d9d", tag="node1")
		##app.bind("<Button-1>", self.click)
		top.tag_bind("node1", "<Button-1>", self.clickNode)
		top.tag_bind("node1", "<B1-Motion>", self.dragNode)
		##top.tag_bind("node1", "<ButtonRelease-1>", self.releaseNode)


	def clickNode(self, event):
        	self.startX = event.x
        	self.startY = event.y


	def dragNode(self, event):
		x, y, _, _ = self.canvas.coords('node1')
		self.canvas.move('node1', (event.x - self.startX), (event.y - self.startY))
		self.startX = event.x
		self.startY = event.y


	def end(self):
		self.frame.quit()


if __name__ == '__main__':
	app = Tk()
	
app.title("Node Editor")
app.configure(bg = "#6a6a6a")
##app.geometry("1080x720")
App(None)

app.mainloop()
##root.destroy()


'''
Create nodes
Move nodes
Draw line between two points
Add anchors on nodes
node name textbox

'''
