import json

class Leaderboard:

    def __init__(self):
        with open("Leaderboard.json", "r") as leaderboard:
            self.jsonFile = json.load(leaderboard)

    def checkScore(self, name):
        try:
            print(self.jsonFile[name])
        except:
            print("User doesn't exist")
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


