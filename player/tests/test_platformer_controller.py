from ..platformer_controller import PlatformerController
from unittest.mock import Mock
import unittest


class TestPlatformerController(unittest.TestCase):
    """Test character platformer controls."""

    def setUp(self):
        """Provides each test case with the following properties::

            self.mock_character: Mock character object at y=0.
            self.walk_acceleration: Walking acceleration for the controller.
            self.jump_height: Jump height for the controller.
            self.controller: `PlatformerController` object for testing.
        """
        self.mock_character = Mock(y=0)
        self.walk_acceleration = 12
        self.jump_height = 34
        self.jump_time = 250
        self.controller = PlatformerController(
            self.mock_character, self.walk_acceleration, self.jump_height,
            self.jump_time)

    def test_controller_is_not_jumping_by_default(self):
        """By default, a controller is not jumping."""
        self.assertFalse(self.controller.is_jumping)

    def test_controller_is_jumping_after_calling_jump(self):
        """A controller is jumping when the `jump` method is called."""
        # Start from rest
        self.mock_character.physics.acceleration.y = 0
        self.mock_character.physics.velocity.y = 0

        self.controller.jump(15)
        self.assertTrue(self.controller.is_jumping)

    def test_controller_is_not_jumping_after_cancelling_jump(self):
        """A controller is no longer jumping when a jump is cancelled."""
        # Start from rest
        self.mock_character.physics.acceleration.y = 0
        self.mock_character.physics.velocity.y = 0

        self.controller.jump(15)
        self.controller.cancel_jump()
        self.assertFalse(self.controller.is_jumping)

    def test_jump_velocity_decreases_as_jump_is_called(self):
        """The velocity of a jump decreases the more `jump` is called."""
        # Start from rest
        self.mock_character.physics.acceleration.y = 0
        self.mock_character.physics.velocity.y = 0

        impulses = []

        # Jump and capture the velocity multiple times
        for i in range(3):
            self.controller.jump(self.jump_time // 3)
            self.mock_character.y += 1
            impulses.append(self.mock_character.physics.velocity.y)

        # Acceleration should decrease
        self.assertLess(impulses[-1], impulses[-2])
        self.assertLess(impulses[-2], impulses[-3])

    def test_impulse_is_removed_at_end_of_jump_time(self):
        """The jump impulse is removed once the jump time has elapsed."""
        # Start from rest
        self.mock_character.physics.acceleration.y = 0
        self.mock_character.physics.velocity.y = 0

        self.controller.jump(0)

        # Just before the end of the jump, impulse should be applied
        self.controller.jump(self.jump_time - 1)
        self.assertGreater(self.mock_character.physics.velocity.y, 0)

        # At jump height, impulse should be removed
        self.controller.jump(1)
        self.assertEqual(0, self.mock_character.physics.velocity.y)

    def test_controller_is_not_airborne_when_at_rest(self):
        """A controller is not airborne when the character is at rest."""
        self.mock_character.physics.velocity.y = 0
        self.assertFalse(self.controller.is_airborne)

    def test_controller_is_airborne_when_moving_up(self):
        """A controller is airborne when the character is moving upwards."""
        self.mock_character.physics.velocity.y = 1
        self.assertTrue(self.controller.is_airborne)

    def test_controller_is_airborne_when_moving_down(self):
        """A controller is airborne when the character is moving downwards."""
        self.mock_character.physics.velocity.y = -1
        self.assertTrue(self.controller.is_airborne)

    def test_walking_right_applies_positive_walk_acceleration(self):
        """Walking right applies positive walking acceleration."""
        self.controller.walk_right()
        self.assertEqual(
            self.walk_acceleration,
            self.mock_character.physics.acceleration.x)

    def test_walking_left_applies_negative_walk_acceleration(self):
        """Walking left applies negative walking acceleration."""
        self.controller.walk_left()
        self.assertEqual(
            -self.walk_acceleration,
            self.mock_character.physics.acceleration.x)

    def test_stopping_a_walk_removes_horizontal_acceleration(self):
        """Stopping a walking removes horizontal acceleration."""
        self.controller.walk_left()
        self.controller.stop_walking()
        self.assertEqual(0, self.mock_character.physics.acceleration.x)
