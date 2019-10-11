import os


class GameStats:

    def __init__(self, ai_settings):
        f = open('high_scores.txt', 'r')
        self.ai_settings = ai_settings
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
        self.reset_stats()
        self.game_active = False
        self.show_high_score = False
        if os.path.getsize("high_scores.txt") != 0:
            self.high_score = int(f.read())
        else:
            self.high_score = 0



    def write(self):
        f = open("high_scores.txt", 'w')
        f.write(str(self.high_score))

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
