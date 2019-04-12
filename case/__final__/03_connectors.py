from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import add_vectors
from compas.geometry import scale_vector


mesh = Mesh.from_json('cablenet.json')

boundary = set(mesh.vertices_on_boundary())

connectors = []

# make a connector for every unconstrained ("normal", "internal" vertices) that is not on the boundary

for key, attr in mesh.vertices(True):
    # skip vertices on the boundary
    if key in boundary:
        continue

    # skip vertices that have a constraint
    if attr['constraint']:
        continue

    # start and end point of the connector
    p1 = mesh.vertex_coordinates(key)
    n = mesh.vertex_normal(key)
    p2 = add_vectors(p1, scale_vector(n, (0.02 + 0.06 + 0.1 + 0.03 + 0.2 + 0.02)))

    # connector "pipe" drawing data as a dict
    connectors.append({
        'points' : [p1, p2],
        'color'  : (255, 0, 0),
        'name'   : "connector.{}".format(key),
        'radius' : 0.0025
    })

compas_rhino.xdraw_pipes(connectors, layer="Connectors", clear=True)
