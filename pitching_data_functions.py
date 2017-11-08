# Functions to support the statcast data analysis
import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *

# function returns the average value of the pitch subset passed to it
def averageVelocity(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	total_vel = 0
	for pitch in pitch_subset:
		total_vel += pitch.velocity
	avg_vel = float(total_vel/len(pitch_subset))
	return avg_vel

# function takes a pitch subset list and the total pitch list as parameters
# returns the proportion of pitches that is the pitch subset out of the total pitches
def pitchFrequency(pitch_subset, all_pitches):
	N_TOTAL = len(all_pitches)
	N_TYPE = len(pitch_subset)
	freq = N_TYPE / N_TOTAL
	return freq

# returns the statical variance in the velocity of the pitch subset
def velocityVariance(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	vel_array = []
	for pitch in pitch_subset:
		vel_array.append(pitch.velocity)
	vel_array = np.array(vel_array)
	return vel_array.var()

# returns the statical standard deviation of the velocity of the pitch subset
def velocitySTDev(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	vel_array = []
	for pitch in pitch_subset:
		vel_array.append(pitch.velocity)
	vel_array = np.array(vel_array)
	return vel_array.std()	

# function returns the average spin rate of the pitches in the subset
def averageSpin(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	spin_array = []
	for pitch in pitch_subset:
		spin_array.append(pitch.spin_rate)
	spin_array = np.array(spin_array)
	return spin_array.mean()

# function returns the average horizontal and vertical release point for pitches in the subset
def averageRelease(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	total_x = 0
	total_z = 0
	for pitch in pitch_subset:
		total_x += pitch.rel_x
		total_z += pitch.rel_z
	avg_x = float(total_x/len(pitch_subset))
	avg_z = float(total_z/len(pitch_subset))
	return avg_x, avg_z

# function returns the magnitude of the 2D vector comprised of the X and Z release point locations
def averageRelease2D(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	x = []
	z = []
	for pitch in pitch_subset:
		x.append(pitch.rel_x)
		z.append(pitch.rel_z)
	x = np.array(x)
	z = np.array(z)
	avg_x = x.mean()
	avg_z = z.mean()
	r2 = np.power(x,2) + np.power(z,2)
	r = np.sqrt(r2)
	r_avg = np.mean(r)
	return r_avg

# function returns the distance from the pitching rubber to home plate at which the pitch was release
def averageExtension(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	ext_array = []
	for pitch in pitch_subset:
		ext_array.append(pitch.rel_ext)
	ext_array = np.array(ext_array)
	return ext_array.mean()

# returns an array of the separation in average velocity of all possible comparisons for 5 different pitches (10 data points)
def pitchSeparation(pitch1, pitch2, pitch3, pitch4, pitch5):
	separation_list = []
	velocity_list = [pitch1, pitch2, pitch3, pitch4, pitch5]
	for i in range(len(velocity_list) - 1):
		for j in range((i+1),len(velocity_list)):
			separation_list.append(velocity_list[i]-velocity_list[j])
	return separation_list

# function returns the average horizontal and vertical break of a pitch subset
def averagePfx(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	total_x = 0
	total_z = 0
	for pitch in pitch_subset:
		total_x += pitch.pfx_x
		total_z += pitch.pfx_z
	avg_pfx_x = float(total_x/len(pitch_subset))
	avg_pfx_z = float(total_z/len(pitch_subset))
	return avg_pfx_x, avg_pfx_z

# function returns the statical standard deviation of the horizontal and vertical break of a pitch subset
def deviationPfx(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	x_array = []
	z_array = []
	for pitch in pitch_subset:
		x_array.append(pitch.pfx_x)
		z_array.append(pitch.pfx_z)
	x_array = np.array(x_array)
	z_array = np.array(z_array)
	pfxDev_x = np.std(x_array)
	pfxDev_z = np.std(z_array)
	return pfxDev_x, pfxDev_z

# function returns the statical standard deviation of the horizontal and vertical release location of a pitch subset
def releaseDeviation(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	x_array = []
	z_array = []
	for pitch in pitch_subset:
		x_array.append(pitch.rel_x)
		z_array.append(pitch.rel_z)
	x_array = np.array(x_array)
	z_array = np.array(z_array)
	stdev_x = np.std(x_array)
	stdev_z = np.std(z_array)
	return stdev_x, stdev_z

# function returns the statical standard deviation of the 2D release point vector of the pitch subset
def releaseDeviation2D(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	x_array = []
	z_array = []
	for pitch in pitch_subset:
		x_array.append(pitch.rel_x)
		z_array.append(pitch.rel_z)
	x_array = np.array(x_array)
	z_array = np.array(z_array)
	r2_array = np.power(x_array,2) + np.power(z_array,2)
	r_array = np.sqrt(r2_array)
	r_stdev = np.std(r_array)
	return r_stdev

# function returns the area of an elipse formed by 90% confidence intervals of the horizontal and vertical release location of a pitch subset
def releaseEllipse(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	N_pitches = len(pitch_subset)
	x_array = []
	z_array = []
	for pitch in pitch_subset:
		x_array.append(pitch.rel_x)
		z_array.append(pitch.rel_z)
	x_array = np.array(x_array)
	z_array = np.array(z_array)
	stdev_x = np.std(x_array)
	stdev_z = np.std(z_array)
	MEx = (stdev_x/np.sqrt(N_pitches)) * 1.96
	MEz = (stdev_z/np.sqrt(N_pitches)) * 1.96
	A = np.pi * MEx * MEz
	return A

# function returns the frequency which pitches in a subset were strikes. User has the option to count pitches with contact as strikes or not
def strikeFrequency(pitch_subset, contact_counts):
	if len(pitch_subset) == 0:
		return 0
	subset_total = len(pitch_subset)
	strike_count = 0
	ball_count = 0
	contact_count = 0
	for pitch in pitch_subset:
		if pitch.outcome == 'S':
			strike_count += 1
		elif pitch.outcome == 'B':
			ball_count += 1
		elif pitch.outcome == 'X':
			contact_count += 1
	if contact_counts == True:
		strike_freq = float((strike_count + contact_count) / subset_total)
	else:
		strike_freq = float(strike_count / subset_total)
	return strike_freq

# function returns and array of the proportion a pitch was located into each of 13 possible zones
def zoneDistribution(pitch_subset):
	zone_dist = np.zeros(14)
	N_TOTAL = 0
	for pitch in pitch_subset:
		if not pitch.zone == 0:
			i = pitch.zone - 1
			zone_dist[i] += 1
			N_TOTAL += 1
	zone_dist = zone_dist / N_TOTAL
	return zone_dist

def zoneStrikes(pitch_subset):
	ZS = 0
	N_TOTAL = 0
	for pitch in pitch_subset:
		if not pitch.zone == 0:
			N_TOTAL += 1
			if pitch.zone > 0 and pitch.zone < 10:
				ZS += 1
	ZS_PROP = float(ZS / N_TOTAL)
	return ZS_PROP

# function returns the proportion that the pitches in the pitch subset where in one of 5 vertical levels
def zoneLevels(pitch_subset):
	top_out = 0
	top = 0
	mid = 0
	bottom = 0
	bottom_out = 0
	N_TOTAL = 0
	for pitch in pitch_subset:
		if not pitch.zone == 0:
			N_TOTAL += 1
			if pitch.zone == 11 or pitch.zone == 12:
				top_out += 1
			elif pitch.zone > 0 and pitch.zone < 4:
				top += 1
			elif pitch.zone > 3 and pitch.zone < 7:
				mid += 1
			elif pitch.zone > 6 and pitch.zone < 10:
				bottom += 1
			elif pitch.zone == 13 or pitch.zone == 14:
				bottom_out += 1
	out_array = np.array([top_out, top, mid, bottom, bottom_out]) / N_TOTAL
	return out_array

# function returns the average velocity of pitches in the subset for each inning
# Second parameter determines the last inning calculated. For example: some pitchers may not have thrown in the 9th inning
def inningVelocity(pitch_subset, last_inning):
	inning_vel = np.zeros(last_inning)
	inning_count = np.zeros(last_inning)
	for pitch in pitch_subset:
		i = pitch.inning - 1
		if i < last_inning:
			vel = pitch.velocity
			inning_vel[i] += vel
			inning_count += 1
	inning_vel = inning_vel / inning_count
	return inning_vel

# function returns the average velocity change of pitches in the subset for each inning compared to the first inning
# Second parameter determines the last inning calculated. For example: some pitchers may not have thrown in the 9th inning
def inningVelocityChange(pitch_subset, last_inning):
	inning_vel = np.zeros(last_inning)
	inning_count = np.zeros(last_inning)
	for pitch in pitch_subset:
		i = pitch.inning - 1
		if i < last_inning:
			vel = pitch.velocity
			inning_vel[i] += vel
			inning_count += 1
	inning_vel = inning_vel / inning_count
	vel_change = (inning_vel - inning_vel[0]) / inning_vel[0]
	return vel_change

# function returns the release point change of pitches in the subset for each inning compared to the first inning
# Second parameter determines the last inning calculated. For example: some pitchers may not have thrown in the 9th inning
def inningReleaseChange(pitch_subset, last_inning):
	inning_rel = np.zeros(last_inning)
	inning_count = np.zeros(last_inning)
	for pitch in pitch_subset:
		i = pitch.inning - 1
		if i < last_inning:
			rel = pitch.rel_z
			inning_rel[i] += rel
			inning_count += 1
	inning_rel = inning_rel / inning_count
	rel_change = (inning_rel - inning_rel[0]) / inning_rel[0]
	return rel_change

# function that adds Pitcher objects to a provide list (second parameter) based on unique pitcher ID's provided from the csv data read
def makePitchers(filename, pitcher_list):
	curr_pitcher_ID = 9999 	# Current pitcher ID number
	pitcher_count = len(pitcher_list) - 1
	row_count = 0
	with open(filename, newline='') as file:
		reader = csv.reader(file)
		for row in reader:
			pitcher_ID = row[7]
			date = row[1]
			pitch_type = row[0]
			velocity = row[2]
			rel_x = row[3]
			rel_z = row[4]
			zone = row[14]
			pfx_x = row[27]
			pfx_z = row[28]
			outcome = row[21]
			spin_rate = row[56]
			rel_ext = row[57]
			inning = row[35]
			if pitcher_ID == curr_pitcher_ID:
				pitcher_list[pitcher_count].pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext, inning))
			else:
				pitcher_list.append(Pitcher(row[5]))
				curr_pitcher_ID = pitcher_ID
				pitcher_count += 1
				pitcher_list[pitcher_count].pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext, inning))






