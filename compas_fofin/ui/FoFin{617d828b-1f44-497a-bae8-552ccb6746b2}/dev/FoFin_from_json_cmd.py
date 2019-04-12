from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc

import compas_fofin
from compas_fofin.datastructures import Cablenet
from compas_fofin.rhino import CablenetArtist


__commandname__ = "FoFin_from_json"


def RunCommand(is_interactive):
    if "FoFin" not in sc.sticky:
        raise Exception("Initialise the plugin first!")

    settings = sc.sticky["FoFin"]['settings']

    filepath = compas_rhino.browse_for_file()
    if not filepath:
        return

    if not filepath.endswith('.json'):
        return

    cablenet = Cablenet.from_json(filepath)

    sc.sticky["FoFin"]["cablenet"] = cablenet

    artist = CablenetArtist(cablenet, layer=settings['layer'])
    artist.clear_layer()
    artist.draw_mesh()
    artist.draw_vertices()
    artist.draw_edges()
    artist.redraw()



# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    RunCommand(True)
