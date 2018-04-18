import tkinter as tk
from Graph import *
import operator
from operator import itemgetter
from GraphCanvas import GraphCanvas

def mathematica_comment_print(*args, **kwargs):
    print('(*', *args, '*)', *kwargs)

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
    #print(spanTree.export_mathematica())
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
    for p in planes:
        mathematica_comment_print("Plane #" + str(j))
        print("AdjacencyGraph[\n")
        planarGraph = Graph(graph.vertices, p)
        print(planarGraph.export_mathematica())
        print('\n,GraphLayout->"PlanarEmbedding"]')
        j+=1
    
    
    #print(planes)
    print('Print["',  "Thiccness = " + str(len(planes))  ,'"]')


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

for graphName in GRAPH_DATA_NAMES:
    mathematica_comment_print(graphName +':')
    mathematica_comment_print('--------------------')
    thickness_solver(GraphData(graphName))
    print('\n\n')
