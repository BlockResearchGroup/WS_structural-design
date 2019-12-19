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

# offset the extrados from the intrados
# by 6cm in the direction of the corresponding cablenet vertex normal

# ==============================================================================
# Concrete volume
# ==============================================================================

volume = idos.copy()
volume.name = 'concrete1'

# flip its cycles to make the bottom normals point downwards

# set the key offset
dkey = volume._max_int_key + 1

# add the vertices of the extrados
for key, attr in edos.vertices(True):

# add the faces of the extrados
for fkey in edos.faces():
    vertices = edos.face_vertices(fkey)

# construct a polygon of boundary vertices

# add the "side" faces

# ==============================================================================
# Export and visualisation
# ==============================================================================

# export
volume.to_json('concrete1.json')

# visualize
artist = MeshArtist(volume, layer="Concrete1")
artist.clear_layer()
artist.draw_mesh(color=(0, 0, 255))
