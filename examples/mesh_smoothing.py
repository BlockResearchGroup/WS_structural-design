import os
from compas.datastructures import Mesh
from compas.datastructures import mesh_smooth_centroid
from compas_plotters import MeshPlotter


# make a callback
def update_plot(k, args):
    plotter.update_vertices()
    plotter.update_edges()
    plotter.update_faces()
    plotter.update(pause=0.001)


# path to the sample file
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE = os.path.join(DATA, 'faces.obj')

# make a mesh
mesh = Mesh.from_obj(FILE)

# identify fixed points
fixed = list(mesh.vertices_where({'vertex_degree': 2}))

# make a plotter
plotter = MeshPlotter(mesh, figsize=(10, 7))

# draw the original configuration
plotter.draw_vertices(facecolor={key: '#ff0000' for key in fixed})
plotter.draw_edges()
plotter.draw_faces()

# smooth with dynamic viz
mesh_smooth_centroid(mesh, fixed=fixed, kmax=100, callback=update_plot)

# keep plot alive
plotter.show()
