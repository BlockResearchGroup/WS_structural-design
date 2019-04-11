from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_hilo

from compas.utilities import pairwise

from compas.datastructures import mesh_flip_cycles
from compas_hilo.datastructures import Shell
from compas_hilo.rhino import ShellArtist

base = Shell.from_json(compas_hilo.get('geometry_correctednormals.json'))
boundary = set(base.vertices_on_boundary())

# create the idos

idos = base.copy()

key_xyz = {key: base.vertex_coordinates(key) for key in base.vertices()}
key_normal = {key: base.vertex_normal(key) for key in base.vertices()}

for key, attr in idos.vertices(True):
    x, y, z = key_xyz[key]
    nx, ny, nz = key_normal[key]

    # use corrected normals if available

    if attr['nx'] is not None:
        nx = attr['nx']
    if attr['ny'] is not None:
        ny = attr['ny']
    if attr['nz'] is not None:
        nz = attr['nz']

    attr['x'] = x + 0.02 * nx
    attr['y'] = y + 0.02 * ny
    attr['z'] = z + 0.02 * nz

# create the edos

edos = idos.copy()

key_xyz = {key: idos.vertex_coordinates(key) for key in idos.vertices()}
key_normal = {key: idos.vertex_normal(key) for key in idos.vertices()}

for key, attr in edos.vertices(True):

    x, y, z = key_xyz[key]
    nx, ny, nz = key_normal[key]

    # use corrected normals if available

    if attr['nx'] is not None:
        nx = attr['nx']
    if attr['ny'] is not None:
        ny = attr['ny']
    if attr['nz'] is not None:
        nz = attr['nz']

    attr['x'] = x + 0.06 * nx
    attr['y'] = y + 0.06 * ny
    attr['z'] = z + 0.06 * nz

# start volume as copy of idos

volume = idos.copy()
volume.name = 'concrete1'

# flip its cycles to make the bottom normals point downwards

mesh_flip_cycles(volume)

# set the key offset

max_int_key = volume._max_int_key + 1
max_int_fkey = volume._max_int_fkey + 1

# add the vertices of the edos

for key, attr in edos.vertices(True):
    volume.add_vertex(key=key + max_int_key, **attr)

# add the faces of the edos

for fkey in edos.faces():
    vertices = edos.face_vertices(fkey)
    vertices = [key + max_int_key for key in vertices]

    volume.add_face(vertices)

# add the side faces

boundary = edos.vertices_on_boundary(ordered=True)
boundary.append(boundary[0])

for a, b in pairwise(boundary):
    volume.add_face([b, a, a + max_int_key, b + max_int_key])

# export

# volume.to_json(compas_hilo.get('concrete1_volume.json'))

# visualize

artist = ShellArtist(volume, layer="Shell::Volumes::Concrete1")
artist.clear_layer()
artist.draw_mesh()
artist.redraw()
