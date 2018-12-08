class PlatformerController(object):
    """Provides controls for a side-scrolling platformer character.

    Attributes
        is_airborne (bool):
            The character's airborne state, e.g. jumping or falling. Read-only.
        is_jumping (bool):
            Whether the character is intentionally jumping. Read-only.
    """

    def __init__(self, character, walk_acceleration, jump_height):
        """Creates a side-scrolling platformer controller for a character.

        Args:
            character (:obj:`engine.game_object.GameObject`):
                The character to control.
            walk_acceleration (int): The walking acceleration of the character.
            jump_height (int): The maximum height the player can jump.
        """
        self._character = character
        self._walk_acceleration = walk_acceleration
        self._jump_height = jump_height
        self._last_ground_position = self._character.y

        # Whether the character is intentionally jumping, not just airborne
        self._is_jumping = False

    @property
    def is_airborne(self):
        """Determines whether the character is airborne."""
        return self._character.physics.velocity.y != 0 or self._is_jumping

    @property
    def is_jumping(self):
        """Returns whether the character is intentionally jumping or not."""
        return self._is_jumping

    def jump(self, *args):
        """Causes the player to jump by applying positive vertical acceleration.

        The jump is an impulse which decreases each time this method is called,
        unless `cancel_jump` is called or the character is not airborne. The
        longer the jump occurs, the higher the jump becomes.

        Recommended as a key down handler.
        """
        if not self.is_airborne:
            # Not airborne, start jumping by setting the impulse
            self._last_ground_position = self._character.y
            self._character.physics.acceleration.y = 80
            self._is_jumping = True
        if self._character.y >= self._last_ground_position + self._jump_height:
            # Reached max jump height, stop jump impulse
            self._character.physics.acceleration.y = 0
        else:  # Continuing jump, increase impulse
            # Get the current height of the jump as a percent of the max height
            height_difference = self._character.y - self._last_ground_position
            jump_percent = 1 - (height_difference / self._jump_height)

            # Acceleration eases in until the character is past the jump height
            self._character.physics.acceleration.y *= pow(max(jump_percent, 0), 3)

    def cancel_jump(self, *args):
        """Cancels an in-progress jump by removing the vertical acceleration.

        Recommended as a key release handler.
        """
        if self._character.physics.acceleration.y > 0:
            self._character.physics.acceleration.y = 0
        self._is_jumping = False

    def walk_left(self, *args):
        """Accelerates the character left using their walking acceleration.

        Recommended as a key down handler.
        """
        self._character.physics.acceleration.x = -self._walk_acceleration

    def walk_right(self, *args):
        """Accelerates the character right using their walking acceleration.

        Recommended as a key down handler.
        """
        self._character.physics.acceleration.x = self._walk_acceleration

    def stop_walking(self, *args):
        """Stops the character's horizontal acceleration.

        Recommended as a key release handler.
        """
        self._character.physics.acceleration.x = 0
