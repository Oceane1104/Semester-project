import re
import pandas as pd
import os

## PROCESS PARAMETER FILE : FIRST COL: SAMPLE ID, THEN VARIABLES
#***** Function: load_process_param_df *****
def load_process_param_df(path):
    process_param = pd.read_excel(path)
    # sample_IDs = process_param['sample ID'].to_list() # get a list of all chips
    process_param.set_index('sample ID', inplace=True) # Set the first column (sample ID) as the index
    print(process_param)
    
    # Get the column names
    process_param_names = process_param.columns
    print('\nNumber of process parameters:', len(process_param_names))
    print('Process parameter names:', ', '.join(map(str,process_param_names)))
    return process_param

## GEOMETRICAL PARAMETER FILE : NO INDICATION OF CHIP / SAMPLE IN FILE
#***** Function: load_geom_param_df *****
def load_geom_param_df(path):
    geom_param = pd.read_excel(path)
    print(geom_param)

#***** Function: extract_pattern_in_string *****
def extract_pattern_in_string(string, pattern):
    # Expression régulière pour rechercher le motif "P-V 1V_1#1" dans le nom de fichier
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return None
    
def extract_voltage_in_graphtype(graph_type, mmnt_type):
    voltage = ""

    pattern = mmnt_type + r' (.*?)#'
    match = re.search(pattern, graph_type)
    if match:
        voltage = match.group(1)
    return voltage

#***** Function: get_chips_from_experience *****
def get_chips_from_experience(experience_string, param_df):
    experience_parts = experience_string.split('-')
    # Get the number of parameter
    nb_params = len(param_df.columns)
    nb_exp_parts = len(experience_parts)
    # Initialisation
    chip_list = []  
    # check that nb params = nb experience parts
    if nb_params == nb_exp_parts:
        df_temp = param_df
        for i in range(nb_params):
            chip_list = []
            param_col = df_temp.iloc[:,i]
            for j in range(len(param_col)):
                if (str(param_col.iloc[j]) == experience_parts[i]):
                    chip_list.append(param_col.index[j])
            #print(chip_list)
            df_temp = df_temp.loc[chip_list] # continue only with rows which have the correct parameter
    else:
        print('Error: Number of parameters are not equal')
    if chip_list is None:
        print('No chips for the experience', experience_string, 'found')
    return chip_list


#***** Function: get_experience_from_chip *****
def get_experience_from_chip(chip_name, param_df):
    experience_list = param_df.loc[chip_name].to_list()
    experience_string = '-'.join(map(str,experience_list))
    return experience_string


#***** Function: select_capas_with_parameter *****
# Input: list of all file names, a specific process experience, a specific geometry experience
# Output: list of selected files names which correspond do the given process and geometry experience
# Note: indicate "" if you don't want to give a process or geometry
def select_capas_with_parameter(file_names, experience, position):
    selected_files = []
    found = False
    if experience == "":
        selected_files = file_names
        found = True
    else:
        for file in file_names: # Iterate over the files in the current directory
            val = file.split("_")[position]
            if val == experience:
                selected_files.append(file)
                found = True
    if not found:
        print("\nERROR: capacitors with parameter", experience, "were not found\n")

    return selected_files

def get_file_names(path,chip_names=[]):
    interim_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".xlsx"):
                if chip_names == []:
                    interim_files.append(os.path.splitext(file)[0])
                else:
                    chip = file.split("_")[0]
                    if chip in chip_names:
                        interim_files.append(os.path.splitext(file)[0])

    #print("\n Interim_files:\n",interim_files, "\n")
    return interim_files
