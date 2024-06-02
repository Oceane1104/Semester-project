import os
import pandas as pd
import numpy as np
import glob
import time
import xlrd
import re
import matplotlib.pyplot as plt
from scipy.integrate import simps
import openpyxl
from zipfile import BadZipFile

# import functions from other python files
from tools import extract_pattern_in_string
from tools import get_chips_from_experience
from tools import get_experience_from_chip
from tools import extract_info_in_capa_name
from tools import select_capas_with_parameter
from tools import extract_voltage_in_graphtype
from tools import load_process_param_df
from tools import load_geom_param_df
from tools import butter_lowpass_filter
from tools import PUND_to_PV
from tools import integrate_pund
from tools import integrate_pund_lkg
from tools import get_pund_times

### CHANGE IF NECESSARY
#---graph types to load: see below

#---chips to load or calculate
selected_chips = ""
#selected_chips = "" # if you want to load all chips in the process parameter file

## PATHS
user = input("Who are you? Nathalie, Océane, Tom, Thibault ")

if (user == "Nathalie"):     
    PATH_FOLDER = 'C:\\Users\\natha\\Downloads\\Semester_project'
    LIST_GRAPH = ["P-V 1V_2#1","P-V 2V_2#1","P-V 3V_2#1", "P-V 4V_2#1","P-V 5V_1#1", "PUND 5V_1#1", "P-V 7V_1#1", 
                  "P-V 10V_1#1","PUND 7V_1#1","PUND 10V_1#1", "IV 3V_1#1", "CV 3V_1#1", "IV 5V_1#1", "CV 5V_1#1"]
elif (user == "Océane"):
    PATH_FOLDER = 'C:\\Documents\\EPFL\\MA4\\Projet_de_semestre\\Code\\Projet_final'
    LIST_GRAPH = [ "P-V 5V_1#1", "P-V 6V_1#1", "P-V 7V_1#1", "P-V 8V_1#1", "P-V 9V_1#1", "P-V 10V_1#1", "P-V 40V_1#1", 
                  "P-V 29V_1#1", "P-V 15V_1#1", "P-V 17V_1#1", "P-V 18V_1#1", "P-V 19V_1#1", "P-V 20V_1#1", 
                  "P-V 21V_1#1", "P-V 22V_1#1", "P-V 23V_1#1", "P-V 24V_1#1", "P-V 25V_1#1", "P-V 28V_1#1", "P-V 29V_1#1", "P-V 30V_1#1", "P-V 32V_1#1"
                  "PUND 5V_for5V#1", "PUND 7V_for7V#1", "PUND 8V_for8V#1", "PUND 10V_for10V#1", "PUND 12V_for12V#1", "PUND 14V_for14V#1", "PUND 15V_for15V#1",
                   "PUND 17V_for17V#1","PUND 18V_for18V#1" , "PUND 19V_for19V#1", "PUND 20V_for20V#1", "PUND 21V_for21V#1", 
                  "PUND 22V_for22V#1", "PUND 23V_for23V#1", "PUND 24V_for24V#1", "PUND 25V_for25V#1", "PUND 28V_for28V#1",
                  "PUND 29V_for29V#1", "PUND 30V_for30V#1", "PUND 32V_for32V#1"
                  "CV 3V_1#1", "CV 6V_1#1", "CV 8V_1#1", "CV 10V_1#1", "CV 11V_1#1", "CV 12V_1#1", "CV 13V_1#1", "CV 14V_1#1",
                  "CV 15V_1#1", "CV 18V_1#1", "CV 20V_1#1", "CV 22V_1#1", "CV 23V_1#1", "CV 24V_1#1"]
    
    #  "P-V 5V_1#1", "P-V 6V_1#1", "P-V 7V_1#1", "P-V 8V_1#1", "P-V 9V_1#1", "P-V 10V_1#1", "P-V 40V_1#1", 
    #               "P-V 29V_1#1", "P-V 15V_1#1", "P-V 17V_1#1", "P-V 18V_1#1", "P-V 19V_1#1", "P-V 20V_1#1", 
    #               "P-V 21V_1#1", "P-V 22V_1#1", "P-V 23V_1#1", "P-V 24V_1#1", "P-V 25V_1#1", "P-V 28V_1#1", "P-V 29V_1#1", "P-V 30V_1#1", "P-V 32V_1#1"
    #               "PUND 5V_for5V#1", "PUND 7V_for7V#1", "PUND 8V_for8V#1", "PUND 10V_for10V#1", "PUND 12V_for12V#1", "PUND 14V_for14V#1", "PUND 15V_for15V#1",
     #               "PUND 17V_for17V#1", 
