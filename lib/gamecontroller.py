import avango
import avango.osg
import time

from avango.script import field_has_changed

# import modules from local library
from lib.globals import *

class GAMECONTROLLER(avango.script.Script):

    counter = 30
    starttime = 0
    racetime = 0
    
     # constructor
    def __init__(self):
        self.super(GAMECONTROLLER).__init__()
        self.always_evaluate(True) # activate evaluate callback        
    
    def my_constructor(self, SCENE, NUM_OF_PLAYERS):
        self.num_of_players = NUM_OF_PLAYERS
        self.Scene = SCENE
        
        
    # callbacks
    def evaluate(self):
        self.count_countdown()
        
    def count_countdown(self):
        if self.num_of_players == 1:
            current_counter = self.counter - math.floor(time.time() - self.starttime)
            self.Scene.Player0.hud.change_text(4, str(current_counter))
            if current_counter <= 0:
                self.Scene.Player0.hud.change_text(4, "")
                #self.always_evaluate(False) # deactivate evaluate callback
        elif self.num_of_players == 2:
            current_counter = self.counter - math.floor(time.time() - self.starttime)
            self.Scene.Player0.hud.change_text(4, str(current_counter))
            self.Scene.Player1.hud.change_text(4, str(current_counter))
            if current_counter <= 0:
                self.Scene.Player0.hud.change_text(4, "")
                self.Scene.Player1.hud.change_text(4, "")
                #self.always_evaluate(False) # deactivate evaluate callback


    def start_countdown(self):
        self.counter = 33
        self.starttime = time.time()
        self.always_evaluate(True) # activate evaluate callback
