from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist


mesh = Mesh.from_json('cablenet.json')

fabric = mesh.copy()
fabric.name = 'fabric'

# make a lookup dict for the vertex normals of the mesh vertices
key_normal = {key: mesh.vertex_normal(key) for key in mesh.vertices()}

for key, attr in fabric.vertices(True):
    nx, ny, nz = key_normal[key]

    # update the attributes of the fabric vertices
    # to be offset in the normal direction by 2cm
    attr['x'] += 0.02 * nx
    attr['y'] += 0.02 * ny
    attr['z'] += 0.02 * nz

fabric.to_json('fabric.json')

artist = MeshArtist(fabric, layer="Fabric")

# clear the "Fabric" layer
# draw the fabric as a mesh
# specify a color for the mesh
artist.clear_layer()
artist.draw_mesh(color=(0, 255, 255))
