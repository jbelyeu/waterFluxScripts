#! /usr/bin/env python

import argparse
import sys
#from Tree import *
#import TreeType
#from Day import *
import Tree
#import Day

#def readTreeTypesFile(name):
def readTreeTypesFile(tree_types_file):
	tree_types = {}

#	tree_types_file = open(name, 'r')

	line = tree_types_file.readline() # skip past header

	for line in tree_types_file:
		line = line.strip().split(',')
		if line[1] == 'A':
			tree_types[line[0]] = "angiosperm"
		elif line[1] == 'G':
			tree_types[line[0]] = "gymnosperm"
		else:
			sys.stderr.write("Invalid Tree type!\n")
			sys.exit(1)

	tree_types_file.close()

	return tree_types

#def readFluxFile(name,tree_types):
def readFluxFile(flux_file, tree_types):

#	flux_file = open(name, 'r')

	trees = {}

	line = flux_file.readline() #skip past header
	for line in flux_file:
		line = line.strip().split(",")
		if line[0] not in trees:
			trees[line[0]] = Tree.Tree(line[0], "gymnosperm")
		date = line[1].split(" ")[0]
		timestamp = line[1].split(" ")[1]
		flux = line[2]
		trees[line[0]].add_day(date)
		trees[line[0]].add_measurement(date,timestamp,flux)

	flux_file.close()

	return trees

#def readRadiusFile(name):
def readRadiusFile(radius_file):

#	radius_file = open(name, 'r')

	conductive = {}
	non_conductive = {}
	total = {}

	line = radius_file.readline() #skip past header
	for line in radius_file:
		line = line.strip().split(",")
		conductive[line[0]] = line[1]
		non_conductive[line[0]] = line[2]
		total[line[0]] = line[3]

	radius_file.close()

	return conductive,non_conductive,total

def qualitycontrol(trees):
	for key in trees:
		trees[key].clean_days()

def make_J0_table(trees):
	j0_table = []
	for i in range(0,len(trees)):
		key = trees.keys()[i]
		if i > 0:
			j0_table += trees[key].get_daily_J_0_table()[1:]
		else:
			j0_table = trees[key].get_daily_J_0_table()
	return j0_table

def make_Js_and_et_tables(trees):
	js_table = []
	et_table = []

	for i in range(0,len(trees)):
		key = trees.keys()[i]
		if i > 0:
			js_temp, et_temp = trees[key].get_daily_J_s_and_E_t_table()
			js_table += js_temp[1:]
			et_table += et_temp[1:]
		else:
			js_table, et_table = trees[key].get_daily_J_s_and_E_t_table()
	
	return js_table, et_table
	
def make_J0_and_Js_and_et_ave_tables(trees):
	j0_table = [["TREE_ID","J_0 (g * cm^-2 * d^-1)"]]
	js_table = [["TREE_ID","J_s (g * cm^-2 * d^-1)"]]
	et_table = [["TREE_ID","E_t (kg / d)"]]

	for tree in trees:
		j0_temp = [[trees[tree].name, str(trees[tree].calc_average_daily_J_0())]]
		js_temp = [[trees[tree].name, str(trees[tree].calc_average_daily_J_s())]]
		et_temp = [[trees[tree].name, str(trees[tree].calc_average_daily_E_t())]]
		if float(j0_temp[0][1]) != -1.0:
			j0_table += j0_temp
		if float(js_temp[0][1]) != -1.0:
			js_table += js_temp
		if float(et_temp[0][1]) != -1.0:
			et_table += et_temp

	return j0_table, js_table, et_table

def generate_et_table_day(trees): # transpiration table
	js_table = []
	js_table.append(["TREE_ID","TIMESTAMP","J_s (g * cm^-2 * d^-1)"])

	et_table = []
	et_table.append(["TREE_ID","TIMESTAMP","E_T (kg / d)"])

	for key in trees:
		trees[key].generate_et_table_day(js_table, et_table)
	
	return js_table, et_table

