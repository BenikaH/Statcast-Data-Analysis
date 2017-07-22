import numpy as np
import csv

def averageVelocity(pitch_subset, velocity):
	if len(pitch_subset) == 0:
		return 0
	total_vel = 0
	for pitch in pitch_subset:
		total_vel = total_vel + velocity[pitch]
	avg_vel = float(total_vel/len(pitch_subset))
	return avg_vel

def pitchFrequency(pitch_subset, N_TOTAL):
	freq = len(pitch_subset) / N_TOTAL
	return freq

def averageRelease(pitch_subset, x, z):
	if len(pitch_subset) == 0:
		return 0, 0
	total_x = 0
	total_z = 0
	for pitch in pitch_subset:
		total_x = total_x + x[pitch]
		total_z = total_z + z[pitch]
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

def velocityVariance(pitch_subset, velocity):
	vel_array = []
	for pitch in pitch_subset:
		vel_array.append(velocity[pitch])
	vel_array = np.array(vel_array)
	return vel_array.var()

def verifyResults(games,result_dates):
	if len(games) == len(result_dates):
		return True
	else:
		return False

class Game(object):
	def __init__(self, date):
		self.date = date
		self.game_pitches = []
		self.game_fastball = []
		self.game_curveball = []
		self.game_cutter = []
		self.game_sinker = []
		self.game_change = []
		self.game_non_classified = []

		self.game_vel_FF = 0
		self.game_vel_CU = 0
		self.game_vel_FC = 0
		self.game_vel_SI = 0
		self.game_vel_CH = 0

		self.game_freq_FF = 0
		self.game_freq_CU = 0
		self.game_freq_FC = 0
		self.game_freq_SI = 0
		self.game_freq_CH = 0

		self.game_relx_FF = 0
		self.game_relx_CU = 0
		self.game_relx_FC = 0
		self.game_relx_SI = 0
		self.game_relx_CH = 0

		self.game_relz_FF = 0
		self.game_relz_CU = 0
		self.game_relz_FC = 0
		self.game_relz_SI = 0
		self.game_relz_CH = 0

		self.game_vel_separation = []

	def calcMetrics(self, velocity, rel_x, rel_z):

		self.game_vel_FF = averageVelocity(self.game_fastball, velocity)
		self.game_vel_CU = averageVelocity(self.game_curveball, velocity)
		self.game_vel_FC = averageVelocity(self.game_cutter, velocity)
		self.game_vel_SI = averageVelocity(self.game_sinker, velocity)
		self.game_vel_CH = averageVelocity(self.game_change, velocity)

		self.game_freq_FF = pitchFrequency(self.game_fastball, len(self.game_pitches))
		self.game_freq_CU = pitchFrequency(self.game_curveball, len(self.game_pitches))
		self.game_freq_FC = pitchFrequency(self.game_cutter, len(self.game_pitches))
		self.game_freq_SI = pitchFrequency(self.game_sinker, len(self.game_pitches))
		self.game_freq_CH = pitchFrequency(self.game_change, len(self.game_pitches))

		self.game_relx_FF, self.game_relz_FF = averageRelease(self.game_fastball, rel_x, rel_z)
		self.game_relx_CU, self.game_relz_CU = averageRelease(self.game_curveball, rel_x, rel_z)
		self.game_relx_FC, self.game_relz_FC = averageRelease(self.game_cutter, rel_x, rel_z)
		self.game_relx_SI, self.game_relz_SI = averageRelease(self.game_sinker, rel_x, rel_z)
		self.game_relx_CH, self.game_relz_CH = averageRelease(self.game_change, rel_x, rel_z)

		self.game_vel_separation = pitchSeparation(self.game_vel_FF, self.game_vel_CU, self.game_vel_FC, self.game_vel_SI, self.game_vel_CH)


	def sortPitches(self, pitch_type):
		for i in self.game_pitches:
			if pitch_type[i] == 'FF':
				self.game_fastball.append(i)
			elif pitch_type[i] == 'CU':
				self.game_curveball.append(i)
			elif pitch_type[i] == 'FC':
				self.game_cutter.append(i)
			elif pitch_type[i] == 'SI':
				self.game_sinker.append(i)
			elif pitch_type[i] == 'CH':
				self.game_change.append(i)
			else:
				self.game_non_classified.append(i)



def makeGames(pitch_dates):
	game = 0
	current_day = pitch_dates[game]
	pitcher_games = []
	pitcher_games.append(Game(current_day))
	for i in range(len(pitch_dates)):
		if pitch_dates[i] == current_day:
			pitcher_games[game].game_pitches.append(i)
		else:
			game = game + 1
			current_day = pitch_dates[i]
			pitcher_games.append(Game(current_day))
			pitcher_games[game].game_pitches.append(i)
	return pitcher_games





pitch_type = []
date = []
velocity = []
rel_x = []
rel_z = []

