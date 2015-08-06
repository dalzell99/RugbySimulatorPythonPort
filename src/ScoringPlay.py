__author__ = 'Chris'

class ScoringPlay:
    minutes = 0
    play = ""
    description = ""

    def __init__(self, minutes, play, description):
        self.minutes = minutes
        self.play = play
        self.description = description

    def get_minutes(self):
        return self.minutes

    def get_play(self):
        return self.play

    def get_description(self):
        return self.description
