# Functions to support the statcast data analysis
import numpy as np

def averageVelocity(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	total_vel = 0
	for pitch in pitch_subset:
		total_vel += pitch.velocity
	avg_vel = float(total_vel/len(pitch_subset))
	return avg_vel

def pitchFrequency(pitch_subset, N_TOTAL):
	freq = len(pitch_subset) / N_TOTAL
	return freq

def velocityVariance(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	vel_array = []
	for pitch in pitch_subset:
		vel_array.append(pitch.velocity)
	vel_array = np.array(vel_array)
	return vel_array.var()

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

def strikeFrequency(pitch_subset):
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
	strike_freq = float(strike_count / subset_total)
	return strike_freq




