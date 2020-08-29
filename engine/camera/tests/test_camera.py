from ..camera import Camera
from ...geometry import Point2d
from unittest.mock import Mock, call, patch
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

    def test_update_centers_on_followed_object(self):
        """Updating the camera centers it on the followed object."""
        # Create an object in the center of the camera
        target = Mock(width=20, height=10, center=Point2d(50, 25))
        camera = Camera(100, 50)
        camera.follow = target
        camera.update(123)

        self.assertEqual(0, camera.x, 'Not centered horizontal on target')
        self.assertEqual(0, camera.y, 'Not centered vertical on target')

        # Move the object to be centered at (75, 35)
        target.center = Point2d(75, 35)
        camera.update(123)

        self.assertEqual(25, camera.x, 'Not centered horizontal after follow')
        self.assertEqual(10, camera.y, 'Not centered vertical after follow')

    def test_update_centers_on_followed_object_with_easing(self):
        """Updating the camera eases to the center of the followed object."""
        # Create an object in the center of the camera
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.update(123)

        self.assertEqual(0, camera.x, 'Target x-axis not centered with easing')
        self.assertEqual(0, camera.y, 'Target y-axis not centered with easing')

        # Easing was updated to view the center of the target
        camera.follow_easing.update.assert_called_once_with(123)
        camera.follow_easing.reset.assert_called_once_with(
            Point2d(50, 25), Point2d(50, 25))

        # Move the object to be centered at (75, 35)
        camera.follow_easing.value = Point2d(55, 30)
        target.center = Point2d(75, 35)
        camera.update(456)

        self.assertEqual(5, camera.x, 'Target x-axis not centered with easing')
        self.assertEqual(5, camera.y, 'Target y-axis not centered with easing')

        # Easing was updated to ease to the new center of the target
        camera.follow_easing.update.assert_called_with(456)
        camera.follow_easing.reset.assert_called_with(
            Point2d(50, 25), Point2d(75, 35))

    def test_update_eases_to_follow_target_with_positive_horizontal_lead(self):
        """Updating the camera with leading eases ahead of followed object."""
        # Create an object in the center of the camera
        lead = 123
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_lead = Point2d(lead, 0)
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.update(1)

        # Easing was updated to view the center of the resting target
        camera.follow_easing.reset.assert_called_once_with(
            Point2d(50, 25), Point2d(50, 25))

        # Move the object to be centered at (75, 25)
        target.physics.velocity.x = 10  # x velocity will be a positive value
        target.center = Point2d(75, 25)
        camera.update(1)

        # Easing had lead applied when following moving target
        camera.follow_easing.reset.assert_called_with(
            Point2d(50, 25), Point2d(75 + lead, 25))

    def test_update_eases_to_follow_target_with_negative_horizontal_lead(self):
        """Updating the camera with leading eases ahead of followed object."""
        # Create an object in the center of the camera
        lead = 123
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_lead = Point2d(lead, 0)
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.update(1)

        # Easing was updated to view the center of the resting target
        camera.follow_easing.reset.assert_called_once_with(
            Point2d(50, 25), Point2d(50, 25))

        # Move the object to be centered at (25, 25)
        target.physics.velocity.x = -10  # x velocity will be a negative value
        target.center = Point2d(25, 25)
        camera.update(1)

        # Easing had lead applied when following moving target
        camera.follow_easing.reset.assert_called_with(
            Point2d(50, 25), Point2d(25 - lead, 25))

    def test_update_eases_to_follow_target_with_positive_vertical_lead(self):
        """Updating the camera with leading eases ahead of followed object."""
        # Create an object in the center of the camera
        lead = 123
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_lead = Point2d(0, lead)
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.update(1)

        # Easing was updated to view the center of the resting target
        camera.follow_easing.reset.assert_called_once_with(
            Point2d(50, 25), Point2d(50, 25))

        # Move the object to be centered at (50, 50)
        target.physics.velocity.y = 10  # y velocity will be a positive value
        target.center = Point2d(50, 50)
        camera.update(1)

        # Easing had lead applied when following moving target
        camera.follow_easing.reset.assert_called_with(
            Point2d(50, 25), Point2d(50, 50 + lead))

    def test_update_eases_to_follow_target_with_negative_vertical_lead(self):
        """Updating the camera with leading eases ahead of followed object."""
        # Create an object in the center of the camera
        lead = 123
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_lead = Point2d(0, lead)
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.update(1)

        # Easing was updated to view the center of the resting target
        camera.follow_easing.reset.assert_called_once_with(
            Point2d(50, 25), Point2d(50, 25))

        # Move the object to be centered at (50, 0)
        target.physics.velocity.y = -10  # y velocity will be a negative value
        target.center = Point2d(50, 0)
        camera.update(1)

        # Easing had lead applied when following moving target
        camera.follow_easing.reset.assert_called_with(
            Point2d(50, 25), Point2d(50, 0 - lead))

    def test_camera_does_not_move_with_object_in_deadzone(self):
        """A camera does not move when a followed object is in the deadzone."""
        # Create an object in the center of the camera
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.follow_deadzone = Mock(x=10, y=5, width=80, height=40)

        # Target moves right within deadzone
        target.physics.velocity.x = 10
        target.center = Point2d(75, 25)
        target.x = 65
        camera.update(1)

        # Target moves left within deadzone
        target.physics.velocity.x = -10
        target.center = Point2d(50, 25)
        target.x = 40
        camera.update(1)

        # Target moves up within deadzone
        target.physics.velocity.y = 10
        target.physics.velocity.x = 0
        target.center = Point2d(50, 35)
        target.y = 30
        camera.update(1)

        # Target moves down within deadzone, even with lead
        camera.follow_lead = Point2d(0, 100)
        target.physics.velocity.y = -10
        target.center = Point2d(50, 25)
        target.y = 20
        camera.update(1)

        # Camera never moved
        camera.follow_easing.reset.assert_has_calls(
            [call(camera.center, camera.center)] * 4)

    def test_camera_moves_once_object_leaves_dead_zone(self):
        """A camera only moves once the followed object leaves the deadzone."""
        # Create an object in the center of the camera
        target = Mock(x=40, y=20, width=20, height=10, center=Point2d(50, 25),
                      physics=Mock(velocity=Point2d(0, 0)))
        camera = Camera(100, 50)
        camera.follow = target
        camera.follow_easing = Mock(value=Point2d(50, 25))
        camera.follow_deadzone = Mock(x=10, y=5, width=80, height=40)

        # Target moves right within deadzone
        target.physics.velocity.x = 10
        target.center = Point2d(99, 25)
        target.x = 89
        camera.update(1)

        # Target moves right outside deadzone
        target.center = Point2d(100, 25)
        target.x = 90
        camera.update(1)

        # Rest within the deadzone to reapply it
        target.physics.velocity.x = 0
        target.center = Point2d(50, 25)
        target.x = 40
        camera.update(1)

        # Target moves left within deadzone
        target.physics.velocity.x = -10
        target.center = Point2d(1, 25)
        target.x = -9
        camera.update(1)

        # Target moves left outside deadzone
        target.center = Point2d(0, 25)
        target.x = -10
        camera.update(1)

        # Rest within the deadzone to reapply it
        target.physics.velocity.x = 0
        target.center = Point2d(50, 25)
        target.x = 40
        camera.update(1)

        # Target moves up within deadzone
        target.physics.velocity.y = 10
        target.center = Point2d(50, 49)
        target.y = 44
        camera.update(1)

        # Target moves up outside deadzone
        target.center = Point2d(50, 50)
        target.y = 45
        camera.update(1)

        # Rest within the deadzone to reapply it
        target.physics.velocity.y = 0
        target.center = Point2d(50, 25)
        target.y = 20
        camera.update(1)

        # Target moves down within deadzone
        target.physics.velocity.y = -10
        target.center = Point2d(50, 1)
        target.y = -4
        camera.update(1)

        # Target moves down outside deadzone
        target.center = Point2d(50, 0)
        target.y = -5
        camera.update(1)

        # Camera never moved
        camera.follow_easing.reset.assert_has_calls([
            call(Point2d(50, 25), Point2d(50, 25)),  # Move right
            call(Point2d(50, 25), Point2d(100, 25)),
            call(Point2d(50, 25), Point2d(50, 25)),
            call(Point2d(50, 25), Point2d(50, 25)),  # Move left
            call(Point2d(50, 25), Point2d(0, 25)),
            call(Point2d(50, 25), Point2d(50, 25)),
            call(Point2d(50, 25), Point2d(50, 25)),  # Move up
            call(Point2d(50, 25), Point2d(50, 50)),
            call(Point2d(50, 25), Point2d(50, 25)),
            call(Point2d(50, 25), Point2d(50, 25)),  # Move down
            call(Point2d(50, 25), Point2d(50, 0)),
            ])

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

    @patch('pyglet.gl.glScalef')
    @patch('pyglet.gl.glTranslatef')
    @patch('pyglet.gl.glPushMatrix')
    def test_attach_creates_new_matrix(self, push, translate, scale):
        """Attaching the camera creates a new OpenGL matrix."""
        camera = Camera(100, 50)
        camera.attach()

        push.assert_called_once()

    @patch('pyglet.gl.glScalef')
    @patch('pyglet.gl.glTranslatef')
    @patch('pyglet.gl.glPushMatrix')
    def test_attach_translates_gl_context_to_coordinates(self, push, translate,
                                                         scale):
        """Attaching the camera translates the OpenGL context."""
        camera = Camera(100, 50)
        camera.look_at(100, 50)
        camera.attach()

        translate.assert_called_once_with(-50, -25, 0)

    @patch('pyglet.gl.glScalef')
    @patch('pyglet.gl.glTranslatef')
    @patch('pyglet.gl.glPushMatrix')
    def test_attach_scales_gl_context(self, push, translate, scale):
        """Attaching the camera scales the OpenGL context."""
        camera = Camera(100, 50)
        camera.scale = 2
        camera.attach()

        scale.assert_called_once_with(camera.scale, camera.scale, 0)

    @patch('pyglet.gl.glScalef')
    @patch('pyglet.gl.glTranslatef')
    @patch('pyglet.gl.glPushMatrix')
    @patch('pyglet.gl.glPopMatrix')
    def test_detach_pops_matrix(self, pop, push, translate, scale):
        """Detaching the camera pops its OpenGL matrix."""
        camera = Camera(100, 50)
        camera.attach()
        camera.detach()

        pop.assert_called_once()
