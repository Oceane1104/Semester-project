import os
import pandas as pd
import numpy as np
import glob
import time
import xlrd
# import functions from other python files
from tools import extract_pattern_in_string
from tools import get_chips_from_experience
from tools import get_experience_from_chip
from tools import select_capas_with_parameter
from tools import extract_voltage_in_graphtype
from tools import load_process_param_df
from tools import load_geom_param_df


## PATHS
user = input("Who are you? Nathalie, Océane, Tom, Thibault ")

if (user == "Nathalie"):      
    #Nathalie
    PATH_FOLDER = 'C:\\Users\\natha\\Downloads\\Semester_project'
elif (user == "Océane"):
    #Océane
    PATH_FOLDER = 'C:\\Documents\\EPFL\\MA4\\Projet_de_semestre\\Code\\Projet_final'
elif (user == "Tom"):
    print("Error:Need to create your path")
    exit()
elif (user == "Thibault"):
    print("Error:Need to create your path")
    exit()
else:
    print("Error: Invalid user input.")
    exit()

PATH_OUTPUT = PATH_FOLDER + '\\Plots'
PATH_PROCESSED_DATA = PATH_FOLDER + '\\Data\\Processed'
PATH_PROCESS_PARAM_FILE = PATH_FOLDER + '\\User_input\\process_parameter.xlsx'
PATH_GEOM_PARAM_FILE = PATH_FOLDER + '\\User_input\\geometrical_parameter.xlsx'

# Load parameters
param_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
geom_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)


# Plot settings
TITLE = ""
LABEL = "" # experience? placement? geometrie? true/false
SIZE_TITLE = 1
SIZE_AXIS = 1
SIZE_LABELS = 1
SIZE_PLOTS = 1

units = ""

# Choose experience
chip = ""
experience = ""
geometrie = ""
placement = ""

# --> moyenne ?

# Choose graphes ! several at once
GRAPHES_TO_PLOT = ["P-V", "IV", "CV", "PUND"]
VOLTAGES = ["1", "3", "","5"]

# Choose results to plot
RESULTS_TO_PLOT = []
RESULTS_X_AXIS = "parameter x"
RESULTS_LABELS = ""