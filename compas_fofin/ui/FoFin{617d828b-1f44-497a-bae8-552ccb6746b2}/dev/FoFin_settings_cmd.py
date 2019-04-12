from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc
import compas_rhino

from compas_fofin.rhino import CablenetArtist


__commandname__ = "FoFin_settings"


def RunCommand(is_interactive):
    if "FoFin" not in sc.sticky:
        raise Exception("Initialise the plugin first!")

    cablenet = sc.sticky["FoFin"]['cablenet']
    settings = sc.sticky["FoFin"]['settings']

    if not cablenet:
        return

    if compas_rhino.update_settings(settings):
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
