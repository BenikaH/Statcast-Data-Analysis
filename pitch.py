# Pitch object class
import numpy as np

class Pitch(object):
	def __init__(self, date, pitch_type, velocity, rel_x, rel_z, zone, pfx_x, pfx_z):
		self.pitch_date = date
		self.pitch_type = pitch_type
		if velocity.isalpha():
			self.velocity = 0
		else:
			self.velocity = float(velocity)

		if rel_x.isalpha():
			self.rel_x = 0
		else:
			self.rel_x = float(rel_x)
		
		if rel_z.isalpha():
			self.rel_z = 0
		else:
			self.rel_z = float(rel_z)

		if zone.isalpha():
			self.zone = 0
		else:
			self.zone = int(zone)

		if pfx_x.isalpha():
			self.pfx_x = 0
		else:
			self.pfx_x = float(pfx_x)

		if pfx_z.isalpha():
			self.pfx_z = 0
		else:
			self.pfx_z = float(pfx_z)

	def getData(self):
		output = np.array([self.pitch_date, self.pitch_type, self.velocity, self.rel_x, self.rel_z])
		return output
