import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *
from pitching_data_functions import *

# Main analysis script to go here

wainwright = Pitcher('Wainwright','wainwright_2017_processed.csv')
wainwright.makeGames()
for game in wainwright.game_list:
	game.runPipeline()

for game in wainwright.game_list:
	print(game.date)
	print(game.pitch_count)
	print(game.game_vel_FF)


