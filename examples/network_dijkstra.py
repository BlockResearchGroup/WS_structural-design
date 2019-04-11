import os
from compas.utilities import pairwise
from compas.datastructures import Network
from compas.topology import dijkstra_path
from compas.plotters import NetworkPlotter

# path to the sample file
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE = os.path.join(DATA, 'grid_irregular.obj')

# make network from sample file
network = Network.from_obj(FILE)

# make a dictionary of edge weights
weight = {(u, v): network.edge_length(u, v) for u, v in network.edges()}

# add the same weight in both directions
weight.update({(v, u): weight[(u, v)] for u, v in network.edges()})

# set high weights for some specific edges
weight[(5, 7)] = 1000
weight[(7, 5)] = 1000
weight[(18, 1)] = 1000
weight[(1, 18)] = 1000

# specify start and end
start = 21
end = 19

# compute the shortest path taking into account the edge weights
path = dijkstra_path(network.adjacency, weight, start, end)

# convert the path to network edges
edges = [(v, u) if not network.has_edge(u, v) else (u, v) for u, v in pairwise(path)]

# make a plotter
plotter = NetworkPlotter(network, figsize=(10, 7))

# set default font sizes
plotter.defaults['vertex.fontsize'] = 6
plotter.defaults['edge.fontsize'] = 6

# draw the vertices
plotter.draw_vertices(
    text='key',
    facecolor={key: '#ff0000' for key in (path[0], path[-1])},
    radius=0.15
)

# set the edge widths and colors
color = {}
width = {}
text  = {}
for uv in network.edges():
    if uv in edges:
        color[uv] = '#ff0000'
        width[uv] = 5.0
    elif weight[uv] > 100:
        color[uv] = '#00ff00'
        width[uv] = 5.0
        text[uv] = weight[uv]

# draw the edges
plotter.draw_edges(color=color, width=width, text=text)

# show the plot
plotter.show()
