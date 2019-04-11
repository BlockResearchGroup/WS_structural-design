from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial
from math import pi

import compas_rhino
import compas_hilo

from compas.utilities import pairwise
from compas.datastructures import mesh_flip_cycles
from compas.datastructures import Mesh
from compas.geometry import offset_polygon
from compas.geometry import normal_polygon
from compas.geometry import dot_vectors
from compas.geometry import subtract_vectors
from compas.geometry import add_vectors
from compas.geometry import cross_vectors
from compas.geometry import normalize_vector
from compas.geometry import scale_vector
from compas.geometry import Frame
from compas.geometry import intersection_line_plane
from compas.geometry import rotate_points

from compas.utilities import red, green, blue, yellow, cyan, white, black

from compas_rhino.artists import MeshArtist

from compas_hilo.datastructures import Shell
from compas_hilo.rhino import ShellArtist


# ==============================================================================
# Parameters
# ==============================================================================

OFFSET = 0.03

# ==============================================================================
# Helper functions
# ==============================================================================

def on_constraint(X, key, attr):
    constraint = attr['constraint']
    if not constraint:
        return False
    if isinstance(constraint, (tuple, list)):
        if any(c == X for c in constraint):
            return True
    else:
        if constraint == X:
            return True
    return False


on_G_SE = partial(on_constraint, 'G_SE')
on_G_ES = partial(on_constraint, 'G_ES')
on_G_EN = partial(on_constraint, 'G_EN')
on_G_NE = partial(on_constraint, 'G_NE')
on_G_N  = partial(on_constraint, 'G_N')
on_G_NW = partial(on_constraint, 'G_NW')
on_G_WN = partial(on_constraint, 'G_WN')
on_G_SW = partial(on_constraint, 'G_SW')

on_B_SE = partial(on_constraint, 'B_SE')
on_B_ES = partial(on_constraint, 'B_ES')
on_B_EN = partial(on_constraint, 'B_EN')
on_B_NE = partial(on_constraint, 'B_NE')
on_B_N  = partial(on_constraint, 'B_N')
on_B_NW = partial(on_constraint, 'B_NW')
on_B_WN = partial(on_constraint, 'B_WN')
on_B_WS = partial(on_constraint, 'B_WS')
on_B_SW = partial(on_constraint, 'B_SW')

on_S_E  = partial(on_constraint, 'S_E')
on_S_NE = partial(on_constraint, 'S_NE')
on_S_NW = partial(on_constraint, 'S_NW')
on_S_W  = partial(on_constraint, 'S_W')
on_S_S  = partial(on_constraint, 'S_S')


def sorted_vertices(vertices, name):
    vertices = list(vertices)
    start = where(vertices, name)
    index = vertices.index(start)
    vertices.pop(index)
    chain = [start]
    while vertices:
        for index, key in enumerate(vertices):
            nbrs = idos.vertex_neighbors(key)
            if chain[-1] in nbrs:
                chain.append(key)
                vertices.pop(index)
                break
    return chain


def where(keys, name):
    for key in keys:
        constraint = idos.get_vertex_attribute(key, 'constraint')
        if isinstance(constraint, (tuple, list)):
            if any(c == name for c in constraint):
                return key


def frame(chain):
    sp = idos.get_vertex_attributes(chain[0], 'xyz')
    ep = idos.get_vertex_attributes(chain[-1], 'xyz')
    sp[2] = 0.0
    ep[2] = 0.0
    u = normalize_vector(subtract_vectors(ep, sp))
    v = [0.0, 0.0, 1.0]
    w = normalize_vector(cross_vectors(u, v))
    return [u, v, w]

# ==============================================================================
# Extrados
# ==============================================================================

idos = Shell.from_json(compas_hilo.get('c1_idos.json'))

# ==============================================================================
# Rebar
# ==============================================================================

connectors = []

boundary = set(idos.vertices_on_boundary())

for key, attr in idos.vertices(True):

    if key in boundary:
        continue

    constraint = attr['constraint']
    if constraint:
        continue

    p1 = idos.vertex_coordinates(key)
    n = idos.vertex_normal(key)
    p2 = add_vectors(p1, scale_vector(n, (0.06 + 0.1 + 0.03 + 0.2 + 0.02)))

    connectors.append({
        'points' : [p1, p2],
        'color'  : red,
        'name'   : "connector.{}".format(key),
        'radius' : 0.0025
    })

compas_rhino.xdraw_pipes(connectors, layer="Shell::Connectors", clear=True, redraw=True)
