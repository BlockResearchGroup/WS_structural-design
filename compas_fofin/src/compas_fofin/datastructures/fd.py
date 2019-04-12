from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.rpc import Proxy
numerical = Proxy('compas.numerical')


__all__ = ['cablenet_fd']


def cablenet_fd(cablenet):
    xyz   = cablenet.get_vertices_attributes('xyz')
    edges = list(cablenet.edges())
    fixed = list(cablenet.vertices_where({'is_anchor': True}))
    q     = cablenet.get_edges_attribute('q', 1.0)
    loads = cablenet.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))

    xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

    for key, attr in cablenet.vertices(True):
        cablenet.set_vertex_attributes(key, 'xyz', xyz[key])
        cablenet.set_vertex_attributes(key, ('rx', 'ry', 'rz'), r[key])

    for index, (u, v, attr) in enumerate(cablenet.edges(True)):
        attr['f'] = f[index][0]
        attr['l'] = l[index][0]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
