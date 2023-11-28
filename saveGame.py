import pickle
SAVE_DIR = "saves/"

class SaveGame:
    def save_game(self, saveName, saveData):
        """This method saves the game state to a file."""
        f = open(SAVE_DIR+saveName, "wb")
        pickle.dump(saveData.__dict__, f, 2)
        f.close()

    
    def load_game(self, saveName):
        """This method loads the game state from a file."""
        f = open(SAVE_DIR+saveName, "rb")
        saveData = pickle.load(f)
        f.close()
        return saveData