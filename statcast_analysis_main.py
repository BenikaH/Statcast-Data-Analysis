import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *
from pitching_data_functions import *

# Main analysis script to go here

pitcher_name = 'Wainwright'
pitcher_data_file = 'wainwright_2017.csv'

pitcher1 = Pitcher('Wainwright','wainwright_2017.csv')
pitcher1.makeGames()
for game in pitcher1.game_list:
	game.runPipeline()

print(pitcher1.name)
for game in pitcher1.game_list:
	print(game.date)
	print(game.pitch_count)
	print(game.game_vel_FF)
