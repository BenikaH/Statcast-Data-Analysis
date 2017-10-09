import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *
from pitching_data_functions import *

pitch_cutoff = 1000
type_cutoff = 50
pitcher_list = []
pitcher_name_list = []

filename_list = ['angels_SP_2016.csv', 'astros_SP_2016.csv', 'athletics_SP_2016.csv', 'bluejays_SP_2016.csv', 'braves_SP_2016.csv', \
'brewers_SP_2016.csv', 'cardinals_SP_2016.csv', 'cubs_SP_2016.csv', 'dbacks_SP_2016.csv', 'dodgers_SP_2016.csv', 'giants_SP_2016.csv', \
'indians_SP_2016.csv', 'mariners_SP_2016.csv', 'marlins_SP_2016.csv', 'mets_SP_2016.csv', 'nationals_SP_2016.csv', 'orioles_SP_2016.csv', \
'padres_SP_2016.csv', 'phillies_SP_2016.csv', 'pirates_SP_2016.csv', 'rangers_SP_2016.csv', 'rays_SP_2016.csv', 'reds_SP_2016.csv', \
'redsox_SP_2016.csv', 'rockies_SP_2016.csv', 'royals_SP_2016.csv', 'tigers_SP_2016.csv', 'twins_SP_2016.csv', 'whitesox_SP_2016.csv', \
'yankees_SP_2016.csv']

target_file = 'TARGET_REF_DATA.csv'
parameter_file = 'Whiteside_SP_Parameters.csv' # Post-hoc ONLY!

for filename in filename_list:
	makePitchers(filename, pitcher_list)

print("Number of Pitchers:",len(pitcher_list))

