import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
import glob

user = input(input("Who are you? Nathalie, Océane, Tom, Thibault"))

## PATHS
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
PATH_RAW_DATA = PATH_FOLDER + '\\Data\\Raw'
PATH_INTERIM_DATA = PATH_FOLDER + '\\Data\\Interim'
PATH_PROCESSED_DATA = PATH_FOLDER + '\\Data\\Processed'
PATH_PROCESS_PARAM_FILE = PATH_FOLDER + '\\User_input\\process_parameter.xlsx'
PATH_GEOM_PARAM_FILE = PATH_FOLDER + '\\User_input\\geometrical_parameter.xlsx'

## GRAPH TYPES
LIST_GRAPH_ALL = ["P-V 1V_1#1", "P-V 1V_2#1", "P-V 2V_1#1", "P-V 2V_2#1", "P-V 3V_1#1", "P-V 3V_2#1", 
                            "P-V 4V_1#1", "P-V 4V_2#1", "P-V 3V neg_1#1", "P-V 3V neg_1#1", "PUND 5V_1#1", "PUND 5V neg_1#1"]
LIST_GRAPH_IMPORTANT = ["P-V 4V_2#1", "IV 3V_1#1", "PUND 5V_1#1", "CV 3V_1#1"]


## PROCESS PARAMETER FILE : FIRST COL: SAMPLE ID, THEN VARIABLES
#***** Function: load_process_param_df *****
def load_process_param_df():
    process_param = pd.read_excel(PATH_PROCESS_PARAM_FILE)
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
def load_geom_param_df():
    geom_param = pd.read_excel(PATH_GEOM_PARAM_FILE)
    print(geom_param)

    # Get the column names
    geom_param_names = geom_param.columns
    print('\nNumber of geometrical parameters:', len(geom_param_names))
    print('Geometrical parameter names:', ', '.join(map(str,geom_param_names)))
    return geom_param


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


#***** Function: extract_capa_info *****
# Input: filename, graph type, geomParam dataframe
# Output: string with capa info: capa placement + geom parameters  
def extract_capa_info(file_name, graph_type, geomParam):
    # Split the string based on the specific sequence (get everything before graph_type)
    capa_info_raw = file_name.split("_"+graph_type)[0]
    #print("\nGraph type:", graph_type)
    #print("Raw capa info",capa_info_raw)
    # Séparation
    parts = capa_info_raw.split('_')

    # Loop through each column of the DataFrame along with its name -> loop over each geometrical parameter
    # Normally the geometrical parameter of each capa should be given in the filename
    geom_param_indices = []
    for column in geomParam.columns:
        column_data_as_str = geomParam[column].astype(str) # Convert to string

        param_x_found = False
        for data_pt in column_data_as_str:
            for i in range(len(parts)):
                if parts[i] == data_pt:
                    param_x_found = True
                    geom_param_indices.append(i)
        if not param_x_found:
            print("\nERROR: the geometrical parameter ", column, " could not be found in ", file_name,"\n")

    # Get geometrical parameters
    geom_param_list = [parts[i] for i in geom_param_indices]
    geom_param_val = '-'.join(geom_param_list)
    #print("Geometrical parameter:",geom_param_val)

    # Get capa placement
        # Get all indices that are not in the 'geom_param_indices' list
    capa_placement_indices = [index for index in range(len(parts)) if index not in geom_param_indices]
    capa_placement_list = [parts[i] for i in capa_placement_indices]
    capa_placement = '-'.join(capa_placement_list)
    #print("Capa placement:",capa_placement)

    # final filename = chip_name + capaPlacement + geomParam + processParam
    capa_info = geom_param_val + "_" + capa_placement
    #print("capa_info:",capa_info,"\n")
    return capa_info


#***** Function: extract_pattern_in_filename *****
def extract_pattern_in_filename(string, pattern):
    # Expression régulière pour rechercher le motif "P-V 1V_1#1" dans le nom de fichier
    match = re.search(pattern, string)
    if match:
        return match.group()
    else:
        return None
    

