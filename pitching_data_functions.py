# Functions to support the statcast data analysis
import numpy as np
import csv
from pitch import *
from game import *
from pitcher import *

def averageVelocity(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	total_vel = 0
	for pitch in pitch_subset:
		total_vel += pitch.velocity
	avg_vel = float(total_vel/len(pitch_subset))
	return avg_vel

def pitchFrequency(pitch_subset, all_pitches):
	N_TOTAL = len(all_pitches)
	N_TYPE = len(pitch_subset)
	freq = N_TYPE / N_TOTAL
	return freq

def velocityVariance(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	vel_array = []
	for pitch in pitch_subset:
		vel_array.append(pitch.velocity)
	vel_array = np.array(vel_array)
	return vel_array.var()

def velocitySTDev(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	vel_array = []
	for pitch in pitch_subset:
		vel_array.append(pitch.velocity)
	vel_array = np.array(vel_array)
	return vel_array.std()	

def averageSpin(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	spin_array = []
	for pitch in pitch_subset:
		spin_array.append(pitch.spin_rate)
	spin_array = np.array(spin_array)
	return spin_array.mean()

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

def averageExtension(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	ext_array = []
	for pitch in pitch_subset:
		ext_array.append(pitch.rel_ext)
	ext_array = np.array(ext_array)
	return ext_array.mean()

def pitchSeparation(pitch1, pitch2, pitch3, pitch4, pitch5):
	separation_list = []
	velocity_list = [pitch1, pitch2, pitch3, pitch4, pitch5]
	for i in range(len(velocity_list) - 1):
		for j in range((i+1),len(velocity_list)):
			separation_list.append(velocity_list[i]-velocity_list[j])
	return separation_list

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
			if pitcher_ID == curr_pitcher_ID:
				pitcher_list[pitcher_count].pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext))
			else:
				pitcher_list.append(Pitcher(row[5]))
				curr_pitcher_ID = pitcher_ID
				pitcher_count += 1
				pitcher_list[pitcher_count].pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext))






