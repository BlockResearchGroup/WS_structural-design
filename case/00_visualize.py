from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist


mesh = Mesh.from_json('cablenet.json')

vertexcolor = {key: (255, 0, 0) for key in mesh.vertices_where({'is_anchor': True})}
edgecolor = {key: (0, 0, 255) for key in mesh.edges_where({'is_joint': True})}

artist = MeshArtist(mesh, layer="Cablenet")

artist.clear_layer()
artist.draw_vertices(color=vertexcolor)
artist.draw_edges(color=edgecolor)