def write_table_to_file(table,out_file_name):
	out_file = open(out_file_name, 'w')

	for row in table:
		for c in range(0,len(row)):
			column = row[c]
			out_file.write(column)
			if c < (len(row) - 1):
				out_file.write(",")
		out_file.write('\n')
	
	out_file.close()

# --------------- MAIN SCRIPT ---------------- ||
if __name__ == "__main__":
#	if len(sys.argv) != 12:
#		sys.stderr.write("usage error (transpiration.py)!\n")
#		sys.exit(1)
	

	parser = argparse.ArgumentParser(description = "Transpiration processor " + 
        "for Decagon datalogger data")
    parser.add_argument("flux_file", type=argparse.FileType('r'),
        help="File of flux data")
    parser.add_argument("radius_file", type=argparse.FileType('r'), 
        help="File of tree radii")
    parser.add_argument("tree_types_file", type=argparse.FileType('r'), 
        help="File of tree types")

    parser.add_argument("js_output_file_30min", type=str, 
        help="File to write js output for 30 minute timeseries")
    parser.add_argument("js_output_file_day", type=str, 
        help="File to write js output for 1 day timeseries")
    parser.add_argument("et_output_file_30min", type=str, 
        help="File to write et output for 30 minute timeseries")
    parser.add_argument("et_output_file_day", type=str, 
        help="File to write et output for 1 day timeseries")
    parser.add_argument("j0_output_file_day", type=str, 
        help="File to write j0 output for 1 day timeseries")
    parser.add_argument("j0_output_file_day_ave", type=str, 
        help="File to write j0 average for 1 day timeseries")
    parser.add_argument("js_output_file_day_ave", type=str, 
        help="File to write js average for 1 day timeseries")
    parser.add_argument("et_output_file_day_ave", type=str, 
        help="File to write et average for 1 day timeseries")

    namespace = parser.parse_args()
    
    flux_file_name = namespace.flux_file                # input
    radius_file_name = namespace.radius_file            # input
    tree_types_file_name = namespace.tree_types_file    # input

    js_output_file_name_30min = namespace.js_output_file_30min		# output
	js_output_file_name_day = namespace.js_output_file_day			# output
	et_output_file_name_30min = namespace.et_output_file_30min		# output
	et_output_file_name_day = namespace.et_output_file_day			# output
	j0_output_file_name_day = namespace.j0_output_file_day			# output
	j0_output_file_name_day_ave = namespace.j0_output_file_day_ave	# output
	js_output_file_name_day_ave = namespace.js_output_file_day_ave	# output
	et_output_file_name_day_ave = namespace.et_output_file_day_ave	# output

	# create the trees
	trees_temp = readFluxFile(flux_file_name, readTreeTypesFile(tree_types_file_name))
	trees = {}

	# add radii info to the trees and remove trees with NAs for radii info
	conductive,non_conductive,total = readRadiusFile(radius_file_name)
	for key in trees_temp:
		if conductive[key] == "NA" or non_conductive[key] == "NA":
			continue

		tot = total[key]
		if tot == "NA":
			tot = float(conductive[key]) + float(non_conductive[key])
		else:
			tot = float(tot)
		
		trees[key] = trees_temp[key]
		trees[key].add_radii(float(conductive[key]), float(non_conductive[key]), tot)
	
	# clean the trees
	qualitycontrol(trees)

	# write output
	j0_table = make_J0_table(trees)
	js_table, et_table = make_Js_and_et_tables(trees)
	write_table_to_file(j0_table,j0_output_file_name_day)
	write_table_to_file(js_table,js_output_file_name_day)
	write_table_to_file(et_table,et_output_file_name_day)
	j0_table_ave, js_table_ave, et_table_ave = make_J0_and_Js_and_et_ave_tables(trees)
	write_table_to_file(j0_table_ave,j0_output_file_name_day_ave)
	write_table_to_file(js_table_ave,js_output_file_name_day_ave)
	write_table_to_file(et_table_ave,et_output_file_name_day_ave)

	sys.exit(0)
