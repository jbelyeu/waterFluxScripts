#! /usr/bin/env python

import sys
#from enum import Enum
#from Day import *
import Day
import Measurement
import math
#import TreeType

class Tree:
	
	def __init__(self, name, tree_type):
		self.name = name # TREE_ID
		self.tree_type = tree_type # angiosperm/gymnosperm
		self.days = []
		self.conductive_radius = 0.0 # cm
		self.non_conductive_radius = 0.0 # cm
		self.total_radius = 0.0 # cm
		self.conductive_area = 0.0 # cm^2
		self.non_conductive_area = 0.0 # cm^2
		self.total_area = 0.0 # cm^2
	
	def get_name(self):
		return self.name
	
	def get_tree_type(self):
		return self.tree_type
	
	def get_days(self):
		return self.days
	
	def add_day(self, date):
		make_new = True
		for day in self.days:
			if day.date == date:
				make_new = False
		if make_new:
			self.days.append(Day.Day(date))
	
	def add_measurement(self, date, timestamp, flux):
		for day in self.days:
			if day.date == date:
				day.measurements.append(Measurement.Measurement(timestamp, flux))
				break
	
	def get_conductive_radius(self):
		return self.conductive_radius
	
	def get_non_conductive_radius(self):
		return self.non_conductive_radius
	
	def get_total_radius(self):
		return self.total_radius

	def add_radii(self, conductive, non_conductive, total):
		self.conductive_radius = conductive
		self.non_conductive_radius = non_conductive
		self.total_radius = total

		self.update_areas()

	def clean_days(self):
		days_to_remove = []

		for i in range(0,len(self.days)):
			
			day = self.days[i]
			
			if day.is_all_NAs() or day.count_NAs_from_5to20() > 12 or day.count_consecutive_NAs_from_5to20() > 6:
				days_to_remove.append(i)

		for index in days_to_remove[::-1]:
			self.days.pop(index)
	
	def update_areas(self):
		self.conductive_area = math.pi * math.pow(self.conductive_radius, 2)
		self.non_conductive_area = math.pi * math.pow(self.non_conductive_radius, 2)
		self.total_area = math.pi * math.pow(self.total_radius, 2)
	
	def generate_mtable(self, mtable):
		for day in self.days:
			mtable.append([self.name, day.get_dashed_date(), str(day.generate_24hr_m_J0())])
	
	def generate_cmtable(self, mtable):
		for day in self.days:
			mtable.append([self.name, day.get_dashed_date(), str(day.generate_24hr_cm_J0())])
	
	def calc_average_daily_J_0(self):
		josum = 0.0
		count = 0
		if len(self.days) > 0:
			for day in self.days:
				josum += day.calc_J_0()
				count += 1
			return josum / count
		else:
			return -1.0
	
	def calc_average_daily_J_s(self):
		jssum = 0.0
		count = 0
		if len(self.days) > 0:
			for day in self.days:
				jstemp, ettemp = day.calc_J_s_and_E_t(self.tree_type, self.conductive_radius, self.total_radius)
				jssum += jstemp
				count += 1
			return jssum / count
		else:
			return -1.0
	
	def calc_average_daily_E_t(self):
		etsum = 0.0
		count = 0
		if len(self.days) > 0:
			for day in self.days:
				jstemp, ettemp = day.calc_J_s_and_E_t(self.tree_type, self.conductive_radius, self.total_radius)
				etsum += ettemp
				count += 1
			return etsum / count
		else:
			return -1.0
	
	def get_daily_J_0_table(self):
		table = [["TREE_ID","DATE","J_0 (g * cm^-2 * d^-1)"]]
		for day in self.days:
			row = []
			row.append(self.name)
			row.append(day.get_dashed_date())
			row.append(str(day.calc_J_0()))
			table.append(row)
		return table

	def get_daily_J_s_and_E_t_table(self):
		jstable = [["TREE_ID","DATE","J_s (g * cm^-2 * d^-1)"]]
		ettable = [["TREE_ID","DATE","E_t (kg / d)"]]
		for day in self.days:
			jsrow = []
			jsrow.append(self.name)
			jsrow.append(day.get_dashed_date())

			etrow = []
			etrow.append(self.name)
			etrow.append(day.get_dashed_date())

			js, et = day.calc_J_s_and_E_t(self.tree_type, self.conductive_radius, self.total_radius)

			jsrow.append(str(js))
			etrow.append(str(et))
			
			jstable.append(jsrow)
			ettable.append(etrow)

		return jstable, ettable
	
	@staticmethod
	def calculate_area_for_increment(increment_start, increment_end, total_radius):
		inner_area = math.pi * math.pow(total_radius - increment_end,2)
		outer_area = math.pi * math.pow(total_radius - increment_start,2)
		return outer_area - inner_area
	
	@staticmethod
	def calculate_ratio_for_increment(tree_type, relative_sapwood_depth):
		if tree_type == "gymnosperm":
			return 1.257 * math.exp( -0.5 * math.pow((relative_sapwood_depth + 0.3724)/0.6620,2) )
		elif tree_type == "angiosperm":
			return 1.033 * math.exp( -0.5 * math.pow((relative_sapwood_depth - 0.09963)/0.4263,2) )
		else:
			sys.stderr.write("THIS SHOULD NEVER HAPPEN! TreeType isn't gymnosperm or angiosperm.\n")
			sys.exit(1)
	
	@staticmethod
	def calculate_relative_sapwood_depth_for_increment(increment_midpoint, conductive_radius):
		return float(increment_midpoint) / conductive_radius


# --------------- MAIN SCRIPT ---------------- ||
if __name__ == "__main__":
	sys.stderr.write("usage error! This file is not meant to be run.\n")
	sys.exit(1)
