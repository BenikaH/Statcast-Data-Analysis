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

def releaseDeviation(pitch_subset):
	if len(pitch_subset) == 0:
		return 0, 0
	x_array = []
	z_array = []
	for pitch in pitch_subset:
		x_array.append(pitch.pfx_x)
		z_array.append(pitch.pfx_z)
	x_array = np.array(x_array)
	z_array = np.array(z_array)
	stdev_x = np.std(x_array)
	stdev_z = np.std(z_array)
	return stdev_x, stdev_z


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

def parseDate(date):
	i = 0
	while i < len(date):
		if date[i] == '/':
			slash1 = i
			break
		i += 1
	i += 1

	while i < len(date):
		if date[i] == '/':
			slash2 = i
			break
		i += 1
	mm = date[0:slash1]
	dd = date[slash1+1:slash2]
	yy = date[slash2+1:len(date)]

	new_date = yy
	if len(mm) == 1:
		new_date += '0'
		new_date += mm
	else:
		new_date += mm

	if len(dd) == 1:
		new_date += '0'
		new_date += dd
	else:
		new_date += dd

	new_date = int(new_date)
	return new_date




