import tkinter as tk
from Graph import *
import operator
from operator import itemgetter
from GraphCanvas import GraphCanvas

#-------------------------

workingSet = []
nextWorkingSet = []
planes = [[]]
firstplane = []
#planes.append(firstplane)
plane = 0

graph = GraphData('graph1')
#graph = Kn(5)
#verts = [Vertex() for i in range(10)]
#edges = EdgesFromIndices(verts, [
#	(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,0),
#	(0,5)
#])
#graph = Graph(verts, edges)

weights = graph.edgeWeights()
usedEdges = prims_alg(graph,weights)
spanTree = Graph(graph.vertices, usedEdges)
sortedWeights = sorted(weights.items(), key=itemgetter(1), reverse=True)

#print('planar?',spanTree.is_planar())
print(spanTree.export_mathematica())
print(sortedWeights)

for u in usedEdges:
    planes[plane].append(u)

print(planes)

for w in sortedWeights:
    if not (w[0] in usedEdges):
        workingSet.append(w[0])

#print(workingSet)

while (len(workingSet) > 0):
    #i = len(workingSet)
    while (len(workingSet) > 0):
        e = workingSet.pop()
        i = len(workingSet)
        print(i)
        edgeset = planes[plane].copy()
        edgeset.append(e)
        subgraph = Graph(graph.vertices, edgeset)
        if (subgraph.is_planar()):
            planes[plane].append(e)
        else:
            nextWorkingSet.append(e)
            #planes[plane+1].append(e)
    workingSet = nextWorkingSet
    nextWorkingSet = []
    print(workingSet)
    emptyplane = []
    if (len(workingSet) > 0):
        planes.append(emptyplane)
        plane += 1
        print(planes)

j = 1
for p in planes:
    print("(* Plane #" + str(j) +" *)")
    print("AdjacencyGraph[\n")
    planarGraph = Graph(graph.vertices, p)
    print(planarGraph.export_mathematica())
    print('\n\n,GraphLayout->"PlanarEmbedding"]')
    j+=1


#print(planes)
print("Thiccness = " + str(len(planes)))
'''
matrix = graph.get_adj_matrix()
print('ORIG:')
for ar in (matrix).toarray():
	print(*ar)

for i in range(2, 11):
	print()
	print('Path',i,':')
	for ar in (matrix **i).toarray():
		print(*ar)
'''

'''
#-------------------------

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
#g = BipartiteGraph(5, 3)
g = spanTree
w.draw_graph(g)
w.show_edge_crossings(g)
'''

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
'''
