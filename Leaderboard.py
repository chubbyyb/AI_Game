import json

class Leaderboard:

    def __init__(self):
        with open("Leaderboard.json", "r") as leaderboard:
            jsonFile = json.load(leaderboard)

    def checkScore(self, name):
        try:
            print(jsonFile[name])
        except:
            print("User doesn't exist")
            self.createScore(name)

    def createScore(self):
        jsonFile[name] = 0
        self.saveScore()

    def changeScore(self, name, score):
        jsonFile[name] = score
        self.saveScore()

    def saveScore(self):
        with open("leaderboard.json", "w") as leaderboard:
            json.dump(jsonFile, leaderboard, indent=2)



