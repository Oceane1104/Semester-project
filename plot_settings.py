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
from Visualize import plot_PV, plot_CV, plot_pund, plot_IV


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
#param_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
#geom_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)


# Plot settings
TITLE = "TEST"
LABEL_EXP = True
LABEL_PLAC = True
LABEL_GEO = True
LABEL = "" # experience? placement? geometrie? true/false
SIZE_TITLE = 25
SIZE_AXIS = 25
SIZE_LABELS = 25
SIZE_GRADUATION = 20
SIZE_PLOTS = (25, 12.5)
SIZE_LINE = 0.8
BOX_PLACE = (0.01, 0.95)
LOC_PLACE = "upper left"

#m, μ, n, p
UNIT_X = m
UNIT_Y = 1

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

data_list = ["3dec09_50_bl-s3-c4_DP-450-120", "3dec09_100_bl-s2-4a_DP-450-120"]
plot_CV(data_list, "CV 3V_1#1")
