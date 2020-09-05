from ..graphics_batch import GraphicsBatch
from unittest.mock import Mock, patch
from pyglet.gl import GL_ENABLE_BIT, GL_LINE_STIPPLE
import unittest


class TestGraphicsBatch(unittest.TestCase):
    """Test graphics batch functionality."""

    @patch('engine.graphics.graphics_batch.glPushAttrib')
    @patch('engine.graphics.graphics_batch.glPopAttrib')
    @patch('engine.graphics.graphics_batch.glEnable')
    @patch('engine.graphics.graphics_batch.glLineStipple')
    def test_draw_dashed_lines(self, mock_line_stipple, mock_enable, mock_pop,
                               mock_push):
        """Graphics batches can be drawn with dashed lines."""
        batch = GraphicsBatch()
        batch.draw = Mock()
        batch.draw_special(GraphicsBatch.DASHED_LINES)

        mock_push.assert_called_once_with(GL_ENABLE_BIT)
        mock_line_stipple.assert_called_once_with(1, 0x00FF)
        mock_enable.assert_called_once_with(GL_LINE_STIPPLE)
        batch.draw.assert_called_once_with()
        mock_pop.assert_called_once_with()
