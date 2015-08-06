__author__ = 'Chris'

import dateutil.parser
import time
import requests
import json
import sched
from random import randint


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
        game_start_time = self.time_start
        if len(game_start_time) > 0:
            # Get hours past midday or midnight and the minutes past hour if game doesn't start on the hour
            if not game_start_time.find(":") == -1:
                hours = int(game_start_time[0:game_start_time.find(":")])
                minutes = int(game_start_time[game_start_time.find(":") + 1:game_start_time.find(":") + 3])
            else:
                hours = int(game_start_time[0:len(game_start_time) - 2])
                minutes = 0

            # Get am or pm
            am_or_pm = game_start_time[len(game_start_time) - 2:]
            # Get minutes since midnight
            self.minutes_since_midnight = minutes + hours * 60 if am_or_pm == "am" or (hours == 12 and am_or_pm == "pm") \
                else minutes + hours * 60 + 12 * 60
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

    def get_time_start(self):
        return self.time_start

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

    def set_time(self, time_start):
        self.time_start = time_start

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


class Main:
    allGames = []

    s = sched.scheduler(time.time, time.sleep)
    current_time_since_midnight_in_minutes = 0
    count = 0
    descriptions = ["A storming break by the centre leads to a try under the posts.",
                    "Fantastic long range try under the posts in Calypso style.",
                    "A beautifully worked play ending in a try just left of the posts.",
                    "A well formed lineout drive finishes with a try to the openside flanker.",
                    "Try out wide to the number 8 after a tighthead scrum.",
                    """"Sustained pressure from the forwards left the defense vulnerable out wide where
                    the right wing strolled over for an easy try."""]

    def get_all_games(self):
        request = requests.get("http://www.possumpam.com/rugby-scoring-app-scripts/Test/get_all_games.php")
        result = request.json()

        for game_index in range(len(result)):
            scoring_plays = []
            all_scoring_plays_for_this_game = json.loads(result[game_index]["scoringPlays"])
            for scoring_play_index in range(len(all_scoring_plays_for_this_game)):
                scoring_play = ScoringPlay(all_scoring_plays_for_this_game[scoring_play_index][0],
                                           all_scoring_plays_for_this_game[scoring_play_index][1],
                                           all_scoring_plays_for_this_game[scoring_play_index][2])
                scoring_plays.append(scoring_play)

            game_info = result[game_index]
            game = Game(int(game_info["GameID"]), game_info["homeTeamName"], 0,
                        game_info["awayTeamName"], 0, game_info["location"],
                        int(game_info["minutesPlayed"]), game_info["time"], game_info["ref"], game_info["assRef1"],
                        game_info["assRef2"], scoring_plays, game_info["changed"])
            self.allGames.append(game)

    def pad(self, num):
        return "0" + str(num) if num < 10 else str(num)

    def pad_hours(self, num):
        return " " + str(num) if num < 10 else str(num)

    def change_score(self, event, g):
        if event[0:4] == "home":
            play = event[4:]
            if play == "Try":
                g.set_home_team_score(g.get_home_team_score() + 5)
            elif play == "DropGoal" or play == "Penalty":
                g.set_home_team_score(g.get_home_team_score() + 3)
            elif play == "Conversion":
                g.set_home_team_score(g.get_home_team_score() + 2)
        elif event[0:4] == "away":
            play = event[4:]
            if play == "Try":
                g.set_away_team_score(g.get_away_team_score() + 5)
            elif play == "DropGoal" or play == "Penalty":
                g.set_away_team_score(g.get_away_team_score() + 3)
            elif play == "Conversion":
                g.set_away_team_score(g.get_away_team_score() + 2)

    def display_event(self, event, g, time_scored):
        # Get hours past midday or midnight and the minutes past hour if game doesn't start on the hour
        if not g.get_time_start().find(":") == -1:
            hours = int(g.get_time_start()[0:g.get_time_start().find(":")])
            minutes = int(g.get_time_start()[g.get_time_start().find(":") + 1:g.get_time_start().find(":") + 3])
        else:
            hours = int(g.get_time_start()[0:len(g.get_time_start()) - 2])
            minutes = 0

        # Get am or pm
        amorpm = g.get_time_start()[len(g.get_time_start()) - 2:]
        # Get minutes since midnight
        minutes += time_scored
        if minutes >= 120:
            minutes -= 120
            hours += 2
            if hours >= 12:
                amorpm = "pm"
                hours -= 12 if hours > 12 else 0
        elif minutes >= 60:
            minutes -= 60
            hours += 1
            if hours >= 12:
                amorpm = "pm"
                hours -= 12 if hours > 12 else 0

        time_string = self.pad_hours(hours) + ":" + self.pad(minutes) + amorpm + " "

        divisions = ["Div 1", "Women", "Div 2", "Div 3", "Colts",
                     "  U18", "  U16", "U14.5", "  U13", "U11.5", "  U10", " U8.5", "   U7"]
        div_id = int(str(g.get_game_id())[12:14])
        div = divisions[div_id] + " "
        if event[0:4] == "home" or event[0:4] == "away":
            # Example: 9:34am Dunsandel 35 vs Leeston 15 (75') - Try to Dunsandel
            scoring_play_string = ""
            scoring_play_string += "Drop Goal" if event[4:] == "DropGoal" else event[4:]
            scoring_play_string += " to "
            scoring_play_string += g.get_home_team_name() if event[0:4] == "home" else g.get_away_team_name()
            print(time_string + " " +
                  div + " " +
                  g.get_home_team_name() + " " + str(g.get_home_team_score()) +
                  " vs " +
                  g.get_away_team_name() + " " + str(g.get_away_team_score()) +
                  " (" + str(time_scored) + "') - " + scoring_play_string)
        elif event[0:4] == "strt":
            print(time_string + " " +
                  div + " GAME START " +
                  g.get_home_team_name() +
                  " vs " +
                  g.get_away_team_name())
        elif event[0:4] == "half":
            print(time_string + " " +
                  div + " HALF TIME " +
                  g.get_home_team_name() + " " + str(g.get_home_team_score()) +
                  " vs " +
                  g.get_away_team_name() + " " + str(g.get_away_team_score()))
        elif event[0:4] == "full":
            print(time_string + " " +
                  div + " FULL TIME " +
                  g.get_home_team_name() + " " + str(g.get_home_team_score()) +
                  " vs " +
                  g.get_away_team_name() + " " + str(g.get_away_team_score()))

    def upload_event(self, event, g, time_scored, description):
        self.change_score(event, g)
        self.display_event(event, g, time_scored)

        payload = {"gameID": str(g.get_game_id()), "minutesPlayed": str(time_scored), "scoring_play_string": event,
                   "description": description, "homeScore": str(g.get_home_team_score()), 
                   "awayScore": str(g.get_away_team_score())}
        request = requests.get("http://www.possumpam.com/rugby-scoring-app-scripts/Test/update_game.php", 
                               params=payload)
        if request.text == "failure":
            print("*************FAILURE*************")

    def game_simulator(self, g):
        number_of_tries = randint(0, 10)
        number_of_penalties = randint(0, 10)
        # Theres a 10% chance of a drop goal
        n = randint(0, 1000) + 1
        number_of_drop_goals = 0
        if n == 1:
            number_of_drop_goals = 3
        elif n < 10:
            number_of_drop_goals = 2
        elif n < 100:
            number_of_drop_goals = 1

        # Simulate the tries
        for i in range(1, number_of_tries):
            # Did the home or away team score it (0=home, 1=away)
            event = "homeTry" if randint(0, 2) == 0 else "awayTry"
            description_number = randint(0, 4)
            description = self.descriptions[description_number]
            # Try is scored at a time between 1 and 80 minutes (inclusive)
            time_scored = randint(0, 80)
            time_diff = (g.get_minutes_since_midnight() + time_scored - self.current_time_since_midnight_in_minutes) \
                * 60

            # If the game has already started then set simulation to start now
            time_diff = 0 if time_diff < 0 else time_diff

            self.s.enter(time_diff + (g.get_minutes_since_midnight() + time_scored) / 60, 2, self.upload_event,
                         argument=(event, g, time_scored, description))

            # Try is converted 65-95% of the time based on kick position which is based on which
            # description is chosen above.
            conversion_number = randint(0, 100)
            conversion_percent = (95 - 9 * description_number)
            if conversion_number >= conversion_percent:
                conevent = event[0:4] + "Conversion"
                self.s.enter(time_diff + (g.get_minutes_since_midnight() + time_scored) / 60, 3, self.upload_event,
                             argument=(conevent, g, time_scored, ""))

        # Simulate the penalties
        for i in range(1, number_of_penalties):
            # Did the home or away team score it (0=home, 1=away)
            event = "homePenalty" if randint(0, 1) == 0 else "awayPenalty"
            # Try is scored at a time between 1 and 80 minutes (inclusive)
            time_scored = randint(0, 80)
            time_diff = (g.get_minutes_since_midnight() + time_scored - self.current_time_since_midnight_in_minutes) \
                * 60

            time_diff = 0 if time_diff < 0 else time_diff

            self.s.enter(time_diff + (g.get_minutes_since_midnight() + time_scored) / 60, 2, self.upload_event,
                         argument=(event, g, time_scored, ""))

        # Simulate the drop goals
        for i in range(1, number_of_drop_goals):
            # Did the home or away team score it (0=home, 1=away)
            event = "homeDropGoal" if randint(0, 1) == 0 else "awayDropGoal"
            # Try is scored at a time between 1 and 80 minutes (inclusive)
            time_scored = randint(0, 80)
            time_diff = (g.get_minutes_since_midnight() + time_scored - self.current_time_since_midnight_in_minutes) \
                * 60

            # If the game has already started then set simulation to start now
            time_diff = 0 if time_diff < 0 else time_diff

            self.s.enter(time_diff + (g.get_minutes_since_midnight() + time_scored) / 60, 2, self.upload_event,
                         argument=(event, g, time_scored, ""))
        
        # Simulate start of game
        time_diff = (g.get_minutes_since_midnight() - self.current_time_since_midnight_in_minutes) * 60

        # If the game has already started then set simulation to start now
        time_diff = 0 if time_diff < 0 else time_diff

        self.s.enter(time_diff + g.get_minutes_since_midnight() / 60, 1, self.upload_event,
                     argument=("strtGame", g, 0, ""))

        # Simulate half time
        time_diff = (g.get_minutes_since_midnight() + 40 - self.current_time_since_midnight_in_minutes) * 60

        time_diff = 0 if time_diff < 0 else time_diff

        self.s.enter(time_diff + (g.get_minutes_since_midnight() + 40) / 60, 4, self.upload_event,
                     argument=("halfTime", g, 40, ""))

        # Simulate full time
        time_diff = (g.get_minutes_since_midnight() + 40 - self.current_time_since_midnight_in_minutes) * 60

        time_diff = 0 if time_diff < 0 else time_diff

        self.s.enter(time_diff + (g.get_minutes_since_midnight() + 80) / 60, 4, self.upload_event,
                     argument=("fullTime", g, 80, ""))

    def set_timers(self):
        today = "20150402"
        for g in self.allGames:
            game_date = str(g.get_game_id())[0:8]
            if game_date == today:
                game_start_time = g.get_time_start()
                if len(game_start_time) > 0:
                    time_diff = (g.get_minutes_since_midnight() - self.current_time_since_midnight_in_minutes) \
                        * 60

                    # If the game has already started then set simulation to start now
                    time_diff = 0 if time_diff < 0 else time_diff

                    self.s.enter(time_diff + g.get_minutes_since_midnight() / 60, 1, self.game_simulator, kwargs={'g': g})

    def __init__(self):
        current_time = time.strftime("%H:%M")
        self.current_time_since_midnight_in_minutes = int(current_time[0:2]) * 60 + int(current_time[3:5])
        self.get_all_games()
        self.set_timers()
        self.s.run()

"""
Program Start
"""
Main()
