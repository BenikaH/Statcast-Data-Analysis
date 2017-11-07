# Pitcher Class
import numpy as np
import csv
from pitch import *
from game import *
from pitching_data_functions import *

# Creates a Pitcher object
# Stores all the pitches thrown by the pitcher and all games the pitcher appeared in
class Pitcher(object):
	def __init__(self, name):
		self.name = name
		self.game_list = []

		self.pitch_list = []
		self.FF = []
		self.FT = []
		self.FC = []
		self.SI = []
		self.SL = []
		self.CH = []
		self.CU = []
		self.KC = []
		self.KN = []
		self.NC = []
		self.all_pitches = []

		self.all_fastballs = []
		self.all_offspeed = []
		self.type_other = []
		self.pitch_type_list = [self.FF, self.FT, self.FC, self.SI, self.SL, self.CH, self.CU, self.KC, self.KN, self.NC]
		self.pitch_type_names = ['FF','FT','FC','SI','SL','CH','CU','KC','KN','NC']
		self.pitch_class_list = [self.all_fastballs, self.all_offspeed, self.type_other]
		self.pitch_class_name = ['Fastballs','Offspeed','Other']

		# Arrays for date of game results, game era, and quality starts
		self.result_dates = []
		self.result_eras = []
		self.quality_start = []

	# method to read line by line from a csv to create pitch objects for each statcast pitch entry and append to the pitcher's pitch list
	def importPitches(self, filename):
		with open(filename, newline='') as file:
			reader = csv.reader(file)
			for row in reader:
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
				self.pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext, inning))

	def calcMetrics():
		pass

	# from the pitcher's pitch_list, make Game objects based on groupings of pitches with the same date
	def makeGames(self):
		game = 0
		current_day = self.pitch_list[0].pitch_date
		self.game_list.append(Game(current_day))
		for i in range(len(self.pitch_list)):
			if self.pitch_list[i].pitch_date == current_day:
				self.game_list[game].game_pitches.append(self.pitch_list[i])
			else:
				game += 1
				current_day = self.pitch_list[i].pitch_date
				self.game_list.append(Game(current_day))
				self.game_list[game].game_pitches.append(self.pitch_list[i])

	# sort all of the pitches the pitcher has thrown into the type of pitch that was thrown
	def sortPitches(self):
		for pitch in self.pitch_list:
			if pitch.pitch_type == 'FF':
				self.FF.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'FT':
				self.FT.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'FC':
				self.FC.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'SI':
				self.SI.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'SL':
				self.SL.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'CH':
				self.CH.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB':
				self.CU.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'KC':
				self.KC.append(pitch)
				self.all_pitches.append(pitch)
			elif pitch.pitch_type == 'KN':
				self.KN.append(pitch)
				self.all_pitches.append(pitch)
			else:
				self.NC.append(pitch)

	# returns an array with the proportions of each pitch type thrown. Order of the array is based on the pitch_type_list
	def pitchProportion(self):
		N_TOTAL = len(self.FF) + len(self.FT) + len(self.FC) + len(self.SI) + len(self.SL) + len(self.CH) + \
		len(self.CU) + len(self.KC) + len(self.KN)
		pitch_type_prop = np.zeros(len(self.pitch_type_list) - 1)
		for i in range(len(self.pitch_type_list) - 1):
			if len(self.pitch_type_list[i]) > 10:
				pitch_type_prop[i] = len(self.pitch_type_list[i]) / N_TOTAL
			else:
				pitch_type_prop[i] = 0
		return pitch_type_prop

	# method to determine the average pitch data for a pitcher's primary offspeed pitch
	# the "primary" offspeed is determined as the offspeed pitch type thrown the greatest number of times
	def primary_offspeed(self):
		N_SL = len(self.SL)
		N_CH = len(self.CH)
		N_CU = len(self.CU)
		N_KC = len(self.KC)
		if N_SL >= N_CH and N_SL >= N_CU and N_SL >= N_KC:
			offspeed_vel = averageVelocity(self.SL)
			offspeed_pfx_x, offspeed_pfx_z = averageRelease(self.SL)
			offspeed_spin = averageSpin(self.SL)
		elif N_CH >= N_SL and N_CH >= N_CU and N_CH >= N_KC:
			offspeed_vel = averageVelocity(self.CH)
			offspeed_pfx_x, offspeed_pfx_z = averageRelease(self.CH)
			offspeed_spin = averageSpin(self.CH)
		elif N_CU >= N_SL and N_CU >= N_CH and N_CU >= N_KC:
			offspeed_vel = averageVelocity(self.CU)
			offspeed_pfx_x, offspeed_pfx_z = averageRelease(self.CU)
			offspeed_spin = averageSpin(self.CU)
		elif N_KC >= N_SL and N_KC >= N_CU and N_KC >= N_CH:
			offspeed_vel = averageVelocity(self.KC)
			offspeed_pfx_x, offspeed_pfx_z = averageRelease(self.KC)
			offspeed_spin = averageSpin(self.KC)
		return offspeed_vel, offspeed_pfx_x, offspeed_pfx_z, offspeed_spin				

	# method to return the number of different pitch types a pitcher throws
	def pitchesThrown(self):
		diff_pitches = 0
		for i in range(len(self.pitch_type_list)-1):
			if len(self.pitch_type_list[i]) > 0:
				diff_pitches += 1
		return diff_pitches

	# method that reads the game results for a pitcher from a csv file.
	def addGameResults(self, filename):
		self.result_dates = np.loadtxt(filename, delimiter=',',usecols = (0,), unpack = True)
		self.result_eras = np.loadtxt(filename, delimiter=',',usecols = (5,), unpack = True)
		self.quality_start = np.loadtxt(filename, delimiter=',',usecols = (6,), unpack = True)

	# method to classify all of the pitcher's pitches as either fastball or offspeed
	def classifyPitches(self):
		for pitch in self.pitch_list:
			if pitch.pitch_type == 'FF' or pitch.pitch_type == 'FA' or pitch.pitch_type == 'FT' or pitch.pitch_type == 'FC' or pitch.pitch_type == 'FS' or pitch.pitch_type == 'SI' or pitch.pitch_type == 'SF':
				self.all_fastballs.append(pitch)
			elif pitch.pitch_type == 'SL' or pitch.pitch_type == 'CH' or pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB' or pitch.pitch_type == 'KC' or pitch.pitch_type == 'KN' or pitch.pitch_type == 'EP':
				self.all_offspeed.append(pitch)
			else:
				self.type_other.append(pitch)

	# method that returns metrics on classified fastball/offspeed pitches
	def classifyMetrics(self):
		self.number_fastballs = len(self.all_fastballs)
		self.number_offspeed = len(self.all_offspeed)

		#self.avg_fastball_vel = averageVelocity(self.all_fastballs)
		self.fastball_freq = float(self.number_fastballs/(self.number_fastballs + self.number_offspeed))

	# pipeline to classify pitches as fastball/offspeed and cumpute metrics
	def runClassifyPipeline(self):
		self.classifyPitches()
		self.classifyMetrics()

# Note moved to pitching data functions file
'''
def averageVelocity(pitch_subset):
	if len(pitch_subset) == 0:
		return 0
	total_vel = 0
	for pitch in pitch_subset:
		total_vel += pitch.velocity
	avg_vel = float(total_vel/len(pitch_subset))
	return avg_vel

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
'''