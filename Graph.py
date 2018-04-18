# Defines the vertices, and edges in a graph.
# Competition Graphs: K5, K8, K9,
# other graphs
#
# numpy, scipy for Windows can be downloaded from:
#	https://www.lfd.uci.edu/~gohlke/pythonlibs/

import math
import json
import scipy
import planarity
from scipy.sparse import lil_matrix


# ------------------------------------

def EdgesFromIndices(verts, edgeList):
    ''' Creates edges between vertices with the given indices.
			edgeList = list of tuples: (v1, v2)
		Returns the list created.
	'''
    return [
        Edge(verts[edgeTuple[0]], verts[edgeTuple[1]])
        for edgeTuple in edgeList
    ]


# ------------------------------------

def TetrahedralGraph():
    ''' Returns the tetrahedral graph: Planar K4 '''
    verts = [
        Vertex(50, 250), Vertex(250, 250),
        Vertex(150, 50), Vertex(150, 175)
    ]
    edges = EdgesFromIndices(verts, [
        (0, 1), (1, 2), (2, 0),  # Outer cycle
        (0, 3), (1, 3), (2, 3),  # All connected to inside node
    ])
    return Graph(verts, edges)


def Kn(n):
    ''' Returns the graph: Kn '''
    # Make vertices (arranged in a circle, starting from top & going clockwise)
    verts = []
    radius = 100
    angle = -math.pi / 2  # Initial angle. Note: 0,0 = top-left... so -degree = counter-clockwise
    centerX, centerY = 200, 150
    angleIncrement = math.pi * 2 / n
    verts = [
        Vertex(
            radius * math.cos(angleIncrement * i) + centerX,  # x
            radius * math.sin(angleIncrement * i) + centerY  # y
        )
        for i in range(0, n)
    ]
    # Make edges
    edges = []
    for index1, v1 in enumerate(verts):
        for v2 in verts[index1 + 1:]:
            edges.append(Edge(v1, v2))
    return Graph(verts, edges)


def BipartiteGraph(n, m):
    # First set = top row
    startX = 5
    lastX = 495
    startY = 250 - 50
    offsetX = (lastX - startX) / n
    vertsA = [
        Vertex(offsetX * i + startX, startY)
        for i in range(0, n)
    ]
    # Second set = next row
    offsetX = (lastX - startX) / m
    startY = 250 + 50
    vertsB = [
        Vertex(offsetX * i + startX, startY)
        for i in range(0, n)
    ]
    # Connect all vertsA to vertsB
    edges = [
        Edge(vertA, vertB)
        for vertB in vertsB
        for vertA in vertsA
    ]
    return Graph(vertsA + vertsB, edges)


def GraphData(graphName):
    '''
		Reads the graph with the given name from CompetitionGraphs.json
		Note: The graphs do NOT have positions, so they can't be drawn yet.
	'''
    with open('CompetitionGraphs.json') as graphJson:
        graphsJson = json.load(graphJson)[graphName]
    num_verts = graphsJson.get('verts', None)
    if num_verts is not None:
        vertices = [Vertex() for i in range(num_verts)]
        edgeIndices = [
            (edge[0] - 1, edge[1] - 1)  # Convert the 1-based index to 0-based index
            for edge in graphsJson['edges']
        ]
        return Graph(vertices, EdgesFromIndices(vertices, edgeIndices))
    else:
        vertexDict = {}
        edgeIndices = []
        maxIndex = -1
        # Read list of vertices
        for edge in graphsJson['edges']:
            v1Index = edge[0] - 1
            v2Index = edge[1] - 1
            edgeIndices.append(v1Index, v2Index)
            maxIndex = max(v1Index, v2Index, maxIndex)
            if vertexDict.get(v1Index, None) is None:
                vertexDict[v1Index] = Vertex()
            if vertexDict.get(v2Index, None) is None:
                vertexDict[v2Index] = Vertex()

        # Convert dictionary to list
        vertices = []
        for i in range(maxIndex):
            vertices.append(vertexDict.get(i, None))
        edges = EdgesFromIndices(vertices, edgeIndices)
        return Graph(vertices, edges)


# ------------------------------------

def prims_alg(graph, edgeWeights):
    # Weird way to get first vertex in graph
    firstVert = None
    for vert in graph.vertices:
        firstVert = vert
        break

    used_verts = [firstVert]
    used_edges = []
    while len(used_edges) < len(graph.vertices) - 1:
        # Add one edge in every iteration of the outer loop
        for edgeInfo in sorted(edgeWeights.items(), key=lambda edgeInfo: edgeInfo[1]):
            edge = edgeInfo[0]
            if ((edge.vert1 not in used_verts and edge.vert2 in used_verts)
                or (edge.vert1 in used_verts and edge.vert2 not in used_verts)
                ):  # Only one of the edges is in the used_verts...
                # Add it to the list
                used_verts.append(edge.vert1)
                used_verts.append(edge.vert2)
                used_edges.append(edge)
                break  # Restart loop
    return used_edges


