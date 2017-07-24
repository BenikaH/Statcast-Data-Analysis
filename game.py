# Game object class
import numpy as np
from pitch import *
from pitching_data_functions import *

class Game(object):
	def __init__(self, date):
		self.date = date
		self.game_pitches = []
		self.game_fastballs = []
		self.game_curveballs = []
		self.game_cutters = []
		self.game_sinkers = []
		self.game_changes = []
		self.game_non_classified = []

		self.pitch_count = 0

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

	def calcMetrics(self):
		self.pitch_count = len(self.game_pitches)

		self.game_vel_FF = averageVelocity(self.game_fastballs)
		self.game_vel_CU = averageVelocity(self.game_curveballs)
		self.game_vel_FC = averageVelocity(self.game_cutters)
		self.game_vel_SI = averageVelocity(self.game_sinkers)
		self.game_vel_CH = averageVelocity(self.game_changes)

		self.game_freq_FF = pitchFrequency(self.game_fastballs, self.pitch_count)
		self.game_freq_CU = pitchFrequency(self.game_curveballs, self.pitch_count)
		self.game_freq_FC = pitchFrequency(self.game_cutters, self.pitch_count)
		self.game_freq_SI = pitchFrequency(self.game_sinkers, self.pitch_count)
		self.game_freq_CH = pitchFrequency(self.game_changes, self.pitch_count)

		self.game_relx_FF, self.game_relz_FF = averageRelease(self.game_fastballs)
		self.game_relx_CU, self.game_relz_CU = averageRelease(self.game_curveballs)
		self.game_relx_FC, self.game_relz_FC = averageRelease(self.game_cutters)
		self.game_relx_SI, self.game_relz_SI = averageRelease(self.game_sinkers)
		self.game_relx_CH, self.game_relz_CH = averageRelease(self.game_changes)

		self.game_velvar_FF = velocityVariance(self.game_fastballs)
		self.game_velvar_CU = velocityVariance(self.game_curveballs)
		self.game_velvar_FC = velocityVariance(self.game_cutters)
		self.game_velvar_SI = velocityVariance(self.game_sinkers)
		self.game_velvar_CH = velocityVariance(self.game_changes)

		self.game_vel_separation = pitchSeparation(self.game_vel_FF, self.game_vel_CU, self.game_vel_FC, self.game_vel_SI, self.game_vel_CH)

	def sortPitches(self):
		for pitch in self.game_pitches:
			if pitch.pitch_type == 'FF':
				self.game_fastballs.append(pitch)
			elif pitch.pitch_type == 'CU':
				self.game_curveballs.append(pitch)
			elif pitch.pitch_type == 'FC':
				self.game_cutters.append(pitch)
			elif pitch.pitch_type == 'SI':
				self.game_sinkers.append(pitch)
			elif pitch.pitch_type == 'CH':
				self.game_changes.append(pitch)
			else:
				self.game_non_classified.append(pitch)

	def outputData(self):
		output_row = np.array([self.game_vel_FF, self.game_vel_CU, self.game_vel_FC, self.game_vel_SI, self.game_vel_CH, \
		self.game_freq_FF, self.game_freq_CU, self.game_freq_FC, self.game_freq_SI, self.game_freq_CH, \
		self.game_relx_FF, self.game_relx_CU, self.game_relx_FC, self.game_relx_SI, self.game_relx_CH, \
		self.game_relz_FF, self.game_relz_CU, self.game_relz_FC, self.game_relz_SI, self.game_relz_CH, \
		self.game_velvar_FF, self.game_velvar_CU, self.game_velvar_FC, self.game_velvar_SI, self.game_velvar_CH, \
		self.game_vel_separation[0], self.game_vel_separation[1], self.game_vel_separation[2], self.game_vel_separation[3], \
		self.game_vel_separation[4], self.game_vel_separation[5], self.game_vel_separation[6], self.game_vel_separation[7], \
		self.game_vel_separation[8], self.game_vel_separation[9]])
		return output_row

	def runPipeline(self):
		self.sortPitches()
		self.calcMetrics()

