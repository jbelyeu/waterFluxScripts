#! /usr/bin/env python

import sys
#from Tree import *
import Tree
#from Measurement import *
import Measurement
#import TreeType
import math

class Day:

	def __init__(self, date):
		self.date = date # "MM:DD:YYYY"
		self.measurements = []
		#self.J0 = 0.0
		#self.Js = 0.0
		#self.Et = 0.0
	
	def get_dashed_date(self):
		return self.date.replace(":","-")

	def get_month(self):
		return int(self.date.split(":")[0])

	def get_day(self):
		return int(self.date.split(":")[1])

	def get_year(self):
		return int(self.date.split(":")[2])
	
	def get_measurements(self):
		return self.measurements
	
	def is_all_NAs(self):
		for m in self.measurements:
			if not m.is_NA():
				return False
		return True

	def count_NAs_from_5to20(self):
		count = 0
		for m in self.measurements:
			if m.is_during_day() and m.is_NA():
				count += 1
			
		return count
	
	def count_consecutive_NAs_from_5to20(self):
		largest_count = 0
		count = 0
		for m in self.measurements:
			if m.is_during_day() and m.is_NA():
				count += 1
			else:
				count = 0

			if count > largest_count:
				largest_count = count

		return largest_count
	
	def calculate_Ji_from_ratio(self, J0, ratio):
		return J0 * ratio
	
	def sum_measurements(self):
		msum = 0.0
		count = 0
		for m in self.measurements:
			if m.flux != "NA":
				msum += float(m.flux)
				count += 1
		return msum, count
	
	def calc_J_0(self):
		msum, count = self.sum_measurements()
		return  msum * 8.64
	
	def calc_J_0_average(self):
		msum, count = self.sum_measurements()
		return msum * 8.64 / count
		
	def calc_J_s_and_E_t(self, tree_type, conductive_radius, total_radius):
		Js = 0.0 # J_s
		As = 0.0 # A_s
		Et = 0.0 # E_T
		J0 = self.calc_J_0()

		for i in range(1, int(conductive_radius)/2):
			increment_start = (2 * i) - 2
			increment_midpoint = (2 * i) - 1
			increment_end = 2 * i
			rsd = Tree.Tree.calculate_relative_sapwood_depth_for_increment(increment_midpoint, conductive_radius)
			ratio = Tree.Tree.calculate_ratio_for_increment(tree_type, rsd)
			Ji = self.calculate_Ji_from_ratio(J0, ratio)
			Ai = Tree.Tree.calculate_area_for_increment(increment_start, increment_end, total_radius)
			temp = Ji * Ai
			As += Ai
			Js += temp
			Et += temp / 1000
		
		if As != 0:
			Js /= As

		return Js, Et

# --------------- MAIN SCRIPT ---------------- ||
if __name__ == "__main__":
	sys.stderr.write("usage error! This file is not meant to be run.\n")
	sys.exit(1)