# , "PUND 19V_for19V#1", "PUND 20V_for20V#1", "PUND 21V_for21V#1", 
#                   "PUND 22V_for22V#1", "PUND 23V_for23V#1", "PUND 24V_for24V#1", "PUND 25V_for25V#1", "PUND 28V_for28V#1",
#                   "PUND 29V_for29V#1", "PUND 30V_for30V#1", "PUND 32V_for32V#1"
#                   "CV 3V_1#1", "CV 6V_1#1", "CV 8V_1#1", "CV 10V_1#1", "CV 11V_1#1", "CV 12V_1#1", "CV 13V_1#1", "CV 14V_1#1",
#                   "CV 15V_1#1", "CV 18V_1#1", "CV 20V_1#1", "CV 22V_1#1", "CV 23V_1#1", "CV 24V_1#1"

elif (user == "Tom"):
    print("Error:Need to create your path")
    exit()
elif (user == "Thibault"):
    PATH_FOLDER = 'C:\\Users\\Travail\\Desktop\\PDS\\Reports'
    LIST_GRAPH = ["P-V 4V_2#1", "P-V 3V neg_2#1", "PUND 5V_1#1", "PUND 5V neg_1#1", "IV 3V_1#1", "CV 3V_1#1",
                  "P-V 5V PUND#1", "P-V 5V PUND neg#1"]
    
else:
    print("Error: Invalid user input.")
    exit()

PATH_OUTPUT = PATH_FOLDER + '\\Plots'
PATH_RAW_DATA = PATH_FOLDER + '\\Data\\Raw'
PATH_INTERIM_DATA = PATH_FOLDER + '\\Data\\Interim'
PATH_PROCESSED_DATA = PATH_FOLDER + '\\Data\\Processed'
PATH_PROCESS_PARAM_FILE = PATH_FOLDER + '\\User_input\\process_parameter.xlsx'
PATH_GEOM_PARAM_FILE = PATH_FOLDER + '\\User_input\\geometrical_parameter.xlsx'


#***** Function: get_area *****
def get_area(geom_param_df):
    
    area = 0
    size = 0
    area = (int(size)*10**(-4))**2
    return area

#***** Function: extract_capa_info *****
# Input: filename of raw data, graph type, geomParam dataframe
# Output: string with capa info: capa placement + geom parameters  
def extract_capa_info_from_raw_data(file_name, graph_type, geomParam):
    capa_info_raw = file_name.split(graph_type)[0]

    last_char_ok = False
    while last_char_ok == False:
        last_char = capa_info_raw[-1]
        if last_char == '_' or last_char == ' ' or last_char == '-':
            capa_info_raw = capa_info_raw[:-1]
        else: 
            last_char_ok = True

    # Séparation
    parts = capa_info_raw.split('_')

    # Loop through each column of the DataFrame along with its name -> loop over each geometrical parameter
    # Normally the geometrical parameter of each capa should be given in the filename
    geom_param_val = ""
    geom_param_indices = []

    goem_rows = ['-'.join(map(str, row)) for row in geomParam.values.astype(str).tolist()]
    param_x_found = False
    for data_pt in goem_rows:
        for i in range(len(parts)):
            if parts[i] == data_pt:
                geom_param_val = data_pt
                geom_param_indices.append(i)
                param_x_found = True
    if not param_x_found:
        print("\nERROR: No geometrical parameter could not be found in ", file_name,"\n")

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

    

