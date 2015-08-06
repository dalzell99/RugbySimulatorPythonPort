__author__ = 'Chris'

import dateutil.parser
import time


class Game:
    game_id = 0
    home_team_name = ""
    home_team_score = 0
    away_team_name = ""
    away_team_score = 0
    location = ""
    minutes_played = 0
    time_start = ""
    ref = ""
    ass_ref_1 = ""
    ass_ref_2 = ""
    scoring_plays = []
    changed = ""
    minutes_since_midnight = 0
    month = ["January", "February", "March", "April", "May", "June", "July",
             "August", "September", "October", "November", "December"]
    day_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def set_minutes_since_midnight(self):
        game_start_time = self.time
        if len(game_start_time) > 0:
            # Get hours past midday or midnight and the minutes past hour if game doesn't start on the hour
            if not game_start_time.find(":") == -1:
                hours = int(game_start_time[0:game_start_time.indexOf(":")])
                minutes = int(game_start_time[game_start_time.indexOf(":") + 1:game_start_time.indexOf(":") + 3])
            else:
                hours = int(game_start_time[0:game_start_time.length() - 2])
                minutes = 0

            # Get am or pm
            am_or_pm = game_start_time[game_start_time.length() - 2:]
            # Get minutes since midnight
            self.minutes_since_midnight = minutes + hours * 60 if am_or_pm == "am" or (hours == 12
                                   and am_or_pm == "pm") else minutes + hours * 60 + 12 * 60
        else:
            self.minutes_since_midnight = 0

    def get_date_string(self):
        date_string = ""
        today = time.strftime("%Y%m%d")
        # Check if game is being played today.
        game_id_str = str(self.game_id)
        if game_id_str[0:8] == today[0, 8]:
            date_string += "Today "
        else:
            date = dateutil.parser.parse(game_id_str[0:8])
            date_string += self.day_of_week[date.weekday()]
            date_string += " "
            date_string += date.day
            date_string += " "
            date_string += self.month[date.month]
            date_string += " "
        return date_string

    def __init__(self, game_id, home_team_name, home_team_score, away_team_name, away_team_score, location,
                 minutes_played, time_start, ref, ass_ref_1, ass_ref_2, scoring_plays, changed):
        self.game_id = game_id
        self.home_team_name = home_team_name
        self.home_team_score = home_team_score
        self.away_team_name = away_team_name
        self.away_team_score = away_team_score
        self.location = location
        self.minutes_played = minutes_played
        self.time_start = time_start
        self.ref = ref
        self.ass_ref_1 = ass_ref_1
        self.ass_ref_2 = ass_ref_2
        self.scoring_plays = scoring_plays
        self.changed = changed
        self.set_minutes_since_midnight()

    def get_game_id(self):
        return self.game_id

    def get_home_team_name(self):
        return self.home_team_name

    def get_home_team_score(self):
        return self.home_team_score

    def get_away_team_name(self):
        return self.away_team_name

    def get_away_team_score(self):
        return self.away_team_score

    def get_location(self):
        return self.location

    def get_minutes_played(self):
        return self.minutes_played

    def get_time(self):
        return self.time

    def get_ref(self):
        return self.ref

    def get_ass_ref_1(self):
        return self.ass_ref_1

    def get_ass_ref_2(self):
        return self.ass_ref_2

    def get_scoring_plays(self):
        return self.scoring_plays

    def get_changed(self):
        return self.changed

    def get_minutes_since_midnight(self):
        return self.minutes_since_midnight

    def set_game_id(self, game_id):
        self.game_id = game_id

    def set_home_team_name(self, home_team_name):
        self.home_team_name = home_team_name

    def set_home_team_score(self, home_team_score):
        self.home_team_score = home_team_score

    def set_away_team_name(self, away_team_name):
        self.away_team_name = away_team_name

    def set_away_team_score(self, away_team_score):
        self.away_team_score = away_team_score

    def set_location(self, location):
        self.location = location

    def set_minutes_played(self, minutes_played):
        self.minutes_played = minutes_played

    def set_time(self, time):
        self.time = time

    def set_ref(self, ref):
        self.ref = ref

    def set_ass_ref_1(self, ass_ref_1):
        self.ass_ref_1 = ass_ref_1

    def set_ass_ref_2(self, ass_ref_2):
        self.ass_ref_2 = ass_ref_2

    def set_scoring_plays(self, scoring_plays):
        self.scoring_plays = scoring_plays

    def set_changed(self, changed):
        self.changed = changed