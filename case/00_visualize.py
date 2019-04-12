from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector


mesh = Mesh.from_json('cablenet.json')


artist = MeshArtist(mesh, layer="Cablenet")

artist.clear_layer()
artist.draw_vertices()
artist.draw_edges()
artist.redraw()

edges = EdgeSelector.select_edges(mesh)
if edges:
    if EdgeModifier.update_edge_attributes(mesh, edges):
        artist.clear_layer()
        artist.draw_vertices()
        artist.draw_edges()

