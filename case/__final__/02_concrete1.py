from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.utilities import pairwise

from compas.datastructures import mesh_flip_cycles
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist


mesh = Mesh.from_json('cablenet.json')

# make lookup dicts for vertex normals of the cablenet
key_normal = {key: mesh.vertex_normal(key) for key in mesh.vertices()}

# ==============================================================================
# Intrados and extrados
# ==============================================================================

idos = mesh.copy()
edos = idos.copy()

# offset the intrados from the cablenet
# by 2cm in the direction of the corresponding cablenet vertex normal
for key, attr in idos.vertices(True):
    nx, ny, nz = key_normal[key]

    attr['x'] += 0.02 * nx
    attr['y'] += 0.02 * ny
    attr['z'] += 0.02 * nz

# offset the intrados from the intrados
# by 2cm in the direction of the corresponding cablenet vertex normal
for key, attr in edos.vertices(True):
    nx, ny, nz = key_normal[key]

    attr['x'] += 0.06 * nx
    attr['y'] += 0.06 * ny
    attr['z'] += 0.06 * nz

# ==============================================================================
# Concrete volume
# ==============================================================================

volume = idos.copy()
volume.name = 'concrete1'

# flip its cycles to make the bottom normals point downwards
mesh_flip_cycles(volume)

# set the key offset
dkey = volume._max_int_key + 1

# add the vertices of the extrados
for key, attr in edos.vertices(True):
    volume.add_vertex(key=key + dkey, **attr)

# add the faces of the extrados
for fkey in edos.faces():
    vertices = edos.face_vertices(fkey)
    vertices = [key + dkey for key in vertices]

    volume.add_face(vertices)

# construct a polygon of boundary vertices
boundary = edos.vertices_on_boundary(ordered=True)
boundary.append(boundary[0])

# add the "side" faces
for a, b in pairwise(boundary):
    volume.add_face([b, a, a + dkey, b + dkey])

# ==============================================================================
# Export and visualisation
# ==============================================================================

# export
volume.to_json('concrete1.json')

# visualize
artist = MeshArtist(volume, layer="Concrete1")
artist.clear_layer()
artist.draw_mesh(color=(0, 0, 255))
