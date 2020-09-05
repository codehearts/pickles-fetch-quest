from ..cross_box import CrossBox
from unittest.mock import Mock, patch
from pyglet.gl import GL_LINES
import unittest


class TestCrossBox(unittest.TestCase):
    """Test rendering of cross box graphics."""

    def setUp(self):
        """Provides the following to all tests:

        * ``self.rectangle``: Mock rectangle.
        * ``self.vertex_count``: Number of vertices for the rectangle.
        * ``self.expected_vertices``: Expected verticies for the rectangle.
        * ``self.default_color``: Expected default color for the cross box.
        * ``self.new_coordinates``: New coordinates to reposition to.
        * ``self.new_expected_vertices``: Expected verticies after reposition.
        """
        self.rectangle = Mock(x=1, y=2, width=3, height=4)

        self.expected_vertices = (
            1, 2, 4, 2,
            1, 2, 1, 6,
            4, 2, 1, 6,
            1, 6, 4, 6,
            4, 6, 1, 2,
            4, 6, 4, 2)
        self.vertex_count = (len(self.expected_vertices) // 2)

        self.default_color = (0, 0, 0) * self.vertex_count

        self.new_coordinates = (2, 4)
        self.new_expected_vertices = [
            2, 4, 5, 4,
            2, 4, 2, 8,
            5, 4, 2, 8,
            2, 8, 5, 8,
            5, 8, 2, 4,
            5, 8, 5, 4]

    @patch('engine.graphics.cross_box.vertex_list')
    def test_creates_vertex_list_without_batch(self, mock_vertex_list):
        """Cross box uses a vertex list if no batch is given."""
        CrossBox(self.rectangle)

        mock_vertex_list.assert_called_once_with(
            self.vertex_count,
            ('v2i', self.expected_vertices),
            ('c3B', self.default_color))

    @patch('engine.graphics.cross_box.vertex_list')
    def test_sets_color_of_vertex_list(self, mock_vertex_list):
        """Cross box sets custom colors for a vertex list."""
        color = (1, 2, 3)
        expected_colors = color * self.vertex_count

        CrossBox(self.rectangle, color)

        mock_vertex_list.assert_called_once_with(
            self.vertex_count,
            ('v2i', self.expected_vertices),
            ('c3B', expected_colors))

    @patch('engine.graphics.cross_box.vertex_list')
    def test_repositions_vertex_list(self, mock_vertex_list):
        """Repositioning a cross box updates the vertex list."""
        mock_vertex_list.return_value.vertices = self.expected_vertices
        cross_box = CrossBox(self.rectangle)
        cross_box.set_position(self.new_coordinates)

        self.assertEqual(
            self.new_expected_vertices, mock_vertex_list.return_value.vertices)

    def test_uses_batch(self):
        """Cross box uses a batch if given."""
        batch = Mock()
        CrossBox(self.rectangle, batch=batch)

        batch.add.assert_called_once_with(
            self.vertex_count,
            GL_LINES,
            None,
            ('v2i', self.expected_vertices),
            ('c3B', self.default_color))

    def test_sets_color_with_batch(self):
        """Cross box sets custom colors when using a batch."""
        color = (1, 2, 3)
        expected_colors = color * self.vertex_count

        batch = Mock()
        CrossBox(self.rectangle, color, batch)

        batch.add.assert_called_once_with(
            self.vertex_count,
            GL_LINES,
            None,
            ('v2i', self.expected_vertices),
            ('c3B', expected_colors))

    def test_repositions_batch(self):
        """Repositioning a cross box updates the batched vertices."""
        batch = Mock()
        batch.add.return_value.vertices = self.expected_vertices

        cross_box = CrossBox(self.rectangle, batch=batch)
        cross_box.set_position(self.new_coordinates)

        self.assertEqual(
            self.new_expected_vertices, batch.add.return_value.vertices)