pitcher_count = 0
for pitcher in pitcher_list:
	pitcher.sortPitches()
	if len(pitcher.pitch_list) >= pitch_cutoff and len(pitcher.FF) > type_cutoff and len(pitcher.SL) > type_cutoff and len(pitcher.CH) > type_cutoff and len(pitcher.CU) > type_cutoff:
		pitcher_count += 1
		pitcher.classifyPitches()
		pitcher.classifyMetrics()

		fastball_prop = pitchFrequency(pitcher.FF, pitcher.all_pitches)
		change_prop = pitchFrequency(pitcher.CH, pitcher.all_pitches)
		slider_prop = pitchFrequency(pitcher.SL, pitcher.all_pitches)
		curveball_prop = pitchFrequency(pitcher.CU, pitcher.all_pitches)

		velocity_FF = averageVelocity(pitcher.FF)
		velocity_CH = averageVelocity(pitcher.CH)
		velocity_SL = averageVelocity(pitcher.SL)
		velocity_CU = averageVelocity(pitcher.CU)

		rel_x_FF, rel_z_FF = averageRelease(pitcher.FF)
		rel_x_FF = np.absolute(rel_x_FF)
		rel_x_CH, rel_z_CH = averageRelease(pitcher.CH)
		rel_x_CH = np.absolute(rel_x_CH)
		rel_x_SL, rel_z_SL = averageRelease(pitcher.SL)
		rel_x_SL = np.absolute(rel_x_SL)
		rel_x_CU, rel_z_CU = averageRelease(pitcher.CU)
		rel_x_CU = np.absolute(rel_x_CU)

		pfx_x_FF, pfx_z_FF = averagePfx(pitcher.FF)
		pfx_x_FF = np.absolute(pfx_x_FF)
		pfx_x_CH, pfx_z_CH = averagePfx(pitcher.CH)
		pfx_x_CH = np.absolute(pfx_x_CH)
		pfx_x_SL, pfx_z_SL = averagePfx(pitcher.SL)
		pfx_x_SL = np.absolute(pfx_x_SL)
		pfx_x_CU, pfx_z_CU = averagePfx(pitcher.CU)
		pfx_x_CU = np.absolute(pfx_x_CU)

		velvar_FF = velocitySTDev(pitcher.FF)
		velvar_CH = velocitySTDev(pitcher.CH)
		velvar_SL = velocitySTDev(pitcher.SL)
		velvar_CU = velocitySTDev(pitcher.CU)

		rel_2D_FF = averageRelease2D(pitcher.FF)
		rel_2D_CH = averageRelease2D(pitcher.CH)
		rel_2D_SL = averageRelease2D(pitcher.SL)
		rel_2D_CU = averageRelease2D(pitcher.CU)

		relDEV_2D_FF = releaseDeviation2D(pitcher.FF)
		relDEV_2D_CH = releaseDeviation2D(pitcher.CH)
		relDEV_2D_SL = releaseDeviation2D(pitcher.SL)
		relDEV_2D_CU = releaseDeviation2D(pitcher.CU)

		pfxDev_x_FF, pfxDev_z_FF = deviationPfx(pitcher.FF)
		pfxDev_x_CH, pfxDev_z_CH = deviationPfx(pitcher.CH)
		pfxDev_x_SL, pfxDev_z_SL = deviationPfx(pitcher.SL)
		pfxDev_x_CU, pfxDev_z_CU = deviationPfx(pitcher.CU)

		ellipse_FF = releaseEllipse(pitcher.FF)
		ellipse_CH = releaseEllipse(pitcher.CH)
		ellipse_SL = releaseEllipse(pitcher.SL)
		ellipse_CU = releaseEllipse(pitcher.CU)

		with open(target_file, newline='') as file:
			reader = csv.reader(file)
			for row in reader:
				if row[0] == pitcher.name:
					age = int(row[2])
					ERA = float(row[3])
					FIP = float(row[5])
					WAR = float(row[6])

		if True:
			with open(parameter_file, newline='') as file:
				reader = csv.reader(file)
				for row in reader:
					if row[0] == pitcher.name:
						height = float(row[2])
						weight = float(row[3])
			
			#rel_x_FF /= height
			rel_z_FF /= height
			#rel_x_CH /= height
			rel_z_CH /= height
			#rel_x_SL /= height
			rel_z_SL /= height
			#rel_x_CU /= height
			rel_z_CU /= height
			rel_2D_FF /= height
			rel_2D_CH /= height
			rel_2D_SL /= height
			rel_2D_CU /= height


		output_row = [fastball_prop, change_prop, slider_prop, curveball_prop, \
		velocity_FF, velocity_CH, velocity_SL, velocity_CU, rel_x_FF, rel_z_FF, \
		rel_x_CH, rel_z_CH, rel_x_SL, rel_z_SL, rel_x_CU, rel_z_CU, pfx_x_FF, \
		pfx_z_FF, pfx_x_CH, pfx_z_CH, pfx_x_SL, pfx_z_SL, pfx_x_CU, pfx_z_CU, \
		velvar_FF, velvar_CH, velvar_SL, velvar_CU, rel_2D_FF, rel_2D_CH, rel_2D_SL, \
		rel_2D_CU, relDEV_2D_FF, relDEV_2D_CH, relDEV_2D_SL, relDEV_2D_CU, pfxDev_x_FF, \
		pfxDev_z_FF, pfxDev_x_CH, pfxDev_z_CH, pfxDev_x_SL, pfxDev_z_SL, pfxDev_x_CU, pfxDev_z_CU, \
		ellipse_FF, ellipse_CH, ellipse_SL, ellipse_CU]

		output_row = np.array(output_row)
		target_value = np.array([pitcher_count, FIP])

		print(pitcher.name)
		print(FIP)

		pitcher_name_list.append(pitcher.name)
		if pitcher_count == 1:
			output = output_row
			target_output = target_value
		else:
			output = np.vstack((output,output_row))
			target_output = np.vstack((target_output,target_value))

target_output = target_output[np.argsort(target_output[:, 1])]

N = pitcher_count
rank_array = np.zeros((N,1))

for i in range(N):
	rank_array[i,0] = i + 1
target_output = np.hstack((target_output,rank_array))

target_output = target_output[np.argsort(target_output[:, 0])]

print("Number of Qualifying Pitchers:",pitcher_count)
F = open("SP_NAMES.csv","w")
for name in pitcher_name_list:
	F.write(name)
	F.write('\n')
F.close()
np.savetxt('SP_OUTPUT.csv', output, delimiter=',')
np.savetxt('TARGET_OUTPUT.csv',target_output, delimiter=',')