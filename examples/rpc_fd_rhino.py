import os
from compas.datastructures import Mesh
from compas.rpc import Proxy
from compas_rhino.artists import MeshArtist

# path to the sample file
DATA = os.path.join(os.path.dirname(__file__), '..', 'data')
FILE = os.path.join(DATA, 'faces.obj')

# the proxy server for remote procedure calls to compas.numerical
proxy = Proxy('compas.numerical')

# make a mesh
mesh = Mesh.from_obj(FILE)

# update default vertex attributes
mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
mesh.update_default_edge_attributes({'q': 1.0})

# numerical data
xyz   = mesh.get_vertices_attributes('xyz')
edges = list(mesh.edges())
fixed = list(mesh.vertices_where({'vertex_degree': 2}))
q     = mesh.get_edges_attribute('q', 1.0)
loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))

# call to fd_numpy over proxy server
xyz, q, f, l, r = proxy.fd_numpy(xyz, edges, fixed, q, loads)

# update the mesh vertices
for key, attr in mesh.vertices(True):
    mesh.set_vertex_attributes(key, 'xyz', xyz[key])
    mesh.set_vertex_attributes(key, ('rx', 'ry', 'rz'), r[key])

# update the mesh edges
for index, (u, v, attr) in enumerate(mesh.edges(True)):
    attr['f'] = f[index][0]
    attr['l'] = l[index][0]

# visualise the result
artist = MeshArtist(mesh, layer="Mesh::FD")
artist.clear_layer()
artist.draw_vertices()
artist.draw()
