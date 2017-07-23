# Pitch object class

class Pitch(object):
	def __init__(self, date, pitch_type, velocity, rel_x, rel_z):
		self.pitch_date = date
		self.pitch_type = pitch_type
		self.velocity = velocity
		self.rel_x
		self.rel_z

	def getData(self):
		output = np.array([self.pitch_date, self.pitch_type, self.velocity, self.rel_x, self.rel_z])
		return output
