#!py -3

import tkinter as tk
from Graph import *
from GraphCanvas import GraphCanvas

BACKGROUND_COLOR = "light slate gray"

root = tk.Tk()
root.configure(bg=BACKGROUND_COLOR)

label = tk.Label(root, text="Title", bg=BACKGROUND_COLOR)
label.pack() # For things to be visible, it needs to be packed

#-------------------------

#v = [Vertex(50,50, label="hi"), Vertex(200,100), Vertex(50,100)]
#e = [Edge(v[0], v[1])]
#g = Graph(v, e)

w = GraphCanvas(root, width=400, height=300, background="white")
w.pack()
#w.draw_graph(g)
g = Kn(4)
w.draw_graph(g)
w.show_edge_crossings(g)

#-------------------------

'''
w = tk.Canvas(root, width=400, height=300, background="white")
w.pack()

w.create_line(0,0, 200, 100)
w.create_rectangle(50,100, 0, 70)
w.create_rectangle(50,25,150,80)

w.create_oval(90,90,150,150, fill="red")
w.create_text(100,10,text="HI")
'''

def func():
	func.i = func.i+1
	g = Kn(func.i)
	w.draw_graph(g)
	w.show_edge_crossings(g)
func.i = 4

next_bttn = tk.Button(root, text="Next", command=func)
next_bttn.pack()

root.mainloop()