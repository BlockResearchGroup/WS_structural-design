import os
from compas.utilities import pairwise
from compas.datastructures import Network
from compas.topology import shortest_path
from compas.plotters import NetworkPlotter

# path to the sample file
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE = os.path.join(DATA, 'grid_irregular.obj')

# make network from sample file
network = Network.from_obj(FILE)

# specify start and end
start = 21
end = 11

# compute the shortest path taking into account the edge weights
path = shortest_path(network.adjacency, start, end)

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

# draw the edges
plotter.draw_edges(
    color={(u, v): '#ff0000' for u, v in edges},
    width={(u, v): 5.0 for u, v in edges}
)

# show the plot
plotter.show()
