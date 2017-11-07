# Pitch object class
import numpy as np
#from pitching_data_functions import *

# Create Pitch object
# Stores data for a single pitch
class Pitch(object):
	def __init__(self, date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z, outcome, spin_rate, rel_ext, inning):
		self.pitch_date = parseDate(date)
		self.pitch_type = pitch_type
		# Check to make sure the data is good and none of the data fields are missing
		if velocity.isalpha() or rel_x.isalpha() or rel_z.isalpha() or zone.isalpha() or pfx_x.isalpha() or pfx_z.isalpha() or spin_rate.isalpha() or rel_ext.isalpha():
			self.pitch_type = 'null'
			self.velocity = 0
			self.rel_x = 0
			self.rel_z = 0
			self.zone = 0
			self.pfx_x = 0
			self.pfx_z = 0
			self.spin_rate = 0
			self.rel_ext = 0
			self.inning = 0
		else:
			self.velocity = float(velocity) # pitch velocity
			self.rel_x = float(rel_x) # horizontal release location
			self.rel_z = float(rel_z) # vertical release location
			self.zone = int(zone) # one of 13 potential zones the pitch was located
			self.pfx_x = float(pfx_x) # horizontal pitch break
			self.pfx_z = float(pfx_z) # vertical pitch break
			self.outcome = outcome # the outcome of the pitch
			self.spin_rate = float(spin_rate) # spin rate of the pitch
			self.rel_ext = float(rel_ext) # distance from the pitching rubber to release location
			self.inning = int(inning) # inning the pitch occurred

	# method to return an array of the data from the pitch
	def getData(self):
		output = np.array([self.pitch_date, self.pitch_type, self.velocity, self.rel_x, self.rel_z, self.zone, self.pfx_x, self.pfx_z, self.outcome, self.spin_rate, self.rel_ext, self.inning])
		return output

# function (outside of the class) used to parse dates given in mm/dd/yy format into yymmdd format
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
