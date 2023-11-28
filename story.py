
from openai import OpenAI
import json
import requests

STORIES_DIR = "stories/"

proompt = '''
Create a investigative story about one of the following:
    "1. A mysterious disappearance in a small town.",
    "2. Unexplained phenomena in a remote location.",
    "3. Corporate corruption within a powerful tech company.",
    "4. Ancient artifacts with mysterious powers resurfacing.",
    "5. A secret society operating in plain sight.",
    "6. Government experiments gone wrong.",
    "7. Time travel anomalies affecting a community.",
    "8. A renowned scientist's controversial discovery."
    "9. Make your own!"

The json key of the clues will be the name of the door, e.g (front door), and the value will be the clue within that room.
The title may not be more than 16 characters long.
The story should be one json value
The characters can all be innocent, or all be guilty, or any combination of the two.
prompt will be a prompt for the AI to generate an image of the story.

Make sure its in a json file with the following format:
  "title": "",
  "story": [
    "",
    "",
    "'"
  ],
  "prompt": "",
 "characters": {
    "suspect": {
      "name": ,
      "alibi": ,
      "confirmation": ",
      "mood": ,
      "innocent": true/false
    },
    "witness": {
      "name": ,
      "observation": ,
      "description": ,
      "mood": ,
      "innocent": true/false
    },
    "npcs": [
      {
        "name": ,
        "dialogue": ,
        "mood": ,
        "innocent": true/false
      },
      {
        "name": "",
        "dialogue": "",
        "mood": ,
        "innocent": true/false
      }
    ]
  },
  "clues": {
    "": "",
    "": "",
    "": "",
    "": ""
  }
'''


class Story:
    def __init__(self):
        self.api_key = "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"
        self.client = OpenAI(api_key=self.api_key)

    def make_story(self):
        completion = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=1.3, # Do not increase above 1.5 or you will get gobblde goob
            messages=[{"role": "user", "content": proompt}])
        try:
            self.json_content = json.loads(completion.choices[0].message.content)
            self.generate_image(self.json_content["prompt"], self.json_content["title"])
            return self.save_story()
        except:
            print("AI Generated story failed")
            return 0

    def save_story(self):
        with open(STORIES_DIR+self.json_content["title"]+".json", "w") as f:
            json.dump(self.json_content, f, indent=4)
            return STORIES_DIR+self.json_content["title"]+".json"

    def get_story(self, title):
        with open(STORIES_DIR+title+".json", "r") as f:
            return json.load(f)
        
    def generate_image(self, prompt, name):
        image = self.client.images.generate(
            prompt=prompt,
            n=1,
            size='512x512'
        )

        with open(f"{STORIES_DIR+name}.png", "wb") as f:
            f.write(requests.get(image.dict()["data"][0]["url"]).content)


