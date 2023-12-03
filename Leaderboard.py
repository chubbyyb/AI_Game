import json

class Leaderboard:

    def __init__(self):
        with open("Leaderboard.json", "r") as leaderboard:
            self.jsonFile = json.load(leaderboard)

    def checkScore(self, name):
        try:
            print(f"Your score is: {self.jsonFile[name]}")
        except:
            print("This is your first time playing! Welcome!")
            self.createScore(name)

    def createScore(self, name):
        self.jsonFile[name] = 0
        self.saveScore()

    def changeScore(self, name, score):
        self.jsonFile[name] = score
        self.saveScore()

    def saveScore(self):
        with open("leaderboard.json", "w") as leaderboard:
            json.dump(self.jsonFile, leaderboard, indent=2)