#***** Function: load_raw_data *****
# Input: chipname, graphe type list, geometrical parameters, process parameters
# What it does: 
#   - load all data of 1 chip (all graphtypes of all measured capacitors)
#   - store data of each capacitor in one file (different sheets for the different graph types)
# Output: list of the names of the stored interim files: chip_name + capa_placement + geom. param. of capa + process param. of capa
def load_raw_data(chip_name, geom_param_df, process_param_df):
    interim_files_stored = []

    # Get a list of paths of all .xls files in the chip folder
    xls_file_paths = []
    xls_file_names = []

    error = False
    pattern = os.path.join(PATH_RAW_DATA, "**", chip_name) # Construct the pattern to search for the specific subfolder name
    directories = glob.glob(pattern)  # Use glob to search for directories matching the pattern
    if directories: # Check if any directories were found
        for dir in directories:
            #print("Found the subfolder:", dir)
            files_in_directory = os.listdir(dir)
            for file in files_in_directory: # Iterate over the files in the current directory
                if file.endswith('.xls'): # Check if the file has a .xls extension
                    xls_file_paths.append(os.path.join(dir, file)) 
                    xls_file_names.append(file) 
        print()

    else:
        error = True
        print("ERROR: chip", chip_name, "was not found")

    
    # for each file of a specific chip, get a list of the measured capacitors:
    capa_list = []
    graph_list = []
    file_paths = []
    for i in range(len(xls_file_names)):
        for graph_type in LIST_GRAPH: # extract graphtype -> skip if none of the searched graphtypes were found
            file_graph_type = extract_pattern_in_string(xls_file_names[i], graph_type)

            if file_graph_type is not None:
                geom_plac_info = extract_capa_info_from_raw_data(xls_file_names[i], file_graph_type, geom_param_df) 
                process_param = get_experience_from_chip(chip_name, process_param_df)
                capa_name = chip_name + "_" + geom_plac_info + "_" + process_param 
                capa_list.append(capa_name)
                graph_list.append(graph_type)
                file_paths.append(xls_file_paths[i])
    graph_list = np.array(graph_list)
    capa_list = np.array(capa_list)
    file_paths = np.array(file_paths)

    capas_unique = np.unique(capa_list)

    # For each capa
    for capa in capas_unique:
        capa_idx = [index for index, value in enumerate(capa_list) if value == capa]
        #print("capa indexes: ", capa_idx)
        sheet_name_list = []
        data_list = []
        for idx in capa_idx:
            # load data into df
            # Determine the file extension and use the appropriate library to read the file
            # if file_paths[idx].endswith('.xls'):
            #     wb = xlrd.open_workbook(file_paths[idx], logfile=open(os.devnull, 'w'))
            #     data_df = pd.read_excel(file_paths[idx], engine='xlrd')
            # elif file_paths[idx].endswith('.xlsx'):
            #     wb = openpyxl.load_workbook(file_paths[idx])
            #     data_df = pd.read_excel(file_paths[idx], engine='openpyxl')
            wb = xlrd.open_workbook(file_paths[idx], logfile=open(os.devnull, 'w'))
            data_df = pd.read_excel(wb)
            if 'PUND' in graph_list[idx]:
                tmp_df = pd.read_excel(file_paths[idx], sheet_name='Sheet3')
                #print(data_df)
                tp  = tmp_df.loc[tmp_df['Unnamed: 0'] ==  'tp', 'Unnamed: 3'].values[0]
                td  = tmp_df.loc[tmp_df['Unnamed: 0'] ==  'td', 'Unnamed: 3'].values[0]
                trf = tmp_df.loc[tmp_df['Unnamed: 0'] == 'trf', 'Unnamed: 3'].values[0]
                tp, td, trf = float(tp), float(td), float(trf)
                data_df['tp']  = np.nan
                data_df['trf'] = np.nan
                data_df['td']  = np.nan
                data_df.loc[0, 'tp']  = tp
                data_df.loc[0, 'trf'] = trf
                data_df.loc[0, 'td']  = td
            data_list.append(data_df)
            sheet_name_list.append(graph_list[idx])

        #***** Create the "PV xV_foryV PUND" plot and load it in the interim file *****  #PUND 5V neg_1#1 PUND 7V_for10V#1 PUND 5V_1#1
        for sheet in sheet_name_list:    
            if 'PUND' in sheet and not 'P-V' in sheet:
                voltage = sheet.split(' ')[1].split('V')[0]
                negative, precedent = '', ''
                if 'neg' in sheet:
                    negative = ' neg'
                if 'for' in sheet:
                    precedent = f"_for{sheet.split('for')[1].split('V')[0]}V"

                pund_index = sheet_name_list.index(sheet)
                pund_data = data_list[pund_index]
                pv_new_df = PUND_to_PV(pund_data, capa+' '+sheet, get_pund_times(pund_data)) 
                data_list.append(pv_new_df)
                sheet_name_list.append(f'P-V {voltage}V{precedent} PUND{negative}#1')

        new_path = PATH_INTERIM_DATA + "\\" + chip_name + "\\" + capa + ".xlsx"
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

        try:
            # store all sheets of the capa into excel file
            if os.path.exists(new_path):
                with pd.ExcelWriter(new_path, engine='openpyxl', mode='a',if_sheet_exists='replace') as writer:
                    for i in range(len(sheet_name_list)):
                        data_list[i].to_excel(writer, sheet_name=sheet_name_list[i], index=False)
            else:
                with pd.ExcelWriter(new_path, engine='openpyxl', mode='w') as writer:
                    for i in range(len(sheet_name_list)):
                        data_list[i].to_excel(writer, sheet_name=sheet_name_list[i], index=False)
            interim_files_stored.append(capa)
            print("Capacitor "+ capa +" loaded")
        except BadZipFile:
            print(f"Le fichier {new_path} est corrompu et ne peut pas être chargé.")
            # Optionnel : ajouter une logique supplémentaire pour gérer le fichier corrompu


    interim_files_stored = np.unique(interim_files_stored)
    if error == False:
        print("****** Chip:",chip_name,"- Raw data loaded and interim data saved ******\n")
        #print("\t\tFiles stored:" )
        #print("\t\t",interim_files_stored,"\n")

    return interim_files_stored

