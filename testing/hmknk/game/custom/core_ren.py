# Core Game Python by Tanix
#
# 13 Apr 2025

"""renpy
init python:
"""

import base64
import json
import logging
import logging.handlers
from random import randint
import random

#Set Config developer to False for Production/Release
config.developer = True

class base_class(renpy.python.RevertableObject):

    def __getstate__(self):
        return vars(self).copy()

    def __setstate__(self, new_dict):
        self.__dict__.update(new_dict)


class core(base_class):
    """Game Core Class
    """

    def __init__(self):
        """Game Code Initilalization
        """
        self.log  = False
        if config.developer:
            self.log = True
            self.tanix_log = self.start_log()
            self.tanix_log.info(f"Starting Game")
        
        self.content = self.load_content("refdata.json")
        self.next_chapter = 0
        self.chapter = 0
        self.minigame1_background = None
        self.elements = []
        self.card_selected = []
        self.shuffle_cards = {}
        self.card_facedown = {}
        self.card_display = {}
        self.card_score = 0

    def start_log(self):
        l = logging.getLogger("tanix_log")
        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        fileHandler = logging.FileHandler(f"{config.gamedir}/tanix.log", mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(logging.DEBUG)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

        return logging.getLogger("tanix_log")
    
    def load_content(self, datafile):
        with open("{}/{}".format(config.gamedir, datafile), 'rb') as f:
            return json.load(f)

    def enc_data(self, inputData):
        return base64.b64encode(inputData)

    def dec_data(self, inputData):
        return base64.b64decode(inputData)

    def start_minigame1(self):
        #load assets
        self.minigame1_background = "gui/custom/minigame1/minigame1.png"
        self.elements = [{"sprite":"gui/custom/minigame1/light_%s.png","pos":(500,340),"selected":False},
                         {"sprite":"gui/custom/minigame1/basket_%s.png","pos":(550,1200),"selected":False},
                         {"sprite":"gui/custom/minigame1/closet_%s.png","pos":(145,1000),"selected":False},
                         {"sprite":"gui/custom/minigame1/bed_%s.png","pos":(230,1350),"selected":False}]
        self.random_place = randint(0, len(self.elements)-1)
        self.elements[self.random_place]["selected"] = True
    
    def shuffle(self):
        cards = list(self.content["cards"].keys())
        cards = [x for pair in zip(cards,cards) for x in pair]
        card_keys = []
        random.shuffle(cards)
        for i in range(0,2):
            for j in range(0,4):
                card_keys.append(f"{i}{j}")
                self.card_facedown[f"{i}{j}"] =  "FACE DOWN CARD"
        self.card_display = self.card_facedown.copy()
        self.card_selected = []
        self.card_score = 0
        self.shuffle_cards =  dict(zip(card_keys, cards))
        self.tanix_log.info(f"card game {self.shuffle_cards}")  

    def select_card(self,i,j):
        if self.card_score == 4 or f"{i}{j}" in self.card_selected:
            self.tanix_log.info(f"End game/Skip")
            return None        
        if len(self.card_selected) == 2:            
            self.card_selected = []
            self.card_display = self.card_facedown.copy()        
        self.card_selected.append(f"{i}{j}")
        self.card_display[f"{i}{j}"] = self.shuffle_cards [f"{i}{j}"]  
        self.tanix_log.info(f"card game {self.card_selected}")
        if len(self.card_selected) == 2 and self.shuffle_cards [self.card_selected[0]] == self.shuffle_cards [self.card_selected[1]]:
                self.card_score += 1
                self.tanix_log.info(f"card game MATCH")
                self.card_facedown = self.card_display.copy()