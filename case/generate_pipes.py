from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial

import compas_hilo

from compas.utilities import pairwise
from compas.utilities import flatten
from compas.geometry import centroid_points
from compas.datastructures import mesh_flip_cycles
from compas.datastructures import Mesh
from compas_rhino.artists import MeshArtist

# ==============================================================================
# Helper functions
# ==============================================================================

def on_support(name, key, attr):
    constraint = attr['constraint']
    if constraint:
        if isinstance(constraint, (tuple, list)):
            if any(c == name for c in constraint):
                return True
        else:
            if constraint == name:
                return True
    return False


def find_start(mesh, keys, name):
    start = None
    for key in keys:
        constraint = mesh.get_vertex_attribute(key, 'constraint')
        if isinstance(constraint, (tuple, list)):
            if constraint[0] == name or constraint[1] == name:
                start = key
                break
    return start


def sorted_vertices(mesh, name_set, name_a, name_b):
    keys = list(mesh.vertices_where_predicate(partial(on_support, name_set)))
    key = find_start(mesh, keys, name_a)
    vertices = [key]
    stop = False
    while not stop:
        key = vertices[-1]
        nbrs = mesh.vertex_neighbors(key)
        for nbr in nbrs:
            if mesh.halfedge[key][nbr] is None:
                vertices.append(nbr)
                constraint = mesh.get_vertex_attribute(nbr, 'constraint')
                if isinstance(constraint, (tuple, list)):
                    if name_b in constraint:
                        stop = True
                break
    return vertices


def find_faces(mesh, vertices):
    faces = []
    for a, b in pairwise(vertices):
        faces.append([])
        while True:
            if mesh.get_edge_attribute((a, b), 'is_joint'):
                break
            fkey = mesh.halfedge[b][a]
            faces[-1].append(fkey)
            a = mesh.face_vertex_descendant(fkey, a)
            b = mesh.face_vertex_ancestor(fkey, b)
    return faces


def find_cycle(mesh, vertices, tovisit):
    cycle = []
    c, d = vertices[:2]
    while tovisit:
        a, b = d, c
        fkey = mesh.halfedge[a][b]
        if fkey not in tovisit:
            fkey = cycle[-1][0]
            c = a
            d = mesh.face_vertex_descendant(fkey, a)
        else:
            c = mesh.face_vertex_descendant(fkey, b)
            d = mesh.face_vertex_descendant(fkey, c)
            tovisit.remove(fkey)
            cycle.append((fkey, (a, b)))
    return cycle

# ==============================================================================
# Load mesh
# ==============================================================================

mesh = Mesh.from_json(compas_hilo.get('c1-3cm_edos.json'))

# ==============================================================================
# Zones
# ==============================================================================

zones = []

for name_set, name_a, name_b in [('S_NW', 'G_NW', 'G_N'), ('S_NE', 'G_N', 'G_NE'), ('S_S', 'G_SE', 'G_SW'), ('S_W', 'G_SW', 'G_WN')]:

    vertices = sorted_vertices(mesh, name_set, name_a, name_b)
    faces = find_faces(mesh, vertices)

    tovisit = set(flatten(faces))
    for u, v in pairwise(vertices[1:]):
        fkey = mesh.halfedge[v][u]
        tovisit.remove(fkey)

    cycle = find_cycle(mesh, vertices, tovisit)

    points = []
    for fkey, (u, v)  in cycle:
        points.append(centroid_points([mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)]))
        points.append(mesh.face_centroid(fkey))

    zones.append([vertices, faces, points])

# ==============================================================================
# Visualisation
# ==============================================================================

colors = [
    (255, 0, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 255, 255),
    (0, 0, 255)
]

vertexcolor = {}
vertexcolor.update({key: (0, 0, 0) for key in mesh.vertices_where({'is_anchor': True})})

edgecolor = {}
edgecolor.update({key: (0, 0, 0) for key in mesh.edges_where({'is_joint': True})})

facecolor = {}
polylines = []

for i, zone in enumerate(zones):
    vertices, faces, points = zone
    polylines.append({
        'points' : points,
        'color'  : colors[-1]
    })
    facecolor.update({key: colors[i] for key in flatten(faces)})
    vertexcolor.update({key: colors[i] for key in vertices})

artist = MeshArtist(mesh)
artist.layer = "Shell::Surfaces::Zones"
artist.clear_layer()
artist.draw_faces(color=facecolor)
artist.draw_edges(keys=list(mesh.edges_where({'is_joint': True})), color=edgecolor)
artist.layer = "Shell::Pipes"
artist.clear_layer()
artist.draw_polylines(polylines)
artist.redraw()