#***** Function: load_raw_data *****
# Input: chipname, graphe type list, geometrical parameters, process parameters
# What it does: 
#   - load all data of 1 chip (all graphtypes of all measured capacitors)
#   - store data of each capacitor in one file (different sheets for the different graph types)
# Output: list of the names of the stored interim files: chip_name + capa_placement + geom. param. of capa + process param. of capa
def load_raw_data(chip_name, graph_type_list, geom_param_df, process_param_df):

    interim_files_stored = []

    # Get a list of paths of all .xls files in the chip folder
    xls_file_paths = []
    xls_file_names = []

    pattern = os.path.join(PATH_RAW_DATA, "**", chip_name) # Construct the pattern to search for the specific subfolder name
    directories = glob.glob(pattern)  # Use glob to search for directories matching the pattern
    if directories: # Check if any directories were found
        for dir in directories:
            print("Found the subfolder:", dir)
            files_in_directory = os.listdir(dir)
            for file in files_in_directory: # Iterate over the files in the current directory
                if file.endswith('.xls'): # Check if the file has a .xls extension
                    xls_file_paths.append(os.path.join(dir, file)) 
                    xls_file_names.append(file) 

    else:
        print("\nERROR: chip", chip_name, "was not found\n")

    # for each file of a specific chip:
    for i in range(len(xls_file_names)):
        for graph_type in graph_type_list: # extract graphtype -> skip if none of the searched graphtypes were found
            file_graph_type = extract_pattern_in_filename(xls_file_names[i], graph_type)
            if file_graph_type is not None:
                capa_info = extract_capa_info(xls_file_names[i], file_graph_type, geom_param_df)   # extract capa info
                # get process param data for this chip
                process_param = get_experience_from_chip(chip_name, process_param_df)
                new_file_name = chip_name + "_" + capa_info + "_" + process_param  # put together new filename
                new_path = PATH_INTERIM_DATA + "\\" + chip_name + "\\" + new_file_name + ".xlsx"
                
                # Create the directory structure if it doesn't exist
                os.makedirs(os.path.dirname(new_path), exist_ok=True)

                # add data of graphtype to new tab in corresponding file ^
                data_df = pd.read_excel(xls_file_paths[i])
                # Create a Pandas ExcelWriter object
                if os.path.exists(new_path):
                    with pd.ExcelWriter(new_path, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
                        # Write the DataFrame to a specific sheet
                        data_df.to_excel(writer, sheet_name=file_graph_type, index=False)
                else:
                    with pd.ExcelWriter(new_path, engine='openpyxl', mode='w') as writer:
                        # Write the DataFrame to a specific sheet
                        data_df.to_excel(writer, sheet_name=file_graph_type, index=False)
                interim_files_stored.append(new_file_name)
    
    interim_files_stored = np.unique(interim_files_stored)
    print("\n****** Chip:",chip_name,"- Raw data loaded and interim data saved ******\n")
    return interim_files_stored

#***** Function: load_interim_data *****
# Loads and returns data for a specific file and graph type
def load_interim_data(interim_file_name, graph_type):
    # filename: chip name _ geometrical parameters _ capa placement _ process parameters
    chip_name = interim_file_name.split("_")[0]
    file_path = PATH_INTERIM_DATA + "\\" + chip_name + "\\" + interim_file_name + ".xlsx"

    # Load the specific sheet into a DataFrame
    data_df = pd.read_excel(file_path, sheet_name=graph_type)

    return data_df

#***** Function: select_capas_with_parameter *****
# Input: list of all file names, a specific process experience, a specific geometry experience
# Output: list of selected files names which correspond do the given process and geometry experience
# Note: indicate "" if you don't want to give a process or geometry
def select_capas_with_parameter(file_names, process_experience="", geom_experience=""):
    correct_process_files = []
    selected_files = []

    process_found = False
    for file in file_names: # Iterate over the files in the current directory
        process_val = file.split("_")[3]
        if process_experience == "":
            correct_process_files.append(file)
            process_found = True
        else: 
            if process_val == process_experience:
                correct_process_files.append(file)
                process_found = True
    if not process_found:
        print("\nERROR: capacitors with process parameter", process_experience, "were not found\n")

    geom_found = False
    for file in correct_process_files: # Iterate over the files in the current directory
        geom_val = file.split("_")[1]
        if geom_experience == "":
            selected_files.append(file)
            geom_found = True
        else: 
            if geom_val == geom_experience:
                selected_files.append(file)
                geom_found = True
    if not geom_found:
        print("\nERROR: capacitors with geometry parameter", geom_experience, "were not found\n")

    return selected_files

# ---------------- FUNCTION FOR RESULT

#***** Function: Polarisation *****
# Input: file name, specific graph type that we want 
# Output: Remanent polarisation positive and negative
def Polarisation(name_file, graph_type):
    data = load_interim_data(name_file, graph_type)

    size = name_file.split('_')[1]
    area = (int(size)*10**(-6))**2

    charge_ma = max(data['Charge'])
    charge_mi = min(data['Charge'])
    diff_charge = (charge_ma + charge_mi)/2

    debut_phase2 = 200 
    fin_phase2 = 600
    df_phase2 = data.iloc[debut_phase2:fin_phase2]
    indice_zero = (df_phase2['Vforce'] - 0).abs().idxmin()
    courant_en_zero_pos = df_phase2.loc[indice_zero, 'Charge']

    debut_phase = 600 
    size_table = len(data)-1
    df_phase3 = data.iloc[debut_phase:size_table]
    indice_zero_2 = (df_phase3['Vforce'] - 0).abs().idxmin()
    courant_en_zero_neg = df_phase3.loc[indice_zero_2, 'Charge']

    pol_max = (courant_en_zero_pos - diff_charge) / area * 10**2
    pol_min = (courant_en_zero_neg - diff_charge) / area * 10**2
    return pol_max, pol_min

#***** Function: Coercive field *****
# Input: file name, specific graph type that we want 
# Output: Coercive field positive and negative
def Coercive(name_file, graph_type):
    data = load_interim_data(name_file, graph_type)

    charge_ma = max(data['Charge'])
    charge_mi = min(data['Charge'])
    diff_charge = (charge_ma + charge_mi)/2

    debut_phase2 = 200 
    fin_phase2 = 600
    df_phase2 = data.iloc[debut_phase2:fin_phase2]
    indice_zero = (df_phase2['Charge'] - diff_charge).abs().idxmin()
    Volt_en_zero_pos = df_phase2.loc[indice_zero, 'Vforce']

    fin_phase = 200  
    df_phase3 = data.iloc[0:fin_phase]
    indice_zero_2 = (df_phase3['Charge'] - diff_charge).abs().idxmin()
    Volt_en_zero_neg = df_phase3.loc[indice_zero_2, 'Vforce']

    Co_max = Volt_en_zero_pos
    Co_min = Volt_en_zero_neg
    return Co_max, Co_min

#***** Function: Leakage current*****
# Input: file name, specific graph type that we want 
# Output: Leakage current positive and negative
def Leakage_current(name_file):
    data = load_interim_data(name_file, "IV 3V_1#1")

    indice_trois = (data['AV'] - 3).abs().idxmin()
    leak_max = data.loc[indice_trois, 'AI']

    indice_trois_min = (data['AV'] + 3).abs().idxmin()
    leak_min = data.loc[indice_trois_min, 'AI']

    return leak_max, leak_min

## --------------- MAIN BLOCK
# load parameters
process_param_df = load_process_param_df()
geom_param_df = load_geom_param_df()


# get list of experiences
exp_list_process = ['-'.join(map(str, row)) for row in process_param_df.values.tolist()]
exp_list_process = np.unique(exp_list_process)
exp_list_geometry = ['-'.join(map(str, row)) for row in geom_param_df.values.tolist()]
exp_list_geometry = np.unique(exp_list_geometry)

print("\nList of all possible process experiences:\n", exp_list_process)
print("\nList of all possible geometry experiences:\n", exp_list_geometry)

exp_list_all = []
for process in exp_list_process:
    for geom in exp_list_geometry:
        exp_list_all.append(geom + "_" + process)
print("\nList of all possible combination of experiences:\n", exp_list_all)



### PRE-PROCESS FILES AND STORED INTO INTERIM FOLDER
chip_names = process_param_df.index
chip_names = ['3dec11', '3dec09', '3dec17'] ## select which chips to load


for chip in chip_names:
    chip_interim_path = os.path.join(PATH_INTERIM_DATA, chip)
    if os.path.exists(chip_interim_path):
        print(f"Interim data already exists for chip '{chip}'. Skipping loading raw data.")
        # interim_files = load_raw_data(chip, LIST_GRAPH_IMPORTANT, geom_param_df, process_param_df)
    else:
        interim_files = load_raw_data(chip, LIST_GRAPH_IMPORTANT, geom_param_df, process_param_df)

xlsx_files = []
for root, dirs, files in os.walk(PATH_INTERIM_DATA):
    for file in files:
        if file.endswith(".xlsx"):
            xlsx_files.append(os.path.splitext(file)[0])

interim_files = xlsx_files

selected_files = select_capas_with_parameter(interim_files, "DP-450-120")
print("\nSelected files: ", selected_files)

selected_files = select_capas_with_parameter(interim_files, "DP-450-120", "50")
print("\nSelected files of size 50: ", selected_files)


### CALCULATIONS + STORE RESULT
test_exp = []
for chip in chip_names:
    test_exp.append(get_experience_from_chip(chip, process_param_df))
#exp_list_process

for exp in test_exp:
    result_df = pd.DataFrame(columns=["Geometrie - Placement", "Polarisation", "Leakage", "Coercive"])

    table_experience = select_capas_with_parameter(interim_files, process_experience=exp)
    GeoPlac_table = []
    Pol_table = []
    Leak_table = []
    Coe_table = []
    for name_file in table_experience:
        GeoPlac_table.append(name_file.split("_")[1] + "_" + name_file.split("_")[2])
        Pol_table.append(Polarisation(name_file, "P-V 4V_2#1")[0])
        Leak_table.append(Leakage_current(name_file)[0])
        Coe_table.append(Coercive(name_file, "P-V 4V_2#1")[0])

    result_df["Geometrie - Placement"] = GeoPlac_table
    result_df["Polarisation"] = Pol_table
    result_df["Leakage"] = Leak_table
    result_df["Coercive"] = Coe_table

    ### STORE RESULT DF TO FILE IN PROCESSED FOLDER
    new_path = PATH_PROCESSED_DATA + "\\" + exp + ".xlsx"
    os.makedirs(os.path.dirname(new_path), exist_ok=True)

    if os.path.exists(new_path):
        with pd.ExcelWriter(new_path, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
            result_df.to_excel(writer, index=False)
    else:
        with pd.ExcelWriter(new_path, engine='openpyxl', mode='w') as writer:
            result_df.to_excel(writer, index=False)