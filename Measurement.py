#! /usr/bin/env python

import sys

class Measurement:

	def __init__(self, timestamp, flux):
		self.timestamp = timestamp # "HH:MM:SS"
		self.flux = flux # string (normally a float, unless "NA") -- J_0
		self.evapotranspiration = 0.0

	def get_hour(self):
		return int(self.timestamp.split(":")[0])

	def get_minute(self):
		return int(self.timestamp.split(":")[1])

	def get_second(self):
		return int(self.timestamp.split(":")[2])
	
	def get_flux(self):
		return self.flux
	
	def get_evapotranspiration(self):
		return self.evapotranspiration
	
	def is_during_day(self): # between 5am (5:00) and 8pm (20:00)
		hour = self.get_hour()
		if hour < 5 or hour > 20:
			return False
		return True
	
	def is_NA(self):
		return (self.flux == "NA")
	
	def set_evapotranspiration(self, evapotranspiration):
		self.evapotranspiration = evapotranspiration
			

# --------------- MAIN SCRIPT ---------------- ||
if __name__ == "__main__":
	sys.stderr.write("usage error! This file is not meant to be run.\n")
	sys.exit(1)
