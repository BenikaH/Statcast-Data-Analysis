# Pitcher Class
import numpy as np
import csv
from pitch import *
from game import *
from pitching_data_functions import *

class Pitcher(object):
	def __init__(self, name, filename):
		self.name = name
		self.game_list = []
		self.pitch_list = []
		self.all_fastballs = []
		self.all_curveballs = []
		self.all_cutters = []
		self.all_sinkers = []
		self.all_changes = []
		self.all_non_classified = []

		self.importPitches(filename)
		self.sortPitches()

		self.total_pitches = len(self.pitch_list)
		# Average velocity for each pitch type
		self.avg_vel_FF = averageVelocity(self.all_fastballs)
		self.avg_vel_CU = averageVelocity(self.all_curveballs)
		self.avg_vel_FC = averageVelocity(self.all_cutters)
		self.avg_vel_SI = averageVelocity(self.all_sinkers)
		self.avg_vel_CH = averageVelocity(self.all_changes)
		# Average freqency each pitch type is thrown
		self.avg_freq_FF = pitchFrequency(self.all_fastballs, self.total_pitches)
		self.avg_freq_CU = pitchFrequency(self.all_curveballs, self.total_pitches)
		self.avg_freq_FC = pitchFrequency(self.all_cutters, self.total_pitches)
		self.avg_freq_SI = pitchFrequency(self.all_sinkers, self.total_pitches)
		self.avg_freq_CH = pitchFrequency(self.all_changes, self.total_pitches)
		# Average variance in velocity for each pitch type
		self.avg_velvar_FF = velocityVariance(self.all_fastballs)
		self.avg_velvar_CU = velocityVariance(self.all_curveballs)
		self.avg_velvar_FC = velocityVariance(self.all_cutters)
		self.avg_velvar_SI = velocityVariance(self.all_sinkers)
		self.avg_velvar_CH = velocityVariance(self.all_changes)
		# Average release point for each pitch
		self.avg_relx_FF, self.avg_relz_FF = averageRelease(self.all_fastballs)
		self.avg_relx_CU, self.avg_relz_CU = averageRelease(self.all_curveballs)
		self.avg_relx_FC, self.avg_relz_FC = averageRelease(self.all_cutters)
		self.avg_relx_SI, self.avg_relz_SI = averageRelease(self.all_sinkers)
		self.avg_relx_CH, self.avg_relz_CH = averageRelease(self.all_changes)
		# Average pfx for each pitch
		self.avg_pfx_x_FF, self.avg_pfx_z_FF = averagePfx(self.all_fastballs)
		self.avg_pfx_x_CU, self.avg_pfx_z_CU = averagePfx(self.all_curveballs)
		self.avg_pfx_x_FC, self.avg_pfx_z_FC = averagePfx(self.all_cutters)
		self.avg_pfx_x_SI, self.avg_pfx_z_SI = averagePfx(self.all_sinkers)
		self.avg_pfx_x_CH, self.avg_pfx_z_CH = averagePfx(self.all_changes)
		# List of average velocity separations between pitches
		self.avg_vel_separation = pitchSeparation(self.avg_vel_FF ,self.avg_vel_CU, self.avg_vel_FC, self.avg_vel_SI, self.avg_vel_CH)
		# Arrays for date of game results, game era, and quality starts
		self.result_dates = []
		self.result_eras = []
		self.quality_start = []

		self.fastball_pitches = []
		self.offspeed_pitches = []
		self.type_other = []

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
		    	self.pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome))

	def calcMetrics():
		pass
		# As of right now, metrics are automatically calculated on initiation

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

	def sortPitches(self):
		for pitch in self.pitch_list:
			if pitch.pitch_type == 'FF':
				self.all_fastballs.append(pitch)
			elif pitch.pitch_type == 'CU':
				self.all_curveballs.append(pitch)
			elif pitch.pitch_type == 'FC':
				self.all_cutters.append(pitch)
			elif pitch.pitch_type == 'SI':
				self.all_sinkers.append(pitch)
			elif pitch.pitch_type == 'CH':
				self.all_changes.append(pitch)
			else:
				self.all_non_classified.append(pitch)

	def addGameResults(self, filename):
		self.result_dates = np.loadtxt(filename, delimiter=',',usecols = (0,), unpack = True)
		self.result_eras = np.loadtxt(filename, delimiter=',',usecols = (5,), unpack = True)
		self.quality_start = np.loadtxt(filename, delimiter=',',usecols = (6,), unpack = True)

	def classifyPitches(self):
		for pitch in self.pitch_list:
			if pitch.pitch_type == 'FF' or pitch.pitch_type == 'FA' or pitch.pitch_type == 'FT' or pitch.pitch_type == 'FC' or pitch.pitch_type == 'FS' or pitch.pitch_type == 'SI' or pitch.pitch_type == 'SF':
				self.fastball_pitches.append(pitch)
			elif pitch.pitch_type == 'SL' or pitch.pitch_type == 'CH' or pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB' or pitch.pitch_type == 'KC' or pitch.pitch_type == 'KN' or pitch.pitch_type == 'EP':
				self.offspeed_pitches.append(pitch)
			else:
				self.type_other.append(pitch)

	def classifyMetrics(self):
		self.number_fastballs = len(self.fastball_pitches)
		self.number_offspeed = len(self.offspeed_pitches)

		self.avg_fastball_vel = averageVelocity(self.fastball_pitches)
		self.fastball_freq = float(self.number_fastballs/(self.number_fastballs + self.number_offspeed))

	def runClassifyPipeline(self):
		self.classifyPitches()
		self.classifyMetrics()