# ------------------------------------

class Vertex:
    # Defaults
    radius = 10
    color = "lightgray"

    def __init__(self, x=None, y=None, label=None, radius=None, color=None):
        self.x = x
        self.y = y
        self.label = label
        if color:
            self.color = color
        if radius and radius >= 0:
            self.radius = radius


class Edge:
    # Defaults
    width = 3
    color = "black"
    vert1 = 0
    vert2 = 0

    def __init__(self, vert1, vert2, width=None, color=None):
        self.vert1 = vert1
        self.vert2 = vert2
        if color:
            self.color = color
        if width and width >= 0:
            self.width = width


class EdgeFormula:
    ''' y = mx + b '''

    def __init__(self, edge):
        # Vertices are stored instead of coordinates because want to check if endpoints are the same...
        # and don't want to check if floats are equal. (since floats aren't stored precisely)
        self.vert1 = edge.vert1
        self.vert2 = edge.vert2
        # The y's are used for edge cases, x's for Sweep line algorithm
        self.minX = min(edge.vert1.x, edge.vert2.x)
        self.maxX = max(edge.vert1.x, edge.vert2.x)
        self.minY = min(edge.vert1.y, edge.vert2.y)
        self.maxY = max(edge.vert1.y, edge.vert2.y)
        # Find m & b
        try:
            self.m = (edge.vert2.y - edge.vert1.y) / (edge.vert2.x - edge.vert1.x)
            self.b = -self.m * edge.vert1.x + edge.vert1.y  # b = -mx +y
        except ZeroDivisionError:  # If vertical line...
            self.m = None
            self.b = None

    def isEndpoint(self, vert):
        ''' Checks if given point is an endpoint of this line. '''
        return self.vert1 == vert or self.vert2 == vert

    def inYBounds(self, other):
        ''' Checks if both EdgeFormulas fit in same y-range. '''
        return self.minY <= other.maxY and self.maxY <= other.minY

    def intersects(self, other):
        ''' other = EdgeFormula
		'''
        # Special case: Ignore the endpoints
        if other.isEndpoint(self.vert1) or other.isEndpoint(self.vert2):
            return None

        if self.m is not None and other.m is not None:  # Both lines not vertical
            ''' Work:
				Line 1 = self, Line 2 = other
				 m1 * x + b1 = m2 * x + b2
				(m1 -m2)*x = b2 -b1
			'''
            try:
                # General case
                intersectX = (other.b - self.b) / (self.m - other.m)
                intersectY = self.m * intersectX + self.b
                if self.minY <= intersectY and intersectY <= self.maxY:
                    return (intersectX, intersectY)
                return None  # Too short
            except ZeroDivisionError:
                # Only intersects if both on the same line...
                if self.b == other.b and self.inYBounds(other):
                    return (self.vert1.x, self.vert1.y)  # Intersects on many points, return one
                return None  # Not on same line, or segments not long enough

        elif self.m is not None or other.m is not None:  # One line is vertical
            if self.m is not None:  # Other line is vertical
                vertical = other
                diag = self
            else:  # This line is vertical
                vertical = self
                diag = other
            intersectX = vertical.minX
            intersectY = diag.m * intersectX + diag.b  # We know the x, find the y
            if intersectY >= diag.minY and intersectY <= diag.maxY:
                return (intersectX, intersectY)
            return None

        else:  # Both lines are vertical
            if self.inYBounds(other):
                # Many intersection points, return the lowest point on this line
                if self.vert1.y < self.vert2.y:
                    return (self.vert1.x, self.vert1.y)
                else:
                    return (self.vert2.x, self.vert2.y)