#***** Function: load_interim_data *****
# Loads and returns data for a specific file and graph type
def load_interim_data(interim_file_name, graph_type):
    # filename: chip name _ geometrical parameters _ capa placement _ process parameters
    chip_name = interim_file_name.split("_")[0]

    #chip_name, _,_,_ = extract_info_in_capa_name(interim_file_name, chip_list, [], [])

    file_path = PATH_INTERIM_DATA + "\\" + chip_name + "\\" + interim_file_name + ".xlsx"
    data_df = pd.DataFrame()
    try:
        if os.path.exists(file_path): # check if file_path exists
            with pd.ExcelFile(file_path) as xls:
                sheet_names = xls.sheet_names
                if graph_type in sheet_names: # check if sheet name exists
                    # Read the Excel file
                    data_df = pd.read_excel(file_path, sheet_name=graph_type)
                else:
                    print("WARNING: Sheet name",  graph_type ,"inexistant for capacitor", interim_file_name)
        else:
            print("ERROR: File",interim_file_name,"doesn't exist in path", file_path)
    except BadZipFile:
            print(f"Le fichier {new_path} est corrompu et ne peut pas être chargé.")
            # Optionnel : ajouter une logique supplémentaire pour gérer le fichier corrompu

    return data_df



# ---------------- FUNCTION FOR RESULT

