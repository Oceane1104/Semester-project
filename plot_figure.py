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
from tools import get_file_names
from Visualize import plot_PV, plot_CV, plot_pund, plot_IV

#from folder1.file1 import ma_fonction$

# import plot settings
from plot_settings import GRAPHES_TO_PLOT
from plot_settings import GRAPH_VOLTAGES

from plot_settings import SELECTED_EXPERIENCES 
from plot_settings import SELECTED_GEOMETRIES
from plot_settings import SELECTED_PLACEMENTS

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
    PATH_FOLDER = 'C:\\Users\\Travail\\Desktop\\PDS\\Reports'
else:
    print("Error: Invalid user input.")
    exit()

PATH_OUTPUT = PATH_FOLDER + '\\Plots'
PATH_PROCESSED_DATA = PATH_FOLDER + '\\Data\\Processed'
PATH_INTERIM_DATA = PATH_FOLDER + '\\Data\\Interim'
PATH_PROCESS_PARAM_FILE = PATH_FOLDER + '\\User_input\\process_parameter.xlsx'
PATH_GEOM_PARAM_FILE = PATH_FOLDER + '\\User_input\\geometrical_parameter.xlsx'


### Load parameters
param_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
geom_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)

chip_names = np.array(param_df.index)
SELECTED_CHIPS = chip_names
print(chip_names)

### Select capacitors to plot
interim_files = get_file_names(PATH_INTERIM_DATA, SELECTED_CHIPS)

capas_with_process = select_capas_with_parameter(interim_files, SELECTED_EXPERIENCES, 3)
capas_with_geom = select_capas_with_parameter(capas_with_process, SELECTED_GEOMETRIES, 1)
print(capas_with_geom)
capas_to_plot = select_capas_with_parameter(capas_with_geom, SELECTED_PLACEMENTS, 2)



### Plot graphes
for graph in GRAPHES_TO_PLOT:
    if extract_pattern_in_string(graph, "P-V") is not None:
        plot_PV(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT)

    elif extract_pattern_in_string(graph, "IV") is not None:
        plot_IV(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT)
        
    elif extract_pattern_in_string(graph, "CV") is not None:
        plot_CV(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT)
        
    elif extract_pattern_in_string(graph, "PUND") is not None:
        plot_pund(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT)



### Plot results
# nom du fichier
#  fct qui retrouver le bon ficheir

print("\n***********End*********")