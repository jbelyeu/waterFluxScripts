#! /usr/local/bin/Rscript

# --------------------- IMPORT PACKAGES --------------------- ||
library(reshape2)

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

# cast the "melted" data back into it's un-melted form
table <- dcast(data, V1~V2, value.var="V3")

# fix the column names
colnames(table)[1] <- ""

# write the output
write.table(table, outputfile, sep=',', row.names=FALSE)

# quit
q()
