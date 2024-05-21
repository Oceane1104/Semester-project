import os
import pandas as pd
import numpy as np
import glob
import time
import xlrd
import re
import matplotlib.pyplot as plt
# import functions from other python files
from tools import extract_pattern_in_string
from tools import get_chips_from_experience
from tools import get_experience_from_chip
from tools import select_capas_with_parameter
from tools import extract_voltage_in_graphtype
from tools import load_process_param_df
from tools import load_geom_param_df
from tools import butter_lowpass_filter
from tools import PUND_to_PV
from tools import integrate_pund
from tools import integrate_pund_lkg

### CHANGE IF NECESSARY
#---graph types to load
LIST_GRAPH = ["P-V 3V_2#1", "P-V 4V_2#1", "P-V 5V_1#1", "IV 3V_1#1", "PUND 5V_1#1", "CV 3V_1#1"]

#---chips to load or calculate
selected_chips = ""
#selected_chips = "" # if you want to load all chips in the process parameter file

## PATHS
user = input("Who are you? Nathalie, Océane, Tom, Thibault ")

if (user == "Nathalie"):      
    #Nathalie
    PATH_FOLDER = 'C:\\Users\\natha\\Downloads\\Semester_project'
elif (user == "Océane"):
    #OcéaneT
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
PATH_RAW_DATA = PATH_FOLDER + '\\Data\\Raw'
PATH_INTERIM_DATA = PATH_FOLDER + '\\Data\\Interim'
PATH_PROCESSED_DATA = PATH_FOLDER + '\\Data\\Processed'
PATH_PROCESS_PARAM_FILE = PATH_FOLDER + '\\User_input\\process_parameter.xlsx'
PATH_GEOM_PARAM_FILE = PATH_FOLDER + '\\User_input\\geometrical_parameter.xlsx'

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
            wb = xlrd.open_workbook(file_paths[idx], logfile=open(os.devnull, 'w'))
            data_df = pd.read_excel(wb)
            data_list.append(data_df)
            sheet_name_list.append(graph_list[idx])

        #***** Create the PV 5V plot and load it in the interim file *****
        pundp_index = sheet_name_list.index('PUND 5V_1#1')
        pundp_data = data_list[pundp_index]
        pv_5v_df = PUND_to_PV(pundp_data) 
        data_list.append(pv_5v_df)
        sheet_name_list.append('P-V 5V_1#1')

        new_path = PATH_INTERIM_DATA + "\\" + chip_name + "\\" + capa + ".xlsx"
        os.makedirs(os.path.dirname(new_path), exist_ok=True)

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
    file_path = PATH_INTERIM_DATA + "\\" + chip_name + "\\" + interim_file_name + ".xlsx"

    data_df = []

    if os.path.exists(file_path): # check if file_path exists
        with pd.ExcelFile(file_path) as xls:
            sheet_names = xls.sheet_names
            if graph_type in sheet_names: # check if sheet name exists
                # Read the Excel file
                data_df = pd.read_excel(file_path, sheet_name=graph_type)
            else:
                print("\nERROR: Sheet name",  graph_type ,"inexistant for capacitor", interim_file_name, "\n")
    else:
        print("\nERROR: File",interim_file_name,"doesn't exist in path", file_path, "\n")

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

            pol_max = (courant_en_zero_pos - diff_charge) * 10**(6) / area 
            pol_min = (courant_en_zero_neg - diff_charge) * 10**(6) / area  #µC.cm-²
        polarisations.append([pol_max,pol_min])
        #penser à normaliser les unités
    polarisations = np.array(polarisations)
    return polarisations


#***** Function: Polarisation *****
# Input: file name, negative? (0 for PUND pos, 1 for PUND neg)
# Output: Remanent polarisation positive and negative
def Polarisation_PUND(name_files, negative):
    polarisations = []
    for file in name_files:
        pol_max = np.nan
        pol_min = np.nan
        data = []
        if negative == 0:
            data = load_interim_data(file, 'PUND 5V_1#1')
        else:
            data = load_interim_data(file, 'PUND 5V neg_1#1')

        if len(data): # if data is not empty
            geometry = file.split('_')[1]
            size = geometry.split('-')[0]
            area = (int(size)*10**(-4))**2

            filtered_I      = butter_lowpass_filter(data['I'], data['t'])
            filtered_data   = pd.DataFrame({'t': data['t'], 'I': filtered_I})
            chargep         = integrate_pund(filtered_data, 0)
            chargen         = integrate_pund(filtered_data, 1)

            pol_max = chargep * 10**(6) / area 
            pol_min = chargen * 10**(6) / area  #µC.cm-²
        
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

