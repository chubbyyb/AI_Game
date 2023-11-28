# CMPU 2016
# KEITH SALHANI
# C22322811
# C22322811@mytudublin.ie
# LAST EDITS: 09:11:2023

# Added class loggable
# made characters return interaction
# logged interactions
# Added terminal colors
# Added ascci art
# Added Sentiment Analysis

from abc import ABC, abstractmethod # for abstract classes
from datetime import datetime # for timestamps
from termcolor import colored # for colored text
from art import * # for the title
#from transformers import pipeline # for questioning the suspects nicely : turning off because needs tensorflow/pytorch and im on school wifi

'''
pip install art
pip install termcolor
pip install -q transformers
'''

#sentiment_pipeline = pipeline("sentiment-analysis")

class Loggable:
    def __init__(self):
        self._logs = []

    # getter
    @property
    def logs(self):
        return self._logs

    # setter so i get marks
    @logs.setter
    def logs(self, value):
        self.logs = value
    
    def add_log(self, message):
        '''This method adds a log entry to the logs list.'''
        # create a timestamp for the log entry
        current_time = datetime.now()

        #12 hour format
        flat_time = current_time.strftime("%I:%M %p")

        # combine the message and the timestamp
        combined_message = f"{flat_time} - {message}"

        self._logs.append(combined_message) # add the message to the logs list
        #print(colored(f"Logged: {message}", "red", attrs=['dark'])) # comment this out to remove logs

    def save_logs_to_file(self,filename):
        for i in self.logs:
            with open(filename+str(".txt"), "a") as f:
                f.write(i + "\n")




class CrimeScene:
    def __init__(self, location):
        self.location = location
        self.__clues = [] # private
        self.__investigated = False # private

    # getter
    @property
    def investigated(self):
        return self.__investigated

    # setter
    @investigated.setter
    def investigated(self, value):
        if isinstance(value, bool):
            self.__investigated = value
        else:
            print("investigated is expected to be a boolean.")

    def add_clue(self, clue):
        """This method adds clues to the crime scene investigation."""
        self.__clues.append(clue)

    def review_clues(self):
        """At the moment there are no checks on who can see the clues. We
        might need some further protection here."""
        return self.__clues
    
crime_scene = CrimeScene("Mansion's Drawing Room")

class Character(ABC):
    """ The Character class serves as the base class, providing common
    attributes and methods for characters. The Suspect and Witness classes
    are subclasses that inherit from Character and introduce their unique
    attributes and methods. """

    def __init__(self, name, dialogue):
        self._name = name
        self._dialogue = dialogue
        self._interacted = False

    # if it is not of benefit for the design of the system
    # you do not need to explicitely provide getter and setter
    # methods. Instead, the behavior methods might be sufficient,
    # as I have chosen in this case.
    
    def interact(self):
        pass
    
    @abstractmethod
    def perform_action(self):
        pass

class Suspect(Character):
    """This is a special type of character. This is the suspect in our crime
    investigation."""

    def __init__(self, name, dialogue, confirmedBy):
        super().__init__(name, dialogue)  # Call the constructor of the base class
        self._confirmedBy = confirmedBy  # Add the unique attribute for Suspect

    @property
    def susDesc(self):
        return self._confirmedBy
    
    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}\n - {self._confirmedBy}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction
    
    def perform_action(self):
        # this piece of code is a monstrocity. Do not read it.
        # There is an fstring within an fstring
        # I didnt even know that was possible
        print(f"\n {colored(f'Suspect {self._name}', 'red')} :",
               colored(f"{self._dialogue}\n - {self._confirmedBy}\n", "green", attrs=['bold']))
        crime_scene.add_clue("Mr.Smith was in the library")
        return(f"Suspect {self._name}: {self._dialogue} - {self._confirmedBy}")
        
        


class Witness(Character):
    """This class is the witness. This person has either seen or heard
    something to do with the crime."""
    def __init__(self, name, dialogue, description):
        super().__init__(name, dialogue)  # Call the constructor of the base class
        self._description = description  # Add the unique attribute for Suspect

    @property
    def whoConfirmed(self):
        return self._description
    
    def interact(self):
        if not self._interacted:
            interaction = f"{self._name}: {self._dialogue}\n - {self._confirmedBy}"
            self._interacted = True
        else:
            interaction = f"{self._name} is no longer interested in talking."

        return interaction
    
    def perform_action(self):
        print(colored(f"Witness {self._name}","blue"), ":",
               colored(f"{self._dialogue}\n - Description: {self._description}\n", "green", attrs=['bold']))
        crime_scene.add_clue("Ms. Parker saw a suspicious figure in dark clothing")
        return(f"Witness {self._name}: {self._dialogue} - Description: {self._description}")

