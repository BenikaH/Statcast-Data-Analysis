# Pitcher Class
import numpy as np
import csv
from pitch import *
from game import *
from pitching_data_functions import *

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
				self.pitch_list.append(Pitch(date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext))

	def calcMetrics():
		pass

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
				self.FF.append(pitch)
			elif pitch.pitch_type == 'FT':
				self.FT.append(pitch)
			elif pitch.pitch_type == 'FC':
				self.FC.append(pitch)
			elif pitch.pitch_type == 'SI':
				self.SI.append(pitch)
			elif pitch.pitch_type == 'SL':
				self.SL.append(pitch)
			elif pitch.pitch_type == 'CH':
				self.CH.append(pitch)
			elif pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB':
				self.CU.append(pitch)
			elif pitch.pitch_type == 'KC':
				self.KC.append(pitch)
			elif pitch.pitch_type == 'KN':
				self.KN.append(pitch)
			else:
				self.NC.append(pitch)

	def pitchesThrown(self):
		diff_pitches = 0
		for i in range(len(self.pitch_type_list)-1):
			if len(self.pitch_type_list[i]) > 0:
				diff_pitches += 1
		return diff_pitches


	def addGameResults(self, filename):
		self.result_dates = np.loadtxt(filename, delimiter=',',usecols = (0,), unpack = True)
		self.result_eras = np.loadtxt(filename, delimiter=',',usecols = (5,), unpack = True)
		self.quality_start = np.loadtxt(filename, delimiter=',',usecols = (6,), unpack = True)

	def classifyPitches(self):
		for pitch in self.pitch_list:
			if pitch.pitch_type == 'FF' or pitch.pitch_type == 'FA' or pitch.pitch_type == 'FT' or pitch.pitch_type == 'FC' or pitch.pitch_type == 'FS' or pitch.pitch_type == 'SI' or pitch.pitch_type == 'SF':
				self.all_fastballs.append(pitch)
			elif pitch.pitch_type == 'SL' or pitch.pitch_type == 'CH' or pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB' or pitch.pitch_type == 'KC' or pitch.pitch_type == 'KN' or pitch.pitch_type == 'EP':
				self.all_offspeed.append(pitch)
			else:
				self.type_other.append(pitch)

	def classifyMetrics(self):
		self.number_fastballs = len(self.all_fastballs)
		self.number_offspeed = len(self.all_offspeed)

		#self.avg_fastball_vel = averageVelocity(self.all_fastballs)
		self.fastball_freq = float(self.number_fastballs/(self.number_fastballs + self.number_offspeed))

	def runClassifyPipeline(self):
		self.classifyPitches()
		self.classifyMetrics()


