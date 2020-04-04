from ..camera import Camera
from unittest.mock import Mock, patch
import unittest


class TestCamera(unittest.TestCase):
    """Test tracking functionality of the camera."""

    def test_scale_defaults_to_1(self):
        """The camera scale is 1 by default."""
        camera = Camera(100, 50)

        self.assertEqual(1, camera.scale)

    def test_look_at_centers_on_coordinates(self):
        """The camera target is centered within the frame."""
        camera = Camera(100, 50)
        camera.look_at(100, 50)

        self.assertEqual(50, camera.x, 'Camera is not horizontally centered')
        self.assertEqual(25, camera.y, 'Camera is not vertically centered')

    def test_camera_can_not_retract_past_boundary(self):
        """The camera will not retract past the boundary."""
        camera = Camera(100, 50)
        camera.set_boundary(200, 100)
        camera.look_at(-200, -100)

        self.assertEqual(0, camera.x, 'Camera receeded past horizontal bounds')
        self.assertEqual(0, camera.y, 'Camera receeded past vertical bounds')

    def test_camera_can_not_extend_past_boundary(self):
        """The camera will not exceed past the boundary."""
        camera = Camera(100, 50)
        camera.set_boundary(200, 100)
        camera.look_at(200, 100)

        self.assertEqual(100, camera.x, 'Camera exceeded horizontal bounds')
        self.assertEqual(50, camera.y, 'Camera exceeded vertical bounds')

    @patch('pyglet.gl.glPushMatrix')
    def test_attach_creates_new_matrix(self, mock_push_matrix):
        """Attaching the camera creates a new OpenGL matrix."""
        camera = Camera(100, 50)
        camera.attach()

        mock_push_matrix.assert_called_once()

    @patch('pyglet.gl.glTranslatef')
    def test_attach_translates_gl_context_to_coordinates(self, mock_translate):
        """Attaching the camera translates the OpenGL context."""
        camera = Camera(100, 50)
        camera.look_at(100, 50)
        camera.attach()

        mock_translate.assert_called_once_with(-50, -25, 0)

    @patch('pyglet.gl.glScalef')
    def test_attach_scales_gl_context(self, mock_scale):
        """Attaching the camera scales the OpenGL context."""
        camera = Camera(100, 50)
        camera.scale = 2
        camera.attach()

        mock_scale.assert_called_once_with(camera.scale, camera.scale, 0)

    @patch('pyglet.gl.glPopMatrix')
    def test_detach_pops_matrix(self, mock_pop_matrix):
        """Detaching the camera pops its OpenGL matrix."""
        camera = Camera(100, 50)
        camera.attach()
        camera.detach()

        mock_pop_matrix.assert_called_once()
