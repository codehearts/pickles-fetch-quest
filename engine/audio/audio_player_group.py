class AudioPlayerGroup(object):
    """Easily control playback and settings for multiple audio players at once.
    """
    def __init__(self, players=[]):
        """Creates a new grouping of audio players.

        Kwargs:
            players (list of :obj:`audio.AudioPlayer`): Initial group members.
        """
        super(AudioPlayerGroup, self).__init__()
        self._currently_playing = set()
        self._players = players

        for player in self._players:
            self._add_player_listeners(player)

    def add(self, player):
        """Adds another player to this group.

        Args:
            player (:obj:`audio.AudioPlayer`): The player to add to this group.
        """
        self._players.append(player)

    def resume(self):
        """Resumes playing paused players from where they left off.

        Only players that were paused in the middle of playback will resume.
        This is useful after pausing an audio player group.
        """
        for player in self._currently_playing:
            player.play()

    def pause(self):
        """Pauses all players in the group."""
        for player in self._players:
            player.pause()

    def stop(self):
        """Stops all players in the group."""
        for player in self._players:
            player.stop()

    def set_volume(self, level):
        """Sets the volume of each player in the group.

        Args:
            level (float): A value between 0.0 (silence) and 1.0 (full volume).
        """
        for player in self._players:
            player.volume = level

    def _add_player_listeners(self, player):
        """Adds listeners to a player to keep track of when it's playing.

        When the player's on_play event is dispatched, it will be added to
        a set of currently playing players.

        When the player finishes or is stopped, it will be removed from the
        set of players which are currently playing.

        Args:
            player (:obj:`audio.AudioPlayer`): Player to add listeners to.
        """
        player.add_listeners(
            on_play=self._add_to_currently_playing,
            on_stop=self._remove_from_currently_playing,
            on_finish=self._remove_from_currently_playing)

    def _add_to_currently_playing(self, player):
        """Adds a player to the list of currently playing players.

        Args:
            player (:obj:`audio.AudioPlayer`): A currently playing player.
        """
        self._currently_playing.add(player)

    def _remove_from_currently_playing(self, player):
        """Removes a player from the list of currently playing players.

        Args:
            player (:obj:`audio.AudioPlayer`): A stopped player.
        """
        self._currently_playing.discard(player)
