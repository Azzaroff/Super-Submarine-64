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
    oldcounter = 0
    number_of_laps = 1
    player0_data = []
    player1_data = []
    number_of_finished_races = 0
    num_of_players = 0
    
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
        now = time.time()
        if self.num_of_players == 1:
            current_counter = self.counter - math.floor(now - self.starttime)
            if current_counter != self.oldcounter :
                text = "%d" % (current_counter)
                self.Scene.Player0.hud.change_text(4, text)
                self.oldcounter = current_counter
            if current_counter <= 0:
                self.Scene.Player0.hud.change_text(4, "")
                self.Scene.Player0.race_start = True
                self.Scene.Player0.starttime = now
                self.Scene.Player0.lap_time = now
                self.always_evaluate(False) # deactivate evaluate callback
        elif self.num_of_players == 2:
            current_counter = self.counter - math.floor(now - self.starttime)
            if not current_counter == self.oldcounter :
                text = "%d" % (current_counter)
                self.Scene.Player0.hud.change_text(4, text)
                self.Scene.Player1.hud.change_text(4, text)
                self.oldcounter = current_counter
            if current_counter <= 0:
                self.Scene.Player0.hud.change_text(4, "")
                self.Scene.Player1.hud.change_text(4, "")
                self.Scene.Player0.race_start = True
                self.Scene.Player1.race_start = True
                self.Scene.Player0.starttime = now
                self.Scene.Player1.starttime = now
                self.Scene.Player0.lap_time = now
                self.Scene.Player1.lap_time = now
                self.always_evaluate(False) # deactivate evaluate callback
                
    def start_countdown(self, countdown):
        self.counter = countdown
        self.oldcounter = self.counter
        self.starttime = time.time()
        self.number_of_finished_races = 0
        
        if self.num_of_players == 1:
            self.Scene.Player0.reset_player()
            self.Scene.Player0.hud.reset_hud()
            self.player0_data = []
        elif self.num_of_players == 2:
            self.Scene.Player0.reset_player()
            self.Scene.Player1.reset_player()
            self.Scene.Player0.hud.reset_hud()
            self.Scene.Player1.hud.reset_hud()
            self.player0_data = []            
            self.player1_data = []
        
        self.always_evaluate(True) # activate evaluate callback
        
    def report_lap_data(self, playerid, lap_count, laptime):
        if self.num_of_players == 1:
            self.Scene.Player0.hud.change_text(0, str(lap_count))
            self.player0_data.append(laptime)
            if (lap_count-1) == self.number_of_laps:
                self.Scene.Player0.race_start = False
                self.Scene.Player0.hud.show_results(self.player0_data)
            else:
                #update hud with best lap
                bestlap = 10000000000000000000000
                for x in range (0, len(self.player0_data)):
                    if self.player0_data[x] < bestlap:
                        bestlap = self.player0_data[x]
                
                seconds = math.floor(bestlap)
                minutes = math.floor(seconds / 60)
                milliseconds = math.floor((bestlap - seconds)*1000)
                seconds = seconds - (minutes * 60)
                text = "%02d%s%02d%s%02d" % (minutes, ":", seconds, ":", milliseconds)
                self.Scene.Player0.hud.change_text(5, text)
                
        if self.num_of_players == 2:
            if (lap_count-1) == self.number_of_laps:
                if playerid == self.Scene.Player0.ID:
                    self.player0_data.append(laptime)
                    self.Scene.Player0.hud.change_text(0, str(lap_count))
                    self.number_of_finished_races = self.number_of_finished_races + 1
                    self.Scene.Player0.race_start = False
                else:
                    self.player1_data.append(laptime)
                    self.Scene.Player1.hud.change_text(0, str(lap_count))
                    self.number_of_finished_races = self.number_of_finished_races + 1
                    self.Scene.Player1.race_start = False
                if self.number_of_finished_races == self.num_of_players:
                    self.Scene.Player0.hud.show_results(self.player0_data, self.player1_data)
                    self.Scene.Player1.hud.show_results(self.player1_data, self.player0_data)
            else:
                if playerid == self.Scene.Player0.ID:
                    self.Scene.Player0.hud.change_text(0, str(lap_count))
                    self.player0_data.append(laptime)
                    #update hud with best lap
                    bestlap = 10000000000000000000000
                    for x in range (0, len(self.player0_data)):
                        if self.player0_data[x] < bestlap:
                            bestlap = self.player0_data[x]
                    
                    seconds = math.floor(bestlap)
                    minutes = math.floor(seconds / 60)
                    milliseconds = math.floor((bestlap - seconds)*1000)
                    seconds = seconds - (minutes * 60)
                    text = "%02d%s%02d%s%02d" % (minutes, ":", seconds, ":", milliseconds)
                    self.Scene.Player0.hud.change_text(5, text)
                else:
                    self.Scene.Player1.hud.change_text(0, lap_count)
                    self.player1_data.append(laptime)
                    #update hud with best lap
                    bestlap = 10000000000000000000000
                    for x in range (0, len(self.player1_data)):
                        if self.player1_data[x] < bestlap:
                            bestlap = self.player1_data[x]
                    
                    seconds = math.floor(bestlap)
                    minutes = math.floor(seconds / 60)
                    milliseconds = math.floor((bestlap - seconds)*1000)
                    seconds = seconds - (minutes * 60)
                    text = "%02d%s%02d%s%02d" % (minutes, ":", seconds, ":", milliseconds)
                    self.Scene.Player1.hud.change_text(5, text)
                    
    def change_race_position(self, playerid, position):
        offset = "/1"
        if self.num_of_players == 2:
            offset = "/2"
        if playerid == 0:
            self.Scene.Player0.hud.change_text(1, str(position) + offset)
        elif playerid == 1:
            self.Scene.Player1.hud.change_text(1, str(position) + offset)
        
        