class Graph:
    def __init__(self, vertices, edges):
        ''' Assumes that egdes only use vertices in the verts list. '''
        self.vertices = vertices
        self.edges = edges

    def export_mathematica(self):
        out_str = '{'
        first_row = True
        for row in self.get_adj_matrix().toarray():
            if not first_row:
                out_str += ',\n'
            out_str += '{'
            out_str += ','.join([str(int(i)) for i in row])
            out_str += '}'
            first_row = False
        out_str += '}'
        return out_str

    def get_adj_matrix(self):
        # Start with matrix of 0s
        matrix = lil_matrix((len(self.vertices), len(self.vertices)))
        # Fill in matrix from the edges
        vertToIndexDict = {
            vert: index
            for index, vert in enumerate(self.vertices)
        }

        for edge in self.edges:
            index1 = vertToIndexDict[edge.vert1]
            index2 = vertToIndexDict[edge.vert2]
            matrix[index1, index2] = 1
            matrix[index2, index1] = 1
        return matrix.tocsr()

    def edges_as_tuples(self):
        return [
            (edge.vert1, edge.vert2)
            for edge in self.edges
        ]

    def is_planar(self):
        return planarity.is_planar(self.edges_as_tuples())

    def ascii(self):
        return planarity.ascii(self.edges_as_tuples())

    def edgeWeights(self):
        adjMatrix = self.get_adj_matrix().toarray()
        vertDegree = {
            vert: sum(adjMatrix[i, :])
            for i, vert in enumerate(self.vertices)
        }
        return {
            edge: vertDegree[edge.vert1] + vertDegree[edge.vert2]
            for edge in self.edges
        }

    def get_edge_crossings(self):
        '''
			Show all the line intersections.
			Uses Sweep Line Algorithm (https://en.wikipedia.org/wiki/Sweep_line_algorithm)
			to reduce the amount of comparisons done.
		'''
        PROP_ORIG_INDEX = 0  # Index in the edges list
        PROP_EDGE = 1
        PROP_FORMULA = 2
        PROP_CHECK_LIST = 3  # Array of all vertices. value = True if already checked that edge
        edges = [
            (  # Make a tuple for each edge...
                index,
                edge,
                EdgeFormula(edge),
                [edge == other for other in self.edges]  # Already checked against self: No intersection
            ) for index, edge in enumerate(self.edges)
        ]
        '''
		# Sort the mins & maxs, for Sweep Line alg.
		edgesMinX = sorted(
			edges, key = lambda edgeInfo: edgeInfo[PROP_FORMULA].minX
		)
		edgesMaxX = sorted(
			edges, key = lambda edgeInfo: edgeInfo[PROP_FORMULA].maxX
		)
		'''

        intersections = []  # Intersection coords

        def check_intersections(edgeInfo, otherList):
            for otherInfo in otherList:
                if not edgeInfo[PROP_CHECK_LIST][otherInfo[PROP_ORIG_INDEX]]:
                    #					print('check v1:',edgeInfo[PROP_ORIG_INDEX], '__v2:',otherInfo[PROP_ORIG_INDEX])
                    intersection = edgeInfo[PROP_FORMULA].intersects(otherInfo[PROP_FORMULA])
                    if intersection is not None:
                        intersections.append(intersection)
                    #						print('\tINTERSECT. pos:',intersection)
                    # Tell both edges that the intersection has been checked
                    edgeInfo[PROP_CHECK_LIST][otherInfo[PROP_ORIG_INDEX]] = True
                    otherInfo[PROP_CHECK_LIST][edgeInfo[PROP_ORIG_INDEX]] = True

        # Check all pairs of edges
        for edgeInfo in edges:
            check_intersections(edgeInfo, edges)

        '''
		# Sweep Edge Algorithm
		activeEdges = []
		nextMinEdgeInfo = edgesMinX.pop(0)
		nextMaxEdgeInfo = edgesMaxX.pop(0)
		while nextMinEdgeInfo is not None or nextMaxEdgeInfo is not None:
			print('min:',nextMinEdgeInfo and nextMinEdgeInfo[PROP_ORIG_INDEX], '__max:',nextMaxEdgeInfo and nextMaxEdgeInfo[PROP_ORIG_INDEX])
			if nextMinEdgeInfo and (not nextMaxEdgeInfo or nextMinEdgeInfo[PROP_FORMULA].minX <= nextMaxEdgeInfo[PROP_FORMULA].maxX):
				# Add edge to activeEdges
				nextEdgeInfo = nextMinEdgeInfo
				activeEdges.append(nextEdgeInfo)
				check_intersections(nextEdgeInfo, activeEdges)
				if len(edgesMinX) > 0:
					nextMinEdgeInfo = edgesMinX.pop(0)
				else:
					nextMinEdgeInfo = None
				
			elif nextMaxEdgeInfo and (not nextMinEdgeInfo or nextMinEdgeInfo[PROP_FORMULA].minX > nextMaxEdgeInfo[PROP_FORMULA].maxX):
				# Remove edge from activeEdges
				check_intersections(nextEdgeInfo, activeEdges)
				nextEdgeInfo = nextMaxEdgeInfo
				if len(edgesMaxX) > 0:
					nextMaxEdgeInfo = edgesMaxX.pop(0)
				else:
					nextMaxEdgeInfo = None
		'''
        return intersections
