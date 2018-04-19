'''
test.py

This is an experiment to find the thickness of graphs.
It reads some graphs, and outputs the planar subgraphs that result in a thickness.

To use:
1. Run this code, and pipe the output to a file.
2. Copy the contents of the output file into a cell inside Mathematica.
3. Run that cell.
'''

import tkinter as tk
from Graph import *
import operator
from operator import itemgetter
from GraphCanvas import GraphCanvas

def mathematica_comment_print(*args, **kwargs):
    print('(*', *args, '*)', *kwargs)
def mathematica_string_print(*args, **kwargs):
    args = [
        str.replace('"', '\\"')
        for str in args
    ]
    print('Print["', *args, '"]', *kwargs)

#-------------------------

#graph = GraphData('graph1')
graph = Kn(6)
#verts = [Vertex() for i in range(10)]
#edges = EdgesFromIndices(verts, [
#	(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,9), (9,0),
#	(0,5)
#])
#graph = Graph(verts, edges)

def thickness_solver(graph):
    workingSet = []
    nextWorkingSet = []
    planes = [[]]
    plane = 0
    weights = graph.edgeWeights()
    usedEdges = prims_alg(graph,weights)
    spanTree = Graph(graph.vertices, usedEdges)
    sortedWeights = sorted(weights.items(), key=itemgetter(1), reverse=False)
    
    #print('planar?',spanTree.is_planar())
    #mathematica_string_print('_____TREE____')
    #print(spanTree.export_mathematica())
    #mathematica_string_print('___________')
    #print(sortedWeights)
    
    for u in usedEdges:
        planes[plane].append(u)
    
    #print(planes)
    
    for w in sortedWeights:
        if not (w[0] in usedEdges):
            workingSet.append(w[0])
    
    #print(workingSet)
    
    while (len(workingSet) > 0):
        #i = len(workingSet)
        while (len(workingSet) > 0):
            e = workingSet.pop()
            i = len(workingSet)
            #print(i)
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
        #print(workingSet)
        emptyplane = []
        if (len(workingSet) > 0):
            planes.append(emptyplane)
            plane += 1
            #print(planes)
    
    j = 1
    print('{')
    for p in planes:
        if j > 1:
            print(',')
        planarGraph = Graph(graph.vertices, p)
        print(planarGraph.export_mathematica())
        j+=1
    print('}')
    
    
    #print(planes)
    mathematica_string_print("Thiccness = " + str(len(planes)))


'''
# Test on K3,3 (WORKS)
thickness_solver(BipartiteGraph(3,3))

# Test on K4 - 11 (WORKS)
for i in range(4, 12):
    print('K'+ str(i) +':')
    print('--------------------')
    thickness_solver(Kn(i))
    print('\n\n')
'''

# Test on some inflations of a tree
v = [Vertex() for i in range(10)]
e = EdgesFromIndices(v, [
    (0,1), (1,2), (2,4), (4,6), (6,8), (6,9),
    (0,3), (3,7),
    (2,5)
])
g = Graph(v, e)
for r in range(1, 11):
    mathematica_string_print('inflate #'+ str(r) +':')
    mathematica_comment_print('--------------------')
    thickness_solver(inflate(g, r))
    mathematica_string_print('---------------------')
    print('\n\n')

#-------------------------------#

# Competition graphs were the ones in the JSON... & K5, 8, 9
graphs = {
    'K' +str(i): Kn(i)
    for i in [5, 8, 9]
}
for graphName in GRAPH_DATA_NAMES:
    graphs[graphName] = GraphData(graphName)

for graphName, graph in graphs.items():
    mathematica_string_print(graphName +':')
    mathematica_comment_print('--------------------')
    thickness_solver(graph)
    mathematica_string_print('---------------------')
    print('\n\n')
