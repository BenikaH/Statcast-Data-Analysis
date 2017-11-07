# Game object class
import numpy as np
from pitch import *
from pitching_data_functions import *

# Creates a Game object
# Object stores all pitches from an entire game as well as these pitches stored into sorted classes based on pitch type
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

	# Currently no metrics are calculated at the Game level within the class
	def calcMetrics(self):
		pass

	# method to sort the pitches from "pitch_list" into additional lists based on the pitch type
	# pitches are not removed from the total pitch list when sorted
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

	# method to classify pitches into fastball or offspeed catagories
	def classifyPitches(self):
		for pitch in self.pitch_list:
			if pitch.pitch_type == 'FF' or pitch.pitch_type == 'FA' or pitch.pitch_type == 'FT' or pitch.pitch_type == 'FC' or pitch.pitch_type == 'FS' or pitch.pitch_type == 'SI' or pitch.pitch_type == 'SF':
				self.all_fastballs.append(pitch)
			elif pitch.pitch_type == 'SL' or pitch.pitch_type == 'CH' or pitch.pitch_type == 'CU' or pitch.pitch_type == 'CB' or pitch.pitch_type == 'KC' or pitch.pitch_type == 'KN' or pitch.pitch_type == 'EP':
				self.all_offspeed.append(pitch)
			else:
				self.type_other.append(pitch)

	# method to calculate the workload on the pitcher based on the stress of each pitch type on the elbow
	# the "weights" of each pitch type are taken from published pitching research
	def calcWorkload(self):
		wFA = 1 # load weight for fastball
		wCU = .963 # load weight for curveball
		wCH = .866 # load weight for change-up
		wSL = .988 # load weight for slider
		numFA = len(self.all_fastballs)
		numCU = len(self.CU)
		numCH = len(self.CH)
		numSL = len(self.SL)
		self.workload = (numFA * wFA) + (numCU * wCU) + (numCH * wCH) + (numSL * wSL)

	# output for the entire Game data object is not currently supported
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
