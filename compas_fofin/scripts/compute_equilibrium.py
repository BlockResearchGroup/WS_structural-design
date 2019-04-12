from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas_rhino
import compas_fofin

from compas_fofin.datastructures import Cablenet
from compas_fofin.datastructures import cablenet_fd

from compas_fofin.rhino import CablenetArtist
from compas_fofin.rhino import CablenetHelper


def draw():
    artist.clear_layer()
    artist.draw_vertices(color={key: (255, 0, 0) for key in cablenet.vertices_where({'is_anchor': True})})
    artist.draw_edges()
    artist.redraw()


cablenet = Cablenet.from_obj(compas.get('faces.obj'))

for key, attr in cablenet.vertices(True):
    attr['is_anchor'] = cablenet.vertex_degree(key) == 2

artist = CablenetArtist(cablenet, layer="Mesh::FD")


draw()


while True:
    selected = CablenetHelper.select_vertices(cablenet)
    if not selected:
        break

    if CablenetHelper.update_vertex_attributes(cablenet, selected):
        cablenet_fd(cablenet)
        draw()

while True:
    selected = CablenetHelper.select_edges(cablenet)
    if not selected:
        break

    if CablenetHelper.update_edge_attributes(cablenet, selected):
        cablenet_fd(cablenet)
        draw()

draw()
