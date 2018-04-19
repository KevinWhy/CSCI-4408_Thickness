# CSCI-4408_Thickness
This is an experiment in trying to find the thickness of a graph. The code was very quickly written, so it is very... disorganized.

## Concept:
1. Weigh the edges based on how "busy" that part of the graph is.
2. Assumption: High degree vertices have a lot of edges nearby, so it's very "busy"... That vertex probably contributes to an edge crossing.
3. So... create a minimum spanning tree with these weights
4. Then add all the lowest weight edges possible... that don't create edge crossings.
5. Repeat Step 4 on another plane... until all edges have been added.

## To use:
1. Run test.py and pipe the output to a file.
2. Copy the contents of that file into a cell inside Mathematica.
3. Run that cell. Mathematica will display the planar graphs, and the resulting thickness of the graph.