def Leakage_PUND(name_files, negative):
    leakage = []
    for file in name_files:
        lkg_max = np.nan
        lkg_min = np.nan
        data = []
        if negative == 0:
            data = load_interim_data(file, 'PUND 5V_1#1')
        else:
            data = load_interim_data(file, 'PUND 5V neg_1#1')

        if len(data): # if data is not empty
            geometry = file.split('_')[1]
            size = geometry.split('-')[0]
            area = (int(size)*10**(-4))**2

            filtered_I      = butter_lowpass_filter(data['I'], data['t'])
            filtered_data   = pd.DataFrame({'t': data['t'], 'I': filtered_I})
            leakagep         = integrate_pund_lkg(filtered_data, 0)
            leakagen         = integrate_pund_lkg(filtered_data, 1)

            lkg_max = leakagep * 10**(6) / area 
            lkg_min = leakagen * 10**(6) / area  #µA.cm-²
        
        if negative == 0:
            leakage.append([lkg_max, lkg_min])
        else:
            leakage.append([lkg_min, lkg_max])
        #penser à normaliser les unités
    leakage = np.array(leakage)
    return leakage

def plots_experience(sizes, columns):
    param_names = np.array(process_param_df.columns)
    if input("Do you want summary plots ? (yes/no) ") == 'no':
        exit()
    primary_var = input(f"Choose your primary parameter (should be a quantitative value) between 0 and {len(param_names) -1} (position in {param_names}) ")
    primary_var = int(primary_var)
    secondary_var = input(f"Choose a secondary parameter (any) between 0 and {len(param_names) -1} (position in {param_names}) ")
    secondary_var = int(secondary_var)
    for j, size in enumerate(sizes):
        folder = PATH_PROCESSED_DATA  
        results = []
        for file in os.listdir(folder):
            if file.endswith('.xlsx'):
                full_path = os.path.join(folder, file)
                xl = pd.ExcelFile(full_path)
                
                for nom_feuille in xl.sheet_names:
                    df = pd.read_excel(full_path, sheet_name=nom_feuille)
                    
                    last_line_given_size = df[df.iloc[:, 0] == size].tail(1) #only retains one measurement for a size
                    
                    col_values = last_line_given_size[columns]
                    
                    parametres = file.split('_')[0]
                    parametres_list = parametres.split('-')
                    
                    results.append(parametres_list + list(col_values.values.flatten()))
        results_np = np.array(results).T
        secondaries = results_np[secondary_var]
        primaries = results_np[primary_var].astype(float)
        for i, column in enumerate(columns):
            values = results_np[len(parametres_list) + i].astype(float)
            unique_secondaries = np.unique(secondaries)
        
            fig, ax = plt.subplots()
        
            for secondary in unique_secondaries:
                indices = secondaries == secondary
                ax.plot(primaries[indices], values[indices], '-o', label=f'{param_names[secondary_var]} {secondary}')
        
            ax.set_xlabel(f'{param_names[primary_var]}')
            ax.set_ylabel(f'{column}')
            ax.set_title(f'{column} - {size}x{size}µm²')
            ax.legend()
            
            filename = f'Report - {size}um2 - {column} v. {param_names[primary_var]} comparison.png'

            # Chemin complet pour enregistrer le fichier
            full_path = os.path.join(PATH_OUTPUT, filename)

            # Enregistrer le graphique dans le dossier spécifié
            plt.savefig(full_path)

            # Fermer la figure après l'enregistrement pour libérer la mémoire
            plt.close()


## --------------- MAIN BLOCK
# load parameters
process_param_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
geom_param_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)
chip_names = process_param_df.index
list_graph_str = ' / '.join(LIST_GRAPH)
load = input("\nLoad graphes: "+ list_graph_str+ " of new chips to interim? yes/no: ")
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
    for file in files:
        if file.endswith(".xlsx"):
            chip = file.split("_")[0]
            if chip in chip_names:
                chips_in_interim.append(chip)
                interim_files.append(os.path.splitext(file)[0])
chips_in_interim = np.unique(chips_in_interim)
print("\nChips in interim: ",chips_in_interim)
not_loaded_chips = [element for element in chip_names if element not in chips_in_interim]
print("Chips not in interim: ",not_loaded_chips)



