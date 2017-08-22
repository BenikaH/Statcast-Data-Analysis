# Game object class
import numpy as np
from pitch import *
from pitching_data_functions import *

class Game(object):
	def __init__(self, date):
		self.date = date

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

		self.pitch_count = 0


	def calcMetrics(self):
		pass

	def classifyMetrics(self):
		pass

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

	def classifyPitches(self):
		for pitch in self.game_pitches:
			if pitch.pitch_type == 'FF' or pitch.pitch_type == 'FA' or pitch.pitch_type == 'FT' or pitch.pitch_type == 'FC' or pitch.pitch_type == 'FS' or pitch.pitch_type == 'SI' or pitch.pitch_type == 'SF':
				self.all_fastballs.append(pitch)
			elif pitch.pitch_type == 'SL' or pitch.pitch_type == 'CH' or pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB' or pitch.pitch_type == 'KC' or pitch.pitch_type == 'KN' or pitch.pitch_type == 'EP':
				self.all_offspeed.append(pitch)
			else:
				self.type_other.append(pitch)

	def calcWorkload(self):
		wFA = 1
		wCU = .963
		wCH = .866
		wSL = .988
		numFA = len(self.all_fastballs)
		numCU = len(self.CU)
		numCH = len(self.CH)
		numSL = len(self.SL)
		self.workload = (numFA * wFA) + (numCU * wCU) + (numCH * wCH) + (numSL * wSL)

	def outputData(self):
		pass

	def runMainPipeline(self):
		self.sortPitches()
		self.calcMetrics()

	def runClassifyPipeline(self):
		self.classifyPitches()
		self.classifyMetrics()

	def runWorkloadPipeline(self):
		self.sortPitches()
		self.calcWorkload()
