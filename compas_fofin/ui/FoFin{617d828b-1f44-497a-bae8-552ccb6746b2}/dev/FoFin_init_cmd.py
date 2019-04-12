from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_fofin


__commandname__ = "FoFin_init"


def RunCommand(is_interactive):
    sc.sticky["FoFin"] = {
        'cablenet' : None,
        'settings' : {
            'scale.reactions' : 0.1,
            'layer' : "FoFin::Cablenet"
        }
    }


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
