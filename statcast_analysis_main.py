import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *
from pitching_data_functions import *

# Main analysis script to go here

pitcher_name = 'Martinez'
pitcher_data_file = 'martinez_2017.csv'

pitcher1 = Pitcher(pitcher_name, pitcher_data_file)
pitcher1.makeGames()
for game in pitcher1.game_list:
	game.runMainPipeline()

print(pitcher1.name)
for game in pitcher1.game_list:
	print(game.date)
	print(game.pitch_count)
	print(game.game_vel_FF)