class NPC(Character):
    def __init__(self, name, dialogue, mood):
        super().__init__(name, dialogue)
        self._mood = mood

    def perform_action(self):
        print(colored(f"NPC {self._name}", "cyan"), colored(f": {self._dialogue}", "green" , attrs=['bold']) , "\n")
        return(f"NPC {self._name}: {self._dialogue}")





class Game:
    """The Game class interacts with the other objects to facilitate game
    play."""

    def __init__(self):
        self.running = True
        self.game_started = False
        self.characters_interacted = False
        self.crime_scene = crime_scene
        self.doors_investigated = {"Front Door": False, "Library Door": False, "Kitchen Door": False, "Lobby": False} # dictionary to keep track of investigated rooms
        self.doors = ['Front Door', 'Library Door', 'Kitchen Door'] # state the scene names that exist
        self.doorSelected = 0 # door selection input
        self.currentScene = 'Lobby' # tracks current scene
        self.peopleSpokenTo = False
        self.NPCsSpokenTo = False
        # new from here:
        self.suspect = Suspect("Mr. Smith", "I was in the library all evening.", "Confirmed by the butler.")
        self.witness = Witness("Ms. Parker", "I saw someone near the window at the time of the incident.", "Suspicious figure in dark clothing.")
        self.johnNPC = NPC("John - Butler", "ay im wooolkin heere.", "Angry")
        self.maryNPC = NPC("Mary - Maid", "I was cooking some lasanga in the living room.", "Happy")
        self.loggable = Loggable()
        self.__eloggable = Loggable()
        self.loggable.add_log("Game started")
        #self.player_name = ""
        # we add a few more doors to our game. This changes out the very
        # generic doors from the previous versions. This also makes doors
        # available at all times in the menu options.


    @property
    def eLogs(self):
        return self.__eloggable.logs
    
        # ---- your door related variables go here ----
    def run(self):
        tprint("The Poirot Mystery")
        print("You are about to embark on a thrilling adventure as a detective.")
        print("Your expertise is needed to solve a complex case and unveil "
              "the truth.")

        while self.running:
            self.update()

    def update(self):
        if not self.game_started:
            # Python wont throw an error if we enter a number
            # Because its taking the input as a string
            # so we dont have to worry about the program crashing
            try:
                player_input = input(colored("Press 'q' to quit or 's' to start:\n ","white"))
                if player_input.lower() == "q": 
                    print("Where would you like to save the logs?")
                    filename = input("Enter the filename: ")
                    self.loggable.save_logs_to_file(filename)
                    self.running = False
                elif player_input.lower() == "s":
                    self.game_started = True
                    self.start_game()
            except KeyboardInterrupt as ke: # check if user pressed ctrl C
                self.__eloggable.add_log(f"Error: User interrupted program.")
            except Exception as e: # catch all other errors
                self.__eloggable.add_log(f"Error: {e}")

        else:
            # this changed a little compared to the previous version. We
            # exchanged the investigate i for i=interact in order to speak
            # to our characters. We also included a general option to check
            # on doors.

            player_input = input(colored("Press 'q' to quit, 'c' to continue, "
                                 "'i' to interact, 'e' to examine clues, "
                                 "'r' to review your clues, "
                                 "'L' to look at the logs, "
                                 "or 'doors' to choose a door: ", "white"))
            if player_input.lower() == "q":
                print("Would you like to save the logs (y/n)?")
                save_logs = str(input())
                if save_logs.lower() == "y":
                    filename = str(input("Enter the filename: "))
                    self.loggable.save_logs_to_file(filename)
                    self.__eloggable.save_logs_to_file(str("Error_")+filename)
                    
                self.running = False
            elif player_input.lower() == "c":
                self.continue_game()
            elif player_input.lower() == "i":
                self.interact_with_characters()
            elif player_input.lower() == "e":
                self.examine_clues()
            elif player_input.lower() == "r":
                clues = self.crime_scene.review_clues()
                if clues:
                    print(colored(clues,"light_yellow"))
                else:
                    print(colored("You have not found any clues yet."),"red")
            elif player_input.lower() == "l":
                print(self.loggable.logs)
            elif player_input.lower() == "doors":
                self.choose_door()
            
            self.loggable.add_log(f"Input: {player_input}")

    def start_game(self):
        self.player_name = input(colored("Enter your detective's name: ", "white"))
        print(f"Welcome, Detective {self.player_name}!")
        print("You find yourself in the opulent drawing room of a grand "
              "mansion.")
        print("As the famous detective, you're here to solve the mysterious "
              "case of...")
        print("'The Missing Diamond Necklace'.")
        print("Put your detective skills to the test and unveil the truth!")

    def interact_with_characters(self):
        """The interact_with_characters method within the Game class
        demonstrates the interaction with characters, where each
        character's dialogue and unique actions (e.g., providing an alibi,
        sharing an observation) are
        displayed. """

        try:
            userInput = int(input(colored("Press 1 to interact with the witness and suspect.\nPress 2 to interact with the NPCs: ", "white")))
            #userMessage = str(input(colored(f"What would you like to say? \n {self.player_name}: ", 'white')))
            #sentiment = sentiment_pipeline(userMessage)
            #sentiment = sentiment[0].get('label')
            #if(sentiment == 'NEGATIVE'): 
            #    print(colored("They witnesses and suspects refuse to speak to you because you are rude!", 'red')) 
            #    return
            
            if(userInput == 1):
                if(self.peopleSpokenTo): 
                    print("You have spoken to the people already - they no longer wish to speak to you")
                    return

                characters = [self.suspect, self.witness]
                for character in characters:
                    self.loggable.add_log(character.perform_action())
                self.peopleSpokenTo = True
            elif(userInput == 2):
                if(self.NPCsSpokenTo): 
                    print("You have spoken to the NPCs already - they no longer wish to speak to you")
                    return
                characters = [self.johnNPC, self.maryNPC]
                for character in characters:
                    self.loggable.add_log(character.perform_action())
                self.NPCsSpokenTo = True
        except ValueError as ve:
            self.__eloggable.add_log(f"Error: {ve}")
        


    def examine_clues(self):
        if not self.crime_scene.investigated:
            if(self.currentScene == "Front Door" and not self.doors_investigated[self.currentScene]):
                self.loggable.add_log("You investigate the room - You find a bloody handprint on the handle")
                print(colored("You investigate the room - You find a bloody handprint on the handle","light_yellow"))
                self.crime_scene.add_clue("Bloody handprint")
            elif(self.currentScene == "Library Door" and not self.doors_investigated[self.currentScene]):
                self.loggable.add_log("You investigate the room - You find a ring")
                print(colored("You investigate the room - You find a ring","light_yellow"))
                self.crime_scene.add_clue("Ring")
            elif(self.currentScene == "Kitchen Door" and not self.doors_investigated[self.currentScene]):
                self.loggable.add_log("You investigate the kitchen - You find a kettle with hot water in it")
                print(colored("You investigate the kitchen - You find a kettle with hot water in it","light_yellow"))
                self.crime_scene.add_clue("Boiling kettle")
            elif(self.currentScene == "Lobby" and not self.doors_investigated[self.currentScene]):
                self.loggable.add_log("You find a key in the door")
                print(colored("You find a key in the door","light_yellow"))
                self.crime_scene.add_clue("A key")
            else:
                print(f"Already investigated {self.currentScene}")
            self.doors_investigated[self.currentScene] = True

            if(not any(self.doors_investigated) == True):
                self.crime_scene.investigated = True
        else:
            print("You've already examined the crime scene clues.")


    def enter_room(self):
        if(self.doorSelected == 1):
            self.loggable.add_log("You enter the front door")
            print("You enter the front door")
        elif(self.doorSelected == 2):
            self.loggable.add_log("You enter the library door")
            print("You enter the library door")
        elif(self.doorSelected == 3):
            self.loggable.add_log("You enter the kitchen door")
            print("You enter the kitchen door")

    def choose_door(self):
        """This method handles the door examination option. User input is
        being handled. The user can make 3 choices: door 1 leads to the
        front door, door 2 leads to the library and door 3 leads to the
        kitchen. Wrong user input is being handled via print outs for error
        handling."""
        print(colored("1. Front Door\n2. Library door\n3. Kitchen Door", "white"))
        self.doors = ['Front Door', 'Library Door', 'Kitchen Door'] # state the scene names that exist

        try:
            self.doorSelected = int(input())
            self.currentScene = self.doors[self.doorSelected-1]
            self.enter_room()
        except IndexError as ie:
            self.__eloggable.add_log(f"Error: door {self.doorSelected} - {ie}")
        except ValueError as ve:
            self.__eloggable.add_log(f"Error: {ve}")

        

    def continue_game(self):
        self.loggable.add_log("You continue your investigation, determined to solve the mystery...")
        print("You continue your investigation, determined to solve the mystery...")


if __name__ == "__main__":
    game = Game()
    game.run()

    print("Game Logs:\n ")
    for log in (game.loggable.logs):
        print(log)

    print("\n")

    print("Error Logs:\n ")
    for eLog in (game.eLogs):
        print(eLog)