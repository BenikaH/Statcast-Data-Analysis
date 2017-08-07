import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *
from pitching_data_functions import *

# Tommy John Pitchers

pitcher_name1 = 'Volquez'
pitcher_data_file1 = 'volquez_2017.csv'

pitcher1 = Pitcher(pitcher_name1, pitcher_data_file1)
pitcher1.runClassifyPipeline()

pitcher_name2 = 'Ross'
pitcher_data_file2 = 'ross_2017.csv'

pitcher2 = Pitcher(pitcher_name2, pitcher_data_file2)
pitcher2.runClassifyPipeline()

pitcher_name3 = 'Pineda'
pitcher_data_file3 = 'pineda_2017.csv'

pitcher3 = Pitcher(pitcher_name3, pitcher_data_file3)
pitcher3.runClassifyPipeline()

pitcher_name4 = 'Miller'
pitcher_data_file4 = 'miller_2016.csv'

pitcher4 = Pitcher(pitcher_name4, pitcher_data_file4)
pitcher4.runClassifyPipeline()

pitcher_name5 = 'Anderson'
pitcher_data_file5 = 'anderson_2016.csv'

pitcher5 = Pitcher(pitcher_name5, pitcher_data_file5)
pitcher5.runClassifyPipeline()

pitcher_name6 = 'Reyes'
pitcher_data_file6 = 'reyes_2016.csv'

pitcher6 = Pitcher(pitcher_name6, pitcher_data_file6)
pitcher6.runClassifyPipeline()

pitcher_name7 = 'Rea'
pitcher_data_file7 = 'rea_2016.csv'

pitcher7 = Pitcher(pitcher_name7, pitcher_data_file7)
pitcher7.runClassifyPipeline()

pitcher_name8 = 'Eovaldi'
pitcher_data_file8 = 'eovaldi_2016.csv'

pitcher8 = Pitcher(pitcher_name8, pitcher_data_file8)
pitcher8.runClassifyPipeline()

pitcher_name9 = 'Topeano'
pitcher_data_file9 = 'tropeano_2016.csv'

pitcher9 = Pitcher(pitcher_name9, pitcher_data_file9)
pitcher9.runClassifyPipeline()

# Healthy Pitchers

pitcher_name10 = 'Koehler'
pitcher_data_file10 = 'koehler_2016.csv'

pitcher10 = Pitcher(pitcher_name10, pitcher_data_file10)
pitcher10.runClassifyPipeline()

pitcher_name11 = 'Scherzer'
pitcher_data_file11 = 'scherzer_2016.csv'

pitcher11 = Pitcher(pitcher_name11, pitcher_data_file11)
pitcher11.runClassifyPipeline()

pitcher_name12 = 'Tanaka'
pitcher_data_file12 = 'tanaka_2016.csv'

pitcher12 = Pitcher(pitcher_name12, pitcher_data_file12)
pitcher12.runClassifyPipeline()

pitcher_name13 = 'Ray'
pitcher_data_file13 = 'ray_2016.csv'

pitcher13 = Pitcher(pitcher_name13, pitcher_data_file13)
pitcher13.runClassifyPipeline()

pitcher_name14 = 'Kluber'
pitcher_data_file14 = 'kluber_2016.csv'

pitcher14 = Pitcher(pitcher_name14, pitcher_data_file14)
pitcher14.runClassifyPipeline()

pitcher_name15 = 'Martinez'
pitcher_data_file15 = 'martinez_2016.csv'

pitcher15 = Pitcher(pitcher_name15, pitcher_data_file15)
pitcher15.runClassifyPipeline()

pitcher_name16 = 'Perdomo'
pitcher_data_file16 = 'perdomo_2016.csv'

pitcher16 = Pitcher(pitcher_name16, pitcher_data_file16)
pitcher16.runClassifyPipeline()

pitcher_name17 = 'Sabathia'
pitcher_data_file17 = 'sabathia_2016.csv'

pitcher17 = Pitcher(pitcher_name17, pitcher_data_file17)
pitcher17.runClassifyPipeline()

pitcher_name18 = 'Shoemaker'
pitcher_data_file18 = 'shoemaker_2016.csv'

pitcher18 = Pitcher(pitcher_name18, pitcher_data_file18)
pitcher18.runClassifyPipeline()


pitcher_list = [pitcher1, pitcher2, pitcher3, pitcher4, pitcher5, pitcher6, pitcher7, pitcher8, pitcher9, \
pitcher10, pitcher11, pitcher12, pitcher13, pitcher14, pitcher15, pitcher16, pitcher17, pitcher18]

output = np.zeros((len(pitcher_list),6))

row = 0
for pitcher in pitcher_list:
	print(pitcher.name)
	print(pitcher.number_fastballs)
	print(pitcher.number_offspeed)
	print(pitcher.total_pitches)
	print(pitcher.avg_fastball_vel)
	print(pitcher.fastball_freq)

	output[row,0] = row + 1
	output[row,1] = pitcher.number_fastballs
	output[row,2] = pitcher.number_offspeed
	output[row,3] = pitcher.total_pitches
	output[row,4] = pitcher.avg_fastball_vel
	output[row,5] = pitcher.fastball_freq
	row += 1

np.savetxt('TJ_fastball_freq.csv', output, delimiter=',')