result_date = np.loadtxt('wainwright_game_summary.csv', delimiter=',',usecols = (0,), unpack = True)
result_era = np.loadtxt('wainwright_game_summary.csv', delimiter=',',usecols = (5,), unpack = True)

with open('wainwright_2017_processed.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        pitch_type.append(row[0])
        date.append(row[1])
        velocity.append(row[2])
        rel_x.append(row[3])
        rel_z.append(row[4])

N_TOTAL = len(pitch_type)

fastball = [] # FF
curveball = [] # CU
cutter = [] # FC
sinker = [] # SI
change = [] # CH
non_classified = []

for i in range(len(velocity)):
	if pitch_type[i] == 'FF':
		fastball.append(i)
	elif pitch_type[i] == 'CU':
		curveball.append(i)
	elif pitch_type[i] == 'FC':
		cutter.append(i)
	elif pitch_type[i] == 'SI':
		sinker.append(i)
	elif pitch_type[i] == 'CH':
		change.append(i)
	else:
		non_classified.append(i)

print('Non Classified')
print(non_classified)

for i in non_classified:
	velocity[i] = 0
	rel_x[i] = 0
	rel_z[i] = 0

print(velocity[610])

for i in range(len(velocity)):
	print(i)
	velocity[i] = float(velocity[i])
	rel_x[i] = float(rel_x[i])
	rel_z[i] = float(rel_z[i])

velocity = np.array(velocity)
rel_x = np.array(rel_x)
rel_z = np.array(rel_z)

print('Fastballs')
print(fastball)
print('Curveballs')
print(curveball)
print('Cutters')
print(cutter)
print('Change-ups')
print(change)
print('Non Classified')
print(non_classified)

avg_vel_FF = averageVelocity(fastball,velocity)
avg_vel_CU = averageVelocity(curveball,velocity)
avg_vel_FC = averageVelocity(cutter,velocity)
avg_vel_SI = averageVelocity(sinker,velocity)
avg_vel_CH = averageVelocity(change,velocity)

print('Average Fastball Velocity')
print(avg_vel_FF)
print('Average Curveball Velocity')
print(avg_vel_CU)
print('Average Cutter Velocity')
print(avg_vel_FC)
print('Average Sinker Velocity')
print(avg_vel_SI)
print('Average Change Velocity')
print(avg_vel_CH)

avg_freq_FF = pitchFrequency(fastball, N_TOTAL)
avg_freq_CU = pitchFrequency(curveball, N_TOTAL)
avg_freq_FC = pitchFrequency(cutter, N_TOTAL)
avg_freq_SI = pitchFrequency(sinker, N_TOTAL)
avg_freq_CH = pitchFrequency(change, N_TOTAL)

print('Average Fastball Frequency')
print(avg_freq_FF)
print('Average Curveball Frequency')
print(avg_freq_CU)
print('Average Cutter Frequency')
print(avg_freq_FC)
print('Average Sinker Frequency')
print(avg_freq_SI)
print('Average Change Frequency')
print(avg_freq_CH)


avg_velvar_FF = velocityVariance(fastball,velocity)
avg_velvar_CU = velocityVariance(curveball,velocity)
avg_velvar_FC = velocityVariance(cutter,velocity)
avg_velvar_SI = velocityVariance(sinker,velocity)
avg_velvar_CH = velocityVariance(change,velocity)

print('Average Fastball Velocity Var')
print(avg_velvar_FF)
print('Average Curveball Velocity Var')
print(avg_velvar_CU)
print('Average Cutter Velocity Var')
print(avg_velvar_FC)
print('Average Sinker Velocity Var')
print(avg_velvar_SI)
print('Average Change Velocity Var')
print(avg_velvar_CH)

avg_relx_FF, avg_relz_FF = averageRelease(fastball,rel_x,rel_z)
avg_relx_CU, avg_relz_CU = averageRelease(curveball,rel_x,rel_z)
avg_relx_FC, avg_relz_FC = averageRelease(cutter,rel_x,rel_z)
avg_relx_SI, avg_relz_SI = averageRelease(sinker,rel_x,rel_z)
avg_relx_CH, avg_relz_CH = averageRelease(change,rel_x,rel_z)

avg_vel_separation = pitchSeparation(avg_vel_FF ,avg_vel_CU, avg_vel_FC, avg_vel_SI, avg_vel_CH)

for sep in avg_vel_separation:
	print(sep)

print(len(change))

wainright_games = makeGames(date)


for i in range(len(wainright_games)):
	wainright_games[i].sortPitches(pitch_type)
	wainright_games[i].calcMetrics(velocity, rel_x, rel_z)

print(result_date)
print(result_era)

print(verifyResults(wainright_games,result_date))
#for i in range(len(wainright_games)):
	#print(wainright_games[i].game_vel_FC)
