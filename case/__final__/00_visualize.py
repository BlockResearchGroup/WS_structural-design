from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier
from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector


mesh = Mesh.from_json('../cablenet.json')

vertexcolor = {key: (255, 0, 0) for key in mesh.vertices_where({'is_anchor': True})}
edgecolor = {key: (255, 0, 0) for key in mesh.edges_where({'is_joint': True})}

artist = MeshArtist(mesh, layer="Cablenet")

artist.clear_layer()
artist.draw_vertices(color=vertexcolor)
artist.draw_edges(color=edgecolor)
artist.redraw()

# select mesh vertices
# update the attributes
# redraw mesh if successful
while True:
    selected = VertexSelector.select_vertices(mesh)
    if not selected:
        break

    if VertexModifier.update_vertex_attributes(mesh, selected):
        artist.clear_layer()
        artist.draw_vertices(color=vertexcolor)
        artist.draw_edges(color=edgecolor)

# select mesh edges
# update the attributes
# redraw mesh if successful
while True:
    selected = EdgeSelector.select_edges(mesh)
    if not selected:
        break
    if EdgeModifier.update_edge_attributes(mesh, selected):
        artist.clear_layer()
        artist.draw_vertices(color=vertexcolor)
        artist.draw_edges(color=edgecolor)
