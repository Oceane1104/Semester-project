import os
import pandas as pd
import numpy as np
import glob
import time
import xlrd

from plot_settings import TITLE

# import functions from other python filess
from tools import extract_pattern_in_string
from tools import get_chips_from_experience
from tools import get_experience_from_chip
from tools import select_capas_with_parameter
from tools import extract_voltage_in_graphtype
from tools import load_process_param_df
from tools import load_geom_param_df
from tools import get_file_names
from Visualize import plot_PV, plot_CV, plot_pund, plot_IV, plot_PV_special, plot_PV_and_calculate_energy, plot_energy_data

#from folder1.file1 import ma_fonction$

# import plot settings
from plot_settings import GRAPHES_TO_PLOT
from plot_settings import GRAPH_VOLTAGES

from plot_settings import SELECTED_CHIPS
from plot_settings import SELECTED_EXPERIENCES 
from plot_settings import SELECTED_GEOMETRIES
from plot_settings import SELECTED_PLACEMENTS
from plot_settings import SPECIAL, SPECIAL_CHIPS, SPECIAL_EXPERIENCES, SPECIAL_GEOMETRIES, SPECIAL_PLACEMENT, SPECIAL_PLOT, FOLDER, INTEGRAL, PLOT_RESULT_ENERGY, CHIP_RESULT_ENERGY

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

#PATH_OUTPUT = PATH_FOLDER + '\\Plots' + "\\" + TITLE
PATH_OUTPUT = PATH_FOLDER + '\\Plots' + "\\" + FOLDER


os.makedirs(PATH_OUTPUT, exist_ok=True)

PATH_PROCESSED_DATA = PATH_FOLDER + '\\Data\\Processed'
PATH_INTERIM_DATA = PATH_FOLDER + '\\Data\\Interim'
PATH_PROCESS_PARAM_FILE = PATH_FOLDER + '\\User_input\\process_parameter.xlsx'
PATH_GEOM_PARAM_FILE = PATH_FOLDER + '\\User_input\\geometrical_parameter.xlsx'

### Load parameters
process_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
geom_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)

if (not(SPECIAL) and not(PLOT_RESULT_ENERGY)):

    chip_names = np.array(process_df.index)
    if SELECTED_CHIPS != []:
        chip_names = SELECTED_CHIPS
    #SELECTED_CHIPS = chip_names
    #print(chip_names)

    ### Select capacitors to plot
    interim_files = get_file_names(PATH_INTERIM_DATA, chip_names)

    capas_with_process = select_capas_with_parameter(interim_files, SELECTED_EXPERIENCES, 3)
    capas_with_geom = select_capas_with_parameter(capas_with_process, SELECTED_GEOMETRIES, 1)
    capas_to_plot = select_capas_with_parameter(capas_with_geom, SELECTED_PLACEMENTS, 2)
    print("selected capacitors:",capas_to_plot)

    
    ### Plot graphes
    for graph in GRAPHES_TO_PLOT:
        print("\n***** Plotting of graph", graph)
        if(INTEGRAL):
            plot_PV_and_calculate_energy(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT, process_df, geom_df)
        else:
            if extract_pattern_in_string(graph, "P-V") is not None:
                plot_PV(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT, process_df, geom_df)

            elif extract_pattern_in_string(graph, "IV") is not None:
                plot_IV(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT, process_df, geom_df)
                
            elif extract_pattern_in_string(graph, "CV") is not None:
                plot_CV(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT, process_df, geom_df)
                
            elif extract_pattern_in_string(graph, "PUND") is not None:
                plot_pund(capas_to_plot, graph, PATH_INTERIM_DATA, PATH_OUTPUT, process_df, geom_df)
elif(not(PLOT_RESULT_ENERGY) and SPECIAL):
    chip_names = np.array(process_df.index)
    if SPECIAL_CHIPS != []:
        chip_names = SPECIAL_CHIPS
    #SELECTED_CHIPS = chip_names
    #print(chip_names)

    capas_to_plot = []
    total_graph = []
    for i, chip in enumerate(chip_names):
        interim_files = get_file_names(PATH_INTERIM_DATA, chip)

        capas_with_process_inter = select_capas_with_parameter(interim_files, SPECIAL_EXPERIENCES, 3)
        capas_with_geom_inter = select_capas_with_parameter(capas_with_process_inter, SPECIAL_GEOMETRIES, 1)
        capas_to_plot_inter = select_capas_with_parameter(capas_with_geom_inter, SPECIAL_PLACEMENT, 2)

        total_graph.extend([SPECIAL_PLOT[i]] * len(capas_to_plot_inter))

        # Étendre la liste de tous les capaciteurs sélectionnés
        capas_to_plot.extend(capas_to_plot_inter)

    print("selected capacitors:",capas_to_plot)
    print("selected graph:",total_graph)

    ### Plot graphes
    print("\n***** Plotting of graph", SPECIAL_PLOT)
    if extract_pattern_in_string(SPECIAL_PLOT[0], "P-V") is not None:
        plot_PV_special(capas_to_plot, total_graph, PATH_INTERIM_DATA, PATH_OUTPUT, SPECIAL_PLOT, process_df, geom_df)

### Plot results
# nom du fichier
#  fct qui retrouver le bon ficheir
# Trouvez l'index de la ligne correspondant à la chip spécifique dans la première colonne

if(PLOT_RESULT_ENERGY):
    plot_energy_data(PATH_PROCESS_PARAM_FILE, CHIP_RESULT_ENERGY, PATH_PROCESSED_DATA)

print("\n***********End*********")