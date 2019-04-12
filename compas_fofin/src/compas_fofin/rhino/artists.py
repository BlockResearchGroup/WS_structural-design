from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas.geometry import scale_vector
from compas.geometry import add_vectors

from compas_rhino.artists import MeshArtist


__all__ = ['CablenetArtist']


class CablenetArtist(MeshArtist):

    def draw_reactions(self, scale=1.0, color=None):
        compas_rhino.delete_objects(compas_rhino.get_objects(name="{}.reaction.*".format(self.mesh.name)))

        color = color or (0, 255, 0)
        lines = []
        for key, attr in self.mesh.vertices(True):
            if not attr['is_anchor']:
                continue

            r = [attr['rx'], attr['ry'], attr['rz']]
            sp = [attr['x'], attr['y'], attr['z']]
            ep = add_vectors(sp, scale_vector(r, -scale))

            lines.append({
                'start' : sp,
                'end'   : ep,
                'color' : color,
                'name'  : "{}.reaction.{}".format(self.mesh.name, key),
                'arrow' : 'end'
            })

        compas_rhino.xdraw_lines(lines, layer=self.layer, redraw=True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    pass
