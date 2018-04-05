# Creates a window that can hold a graph.

import tkinter as tk

class GraphCanvas(tk.Canvas):
	graphScale = 1 # How much to * vertex positions by
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	
	def draw_graph(self, graph):
		self.delete(tk.ALL)
		for index, edge in enumerate(graph.edges):
			self.create_line(
				edge.vert1.x *self.graphScale,edge.vert1.y *self.graphScale,
				edge.vert2.x *self.graphScale,edge.vert2.y *self.graphScale,
				fill=edge.color,
				width=edge.width *self.graphScale
			)
			# DEBUG: Add label to edge
			labelX = (edge.vert2.x -edge.vert1.x) /4 +edge.vert1.x
			labelY = (edge.vert2.y -edge.vert1.y) /4 +edge.vert1.y
			self.create_text(
				labelX *self.graphScale,
				labelY *self.graphScale,
				text=index, fill="green", font="bold"
			)
		for vert in graph.vertices:
			self.create_oval(
				(vert.x -vert.radius) *self.graphScale, (vert.y -vert.radius) *self.graphScale,
				(vert.x +vert.radius) *self.graphScale, (vert.y +vert.radius) *self.graphScale,
				fill=vert.color
			)
			if vert.label:
				self.create_text(vert.x *self.graphScale,vert.y *self.graphScale, text=vert.label)
	
	def show_edge_crossings(self, graph):
		CROSSING_RADIUS = 5
		CROSSING_COLOR = "red"
		for intersection in graph.get_edge_crossings():
			x = intersection[0]
			y = intersection[1]
			self.create_oval(
				(x -CROSSING_RADIUS) *self.graphScale, (y -CROSSING_RADIUS) *self.graphScale,
				(x +CROSSING_RADIUS) *self.graphScale, (y +CROSSING_RADIUS) *self.graphScale,
				fill=CROSSING_COLOR
			)
	