### GET LIST OF EXPERIENCES
exp_list_process = ['-'.join(map(str, row)) for row in process_param_df.values.astype(str).tolist()]
exp_list_process = np.unique(exp_list_process)
exp_list_geometry = ['-'.join(map(str, row)) for row in geom_param_df.values.astype(str).tolist()]
exp_list_geometry = np.unique(exp_list_geometry)
print("List of all possible process experiences:", exp_list_process)
#print("\nList of all possible geometry experiences:\n", exp_list_geometry)
exp_list_all = []
for process in exp_list_process:
    for geom in exp_list_geometry:
        exp_list_all.append(geom + "_" + process)
#print("\nList of all possible combination of experiences:\n", exp_list_all)


### CALCULATIONS + STORE RESULT
calculate = input("\nCalculate results using graphes: "+ list_graph_str+ " for the chips in interim? yes/no: ")
if calculate=="yes":

    print("\n***********Calculation started*********")

    calculate_neg = input("\nCalculate negative polarisation / coercive field / leakage values? yes/no: ")

    test_exp = []
    for chip in chips_in_interim:
        test_exp.append(get_experience_from_chip(chip,process_param_df))

    for exp in test_exp: 
        chips_str = get_chips_from_experience(exp, process_param_df)
        new_path = PATH_PROCESSED_DATA + "\\" + exp + "_" + chips_str + ".xlsx"

        calculate = True
        if os.path.exists(new_path):
            continue_calculation = input("\nThe results for the experience "+exp+" for chips "+chips_str+" already exists. Do you want to recalculate? yes/no: ")
            if not continue_calculation == "yes":
                calculate = False

        if calculate:
            result_df = pd.DataFrame(columns=["Geometry","Placement"])
            table_experience = select_capas_with_parameter(interim_files, [exp],3)
            Geom_table = []
            Placement_table = []
            for name_file in table_experience:
                Geom_table.append(name_file.split("_")[1])
                Placement_table.append(name_file.split("_")[2])
            result_df["Geometry"] = Geom_table
            result_df["Placement"] = Placement_table

            for graph_type in LIST_GRAPH:
                if extract_pattern_in_string(graph_type, "P-V") is not None:
                    voltage = extract_voltage_in_graphtype(graph_type, "P-V")
                    result_df["Pos Polarisation "+voltage] = Polarisation(table_experience, graph_type)[:,0]
                    if calculate_neg == "yes":
                        result_df["Neg Polarisation "+voltage] = Polarisation(table_experience, graph_type)[:,1]
                    print("Polarisations calculated for plot " + graph_type)

                    result_df["Pos Coercive field "+voltage] = Coercive(table_experience, graph_type)[:,0]
                    if calculate_neg == "yes":
                        result_df["Neg Coercive field "+voltage] = Coercive(table_experience, graph_type)[:,1]
                    print("Coercive fields calculated for plot " + graph_type)
                
                elif extract_pattern_in_string(graph_type, "IV") is not None:
                    voltage = extract_voltage_in_graphtype(graph_type, "IV")
                    result_df["Pos Leakage "+voltage] = Leakage_current(table_experience, graph_type)[:,0]
                    if calculate_neg == "yes":
                        result_df["Neg Leakage "+voltage] = Leakage_current(table_experience, graph_type)[:,1]
                    print("Leakage currents calculated for plot " + graph_type)

                elif extract_pattern_in_string(graph_type, "PUND") is not None:
                    result_df["Pos Polarisation PUND"] = Polarisation_PUND(table_experience, 0)[:,0]
                    if calculate_neg == "yes":
                        result_df["Neg Polarisation PUND"] = Polarisation_PUND(table_experience, 0)[:,1]
                    print("Polarisations calculated for plot " + graph_type)

                    result_df["Pos Leakage PUND"] = Leakage_PUND(table_experience, 0)[:,0]
                    if calculate_neg == "yes":
                        result_df["Neg Leakage PUND"] = Leakage_PUND(table_experience, 0)[:,1]
                    print("Leakages calculated for plot " + graph_type)
                    
                elif extract_pattern_in_string(graph_type, "CV") is not None:
                    # calculate coercive field
                    print("Calculations based on CV plots not implemented yet.")

            ### STORE RESULT DF TO FILE IN PROCESSED FOLDER
            os.makedirs(os.path.dirname(new_path), exist_ok=True)
            with pd.ExcelWriter(new_path, engine='openpyxl', mode='w') as writer:
                result_df.to_excel(writer, index=False)

    print("\n***********Calculation completed*********")

SIZES = [50, 100, 150]
OBSERVABLES = ['Pos Coercive field 5V_1', 'Pos Polarisation PUND',  'Pos Leakage PUND']
plots_experience(SIZES, OBSERVABLES)
print("Finished generating report plots !")


print("\n***********Calculation completed*********")