#***** Function: Polarisation *****
# Input: file name, specific graph type that we want 
# Output: Remanent polarisation positive and negative
def Polarisation(name_files, graph_type):
    polarisations = []
    for file in name_files:
        pol_max = np.nan
        pol_min = np.nan

        data = load_interim_data(file, graph_type)

        if len(data): # if data is not empty
            geometry = file.split('_')[1]
            size = geometry.split('-')[0]
            area = (int(size)*10**(-4))**2

            size_phase = len(data['Charge']-1)

            charge_ma = max(data['Charge'])
            charge_mi = min(data['Charge'])
            diff_charge = (charge_ma + charge_mi)/2

            debut_phase2 = int(size_phase/4)
            fin_phase2 = int(3*size_phase/4)
            df_phase2 = data.iloc[debut_phase2:fin_phase2]
            indice_zero = (df_phase2['Vforce'] - 0).abs().idxmin()
            courant_en_zero_pos = df_phase2.loc[indice_zero, 'Charge']

            debut_phase = int(3*size_phase/4)
            size_table = len(data['Charge'])-1
            df_phase3 = data.iloc[debut_phase:size_table]
            indice_zero_2 = (df_phase3['Vforce'] - 0).abs().idxmin()
            courant_en_zero_neg = df_phase3.loc[indice_zero_2, 'Charge']

            pol_max = (courant_en_zero_pos - diff_charge) * 10**(6) / area 
            pol_min = (courant_en_zero_neg - diff_charge) * 10**(6) / area  #µC.cm-²
        polarisations.append([pol_max,pol_min])
        #penser à normaliser les unités
    polarisations = np.array(polarisations)
    return polarisations

