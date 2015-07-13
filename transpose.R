#! /usr/local/bin/Rscript

# --------------------- IMPORT PACKAGES --------------------- ||

# -------------------- PROCESS ARGUMENTS -------------------- ||
incorrect_args_msg <- "This R script accepts 2 command-line arguments (not more, not less):\n\t(1) Input CSV file\n\t(2) Output CSV file\n\n"
args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 2) {
	inputfile <- args[1]
	outputfile <- args[2]
} else  {
	stop(incorrect_args_msg)
}

# --------------------- MANAGE  DEVICES --------------------- ||

# --------------------- MANAGE  OPTIONS --------------------- ||
options(digits=15)

# ------------------------ FUNCTIONS ------------------------ ||

# ----------------------- MAIN SCRIPT ----------------------- ||
# read in the data
data <- read.csv(inputfile, sep=',', header=FALSE, row.names=NULL)

# transpose the data
table <- t(data)

# write the output
write.table(table, outputfile, sep='\t', row.names=FALSE, col.names=FALSE)

# quit
q()
