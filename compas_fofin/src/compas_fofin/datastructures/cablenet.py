from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Mesh


__all__ = ['Cablenet']


class Cablenet(Mesh):

    def __init__(self):
        super(Cablenet, self).__init__()
        self.default_vertex_attributes.update({
            'is_anchor': False,
            'rx' : 0.0,
            'ry' : 0.0,
            'rz' : 0.0,
            'px' : 0.0,
            'py' : 0.0,
            'pz' : 0.0
        })
        self.default_edge_attributes.update({
            'q' : 1.0,
            'f' : 0.0,
            'l' : 0.0
        })


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    net = Cablenet()

    print(net)
