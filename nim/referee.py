import random

from nim.participant import Participant


class Referee(Participant):
    def __init__(self):
        super().__init__("裁判", "Jake")
        self.game = None

    def enter_game(self, game):
        self.game = game

    def introduce(self):
        self.talk(f"欢迎参加 Nim 游戏！")
        self.talk(f"左侧选手是 {self.game.player_left.name}，右侧选手是 {self.game.player_right.name}")

    def init_game(self):
        self.game.total_stones = random.randint(10, 30)
        self.game.maximum_take = random.randint(2, 7)
        self.talk(f"本次比赛共有 {self.game.total_stones} 个棋子。")
        self.talk("下面游戏进入猜先环节。")
        self.game.phase = "guessing"

    def choose_first_guesser(self):
        self.game.current_player = random.choice([self.game.player_left, self.game.player_right])
        self.talk(f"首先进行猜先的选手是 {self.game.current_player.name}")

    def evaluate_guess(self, player):
        if player.guess == self.game.maximum_take:
            first_player = self.game.current_player.name
            self.talk(f"{first_player} 猜先成功！")
            self.talk(f"下面游戏进入对战环节，由 {first_player} 先取子。")
            self.game.phase = "playing"
        else:
            self.switch_player()

    def check_game_over(self, remaining_stones):
        if remaining_stones == 0:
            winner = self.game.current_player.name
            self.talk(f"比赛结束，选手 {winner} 获胜！")
            self.game.phase = "finished"
        else:
            self.switch_player()

    def switch_player(self):
        if self.game.current_player == self.game.player_left:
            self.game.current_player = self.game.player_right
        else:
            self.game.current_player = self.game.player_left

    def run(self):
        if self.game.phase == "init":
            self.introduce()
            self.init_game()
        elif self.game.phase == "guessing":
            if not self.game.current_player:
                self.choose_first_guesser()
            else:
                self.evaluate_guess(self.game.current_player)
        elif self.game.phase == "playing":
            self.check_game_over(self.game.total_stones)
