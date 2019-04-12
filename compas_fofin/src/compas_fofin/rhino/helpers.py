from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino.selectors import VertexSelector
from compas_rhino.selectors import EdgeSelector

from compas_rhino.modifiers import VertexModifier
from compas_rhino.modifiers import EdgeModifier


__all__ = ['CablenetHelper']


class CablenetHelper(VertexSelector, VertexModifier, EdgeSelector, EdgeModifier):
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
