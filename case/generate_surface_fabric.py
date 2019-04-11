from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_hilo

from compas.utilities import pairwise

from compas.datastructures import mesh_flip_cycles
from compas_hilo.datastructures import Shell
from compas_hilo.rhino import ShellArtist

base = Shell.from_json(compas_hilo.get('geometry_correctednormals.json'))

idos = base.copy()
idos.name = 'c1_idos'

key_xyz = {key: base.vertex_coordinates(key) for key in base.vertices()}
key_normal = {key: base.vertex_normal(key) for key in base.vertices()}

for key, attr in idos.vertices(True):

    x, y, z = key_xyz[key]
    nx, ny, nz = key_normal[key]

    if attr['nx'] is not None:
        nx = attr['nx']
    if attr['ny'] is not None:
        ny = attr['ny']
    if attr['nz'] is not None:
        nz = attr['nz']

    attr['x'] = x + 0.02 * nx
    attr['y'] = y + 0.02 * ny
    attr['z'] = z + 0.02 * nz

idos.to_json(compas_hilo.get('c1_idos.json'))

artist = ShellArtist(idos, layer="Shell::Surfaces::c1-Idos")
artist.clear_layer()
artist.draw_mesh()
artist.draw_vertices()
artist.redraw()