def Energy(name_files, graph_type, thickness):
    energy = []
    for file in name_files:
        energy_total = np.nan
        energy_density = np.nan
        energy_lost = np.nan

        data = load_interim_data(file, graph_type)

        if len(data): # if data is not empty
            geometry = file.split('_')[1]
            size = geometry.split('-')[0]
            area = (int(size)*10**(-4))**2
            Volume = area * thickness

            charge_ma = max(data['Charge'])
            charge_mi = min(data['Charge'])
            diff_charge = (charge_ma + charge_mi)/2

            Vforce = data['Vforce']
            Polarisation = (data['Charge'] - diff_charge)*10**6 / Volume
            
            # Find the index of the maximum voltage
            max_voltage_idx = np.argmax(Vforce)

            # Calculate energy densities
            n = len(Vforce)
            energy_total = simps(Vforce[:max_voltage_idx], Polarisation[:max_voltage_idx])
            energy_density = -simps(Vforce[max_voltage_idx:n//2], Polarisation[max_voltage_idx:n//2])
            energy_lost = energy_total - energy_density

        energy.append([energy_density, energy_total, energy_lost])
        #penser à normaliser les unités
    energy = np.array(energy)
    return energy


#***** Function: Polarisation *****
# Input: file name, negative? (0 for PUND pos, 1 for PUND neg)
# Output: Remanent polarisation positive and negative
def Polarisation_PUND(name_files, negative, graph_type):
    polarisations = []
    for file in name_files:
        pol_max = np.nan
        pol_min = np.nan
        data = []
        data = load_interim_data(file, graph_type)

        if (len(data) > 1 and abs(data['I'][0]) > 10**(-12) and abs(data['I'][1]) > 10**(-12)): # if data is not empty
            geometry = file.split('_')[1]
            size = geometry.split('-')[0]
            area = (int(size)*10**(-4))**2

            filtered_I      = butter_lowpass_filter(data['I'], data['t'])
            filtered_data   = pd.DataFrame({'t': data['t'], 'I': filtered_I})
            times = get_pund_times(data)
            chargep         = integrate_pund(filtered_data, 0, times)
            chargen         = integrate_pund(filtered_data, 1, times)

            pol_max = chargep * 10**(6) / area 
            pol_min = chargen * 10**(6) / area  #µC.cm-²
        else:
            print(f"ERROR: could not derive polarisation from {graph_type}")
            pol_max = np.nan
            pol_min = np.nan
        
        if negative == 0:
            polarisations.append([pol_max, pol_min])
        else:
            polarisations.append([pol_min, pol_max])
        #penser à normaliser les unités
    polarisations = np.array(polarisations)
    return polarisations

#***** Function: Coercive field *****
# Input: file name, specific graph type that we want 
# Output: Coercive field positive and negative
def Coercive(name_files, graph_type):
    coercive_field_values = []
    for file in name_files:
        Co_max = np.nan
        Co_min = np.nan

        data = load_interim_data(file, graph_type)

        if len(data): # if data is not empty
            charge_ma = max(data['Charge'])
            charge_mi = min(data['Charge'])
            diff_charge = (charge_ma + charge_mi)/2
            size_phase = len(data['Charge']-1)

            debut_phase2 = int(size_phase/4)
            fin_phase2 = int(3*size_phase/4)
            df_phase2 = data.iloc[debut_phase2:fin_phase2]
            indice_zero = (df_phase2['Charge'] - diff_charge).abs().idxmin()
            Volt_en_zero_pos = df_phase2.loc[indice_zero, 'Vforce']

            fin_phase = int(size_phase/4)
            df_phase3 = data.iloc[0:fin_phase]
            indice_zero_2 = (df_phase3['Charge'] - diff_charge).abs().idxmin()
            Volt_en_zero_neg = df_phase3.loc[indice_zero_2, 'Vforce']

            Co_max = Volt_en_zero_pos
            Co_min = Volt_en_zero_neg

        coercive_field_values.append([Co_max,Co_min])

    coercive_field_values = np.array(coercive_field_values)
    return coercive_field_values

#***** Function: Leakage current*****
# Input: file name, specific graph type that we want 
# Output: Leakage current positive and negative
def Leakage_current(name_files, graph_type):
    leakage = []
    for file in name_files:
        leak_max = np.nan
        leak_min = np.nan

        data = load_interim_data(file, graph_type)

        if len(data): # if data is not empty
            indice_trois = (data['AV'] - 3).abs().idxmin()
            leak_max = data.loc[indice_trois, 'AI']

            indice_trois_min = (data['AV'] + 3).abs().idxmin()
            leak_min = data.loc[indice_trois_min, 'AI']
        leakage.append([leak_max,leak_min])

    leakage = np.array(leakage)
    return leakage

def Leakage_PUND(name_files, negative, graph_type):
    leakage = []
    for file in name_files:
        lkg_max = np.nan
        lkg_min = np.nan
        data = []
        data = load_interim_data(file, graph_type)

        if (len(data) > 1 and abs(data['I'][0]) > 10**(-10) and abs(data['I'][1]) > 10**(-10)): # if data is not empty
            geometry = file.split('_')[1]
            size = geometry.split('-')[0]
            area = (int(size)*10**(-4))**2

            filtered_I      = butter_lowpass_filter(data['I'], data['t'])
            filtered_data   = pd.DataFrame({'t': data['t'], 'I': filtered_I})
            leakagep         = integrate_pund_lkg(filtered_data, 0, get_pund_times(data))
            leakagen         = integrate_pund_lkg(filtered_data, 1, get_pund_times(data))

            lkg_max = leakagep * 10**(6) / area 
            lkg_min = leakagen * 10**(6) / area  #µA.cm-²
        else:
            print(f"ERROR: could not derive leakage from {graph_type}")
            lkg_max = np.nan
            lgk_min = np.nan
        
        if negative == 0:
            leakage.append([lkg_max, lkg_min])
        else:
            leakage.append([lkg_min, lkg_max])
        #penser à normaliser les unités
    leakage = np.array(leakage)
    return leakage

def get_chip_name(capa_name, chip_list):
    chip = None
    for chip in chip_list:
        temp = extract_pattern_in_string(capa_name, chip)
        if temp is not None:
            chip = temp
    return chip


## --------------- MAIN BLOCK
# load parameters
process_param_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
geom_param_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)
chip_names = process_param_df.index
#chip_names = selected_chips
list_graph_str = ' / '.join(LIST_GRAPH)
load = 'yes' #input("\nLoad graphes: "+ list_graph_str+ " of new chips to interim? yes/no: ")
if load=="yes":
    ### PRE-PROCESS FILES AND STORED INTO INTNERIM FOLDER
    print("\n***********Data loading started*********")

    for chip in chip_names:
        chip_interim_path = os.path.join(PATH_INTERIM_DATA, chip)
        if os.path.exists(chip_interim_path):
            load_chip = input(f"Interim data already exists for chip '{chip}'. Do you want to reload data? yes/no: ")
            if load_chip == "yes":
                #start_time = time.time()
                load_raw_data(chip, geom_param_df, process_param_df)
                #end_time = time.time()
                #elapsed_time = end_time - start_time
                #print("\nElapsed time:", elapsed_time, "seconds")
            else:
                print("Loading skipped")
        else: 
            load_raw_data(chip, geom_param_df, process_param_df)


## Get loaded files and corresponding chips
interim_files = []
chips_in_interim = []
for root, dirs, files in os.walk(PATH_INTERIM_DATA):
    for dir in dirs:
        chips_in_interim.append(dir)
    for file in files:
        if file.endswith(".xlsx"):
            interim_files.append(os.path.splitext(file)[0])
chips_in_interim = np.unique(chips_in_interim)
print("\nChips in interim: ",chips_in_interim)
not_loaded_chips = [element for element in chip_names if element not in chips_in_interim]
print("Chips not in interim: ",not_loaded_chips)
print("Number of files in interim: ", len(interim_files))

### GET LIST OF EXPERIENCES
exp_list_process = ['-'.join(map(str, row)) for row in process_param_df.values.astype(str).tolist()]
exp_list_process = np.unique(exp_list_process)
exp_list_geometry = ['-'.join(map(str, row)) for row in geom_param_df.values.astype(str).tolist()]
exp_list_geometry = np.unique(exp_list_geometry)
print("List of all possible process experiences:", exp_list_process)
print("\nList of all possible geometry experiences:\n", exp_list_geometry)
exp_list_all = []
for process in exp_list_process:
    for geom in exp_list_geometry:
        exp_list_all.append(geom + "_" + process)
#print("\nList of all possible combination of experiences:\n", exp_list_all)

#for capa in interim_files:
#    infos = extract_info_in_capa_name(capa, chips_in_interim, exp_list_process, exp_list_geometry)
#    print("\nCapa: ",capa, "\nInfos: ", infos)
          
### CALCULATIONS + STORE RESULT
calculate = 'yes' #input("\nCalculate results using graphes: "+ list_graph_str+ " for the chips in interim? yes/no: ")
if calculate=="yes":

    print("\n***********Calculation started*********")
    calculate_neg = 'yes' #input("\nCalculate negative polarisation / coercive field / leakage values? yes/no: ")

    for exp in exp_list_process: 
        print("\n***Calculations for experience", exp,"***")
        #chips_with_exp = get_chips_from_experience(exp, process_param_df, get_str=False)

        #chip_list = []
        #for chip in chips_with_exp:
        #    if chip in chips_in_interim:
        #        chip_list.append(chip)

        table_experience = []
        chip_list = []
        for capa in interim_files:
            chip, geom, plac, process  = extract_info_in_capa_name(capa, chips_in_interim, [exp], exp_list_geometry)
            if chip != "" and geom != "" and process != "":
                table_experience.append(capa)
                chip_list.append(chip)

        if table_experience == []:
            print("No capacitors found for experience", exp)
            continue

        chip_str = "_".join(np.unique(chip_list))
        new_path = PATH_PROCESSED_DATA + "\\" + exp + "_" + chip_str + ".xlsx"
        print("experience:", exp, "chips:",chip_str)

        calculate = True
        if os.path.exists(new_path):
            continue_calculation = input("\nThe results for the experience "+exp+" for chips "+chip_str+" already exists. Do you want to recalculate? yes/no: ")
            if not continue_calculation == "yes":
                calculate = False

        if calculate:

            result_df = pd.DataFrame(index=range(len(table_experience)),columns=["Chip","Geometry","Placement"])

            for i in range(len(table_experience)):
                infos = extract_info_in_capa_name(table_experience[i], chip_list, [exp], exp_list_geometry)
 
                result_df.iloc[i, result_df.columns.get_loc("Chip")] = infos[0]
                result_df.iloc[i, result_df.columns.get_loc("Geometry")] = infos[1]
                result_df.iloc[i, result_df.columns.get_loc("Placement")] = infos[2]

            for graph_type in LIST_GRAPH:
                if 'P-V' in graph_type:
                    voltage = extract_voltage_in_graphtype(graph_type, "P-V")
                    #Thick_infos = exp.split("-")
                    #thickness = (int(Thick_infos[0]) + int(Thick_infos[1])) * int(Thick_infos[2])
                    result_df["Forward Polarisation "+voltage] = Polarisation(table_experience, graph_type)[:,0]
                    #result_df["Energy density "+voltage] = Energy(table_experience, graph_type, thickness)[:,0]
                    #result_df["Energy total "+voltage] = Energy(table_experience, graph_type, thickness)[:,1]
                    #result_df["Energy lost "+voltage] = Energy(table_experience, graph_type, thickness)[:,2]
                    if calculate_neg == "yes":
                        result_df["Reverse Polarisation "+voltage] = Polarisation(table_experience, graph_type)[:,1]
                    #print("Polarisations calculated for plot " + graph_type)

                    result_df["Forward Coercive field "+voltage] = Coercive(table_experience, graph_type)[:,0]
                    if calculate_neg == "yes":
                        result_df["Reverse Coercive field "+voltage] = Coercive(table_experience, graph_type)[:,1]
                    #print("Coercive fields calculated for plot " + graph_type)
                
                elif 'IV' in graph_type:
                    voltage = extract_voltage_in_graphtype(graph_type, "IV")
                    result_df["Forward Leakage "+voltage] = Leakage_current(table_experience, graph_type)[:,0]
                    if calculate_neg == "yes":
                        result_df["Reverse Leakage "+voltage] = Leakage_current(table_experience, graph_type)[:,1]
                    #print("Leakage currents calculated for plot " + graph_type)

                elif 'PUND' in graph_type and not 'P-V' in graph_type:
                    voltage = graph_type.split(' ')[1].split('V')[0]
                    #print(f"Le voltage est: {voltage}")
                    negative, negative_text = 0, ''
                    if 'neg' in graph_type:
                        negative, negative_text = 1, ' neg'
                    result_df[f"Forward Polarisation PUND {voltage}V {negative_text}"] = Polarisation_PUND(table_experience, negative, graph_type)[:,0]/2
                    if calculate_neg == "yes":
                        result_df[f"Reverse Polarisation PUND {voltage}V {negative_text}"] = Polarisation_PUND(table_experience, negative, graph_type)[:,1]/2
                    #print("Polarisations calculated for plot " + graph_type)

                    result_df[f"Forward Leakage PUND {voltage}V {negative_text}"] = Leakage_PUND(table_experience, negative, graph_type)[:,0]
                    if calculate_neg == "yes":
                        result_df[f"Reverse Leakage PUND {voltage}V {negative_text}"] = Leakage_PUND(table_experience, negative, graph_type)[:,1]
                    #print("Leakages calculated for plot " + graph_type)
                    
                elif 'CV' in graph_type:
                    print()
                    # calculate coercive field
                    #print("Calculations based on CV plots not implemented yet.")

            # clean result df (remove empty columns)
            result_df_cleaned = result_df.dropna(axis=1, how='all')

            # Calculer les moyennes et les écarts types pour chaque colonne (en ignorant les valeurs vides)
            means = result_df_cleaned.iloc[:, 3:].mean(axis=0, skipna=True)
            stds = result_df_cleaned.iloc[:, 3:].std(axis=0, skipna=True)

            # Créer les nouvelles lignes MEA et STD
            mea_row = ['MEA'] + ['MEA'] + ['MEA'] + means.tolist()
            std_row = ['STD'] + ['STD'] + ['STD'] + stds.tolist()

            # Créer un DataFrame temporaire pour les nouvelles lignes
            new_rows = pd.DataFrame([mea_row, std_row], columns=result_df_cleaned.columns)

            # Concaténer le DataFrame existant avec les nouvelles lignes
            result_df_cleaned = pd.concat([result_df_cleaned, new_rows], ignore_index=True)

            ### STORE RESULT DF TO FILE IN PROCESSED FOLDER
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            with pd.ExcelWriter(new_path, engine='openpyxl', mode='w') as writer:
                result_df_cleaned.to_excel(writer, index=False)

    print("\n***********Calculation completed*********")