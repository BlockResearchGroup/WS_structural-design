import os
from compas.datastructures import Network
from compas.plotters import NetworkPlotter
from compas.topology import shortest_path
from compas.utilities import pairwise


# wrapper for the shortest path function
def shortest_path_to(end):
    if start == end:
        return
    path = shortest_path(network.adjacency, start, end)
    edges = [(v, u) if not network.has_edge(u, v) else (u, v) for u, v in pairwise(path)]
    plotter.clear_vertices()
    plotter.clear_edges()
    plotter.draw_vertices(facecolor={start: '#ff0000', end: '#ff0000'}, radius=0.15, picker=10)
    plotter.draw_edges(color={uv: '#ff0000' for uv in edges}, width={uv: 5.0 for uv in edges})
    plotter.update()


# callback for the pick event
def onpick(event):
    index = event.ind[0]
    shortest_path_to(index)


# path to the sample file
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE = os.path.join(DATA, 'grid_irregular.obj')

# load a network from an OBJ file
network = Network.from_obj(FILE)

# define the starting point
start = 21

# create plotter
# draw the original configuration
# register the pick callback
# show the viewer
plotter = NetworkPlotter(network, figsize=(10, 7))
plotter.draw_vertices(facecolor={start: '#ff0000'}, radius=0.15, picker=10)
plotter.draw_edges()
plotter.register_listener(onpick)
plotter.show()
