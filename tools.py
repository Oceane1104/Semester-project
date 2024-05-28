import re
import pandas as pd
import os
import numpy as np
from scipy.integrate import simps
from scipy.signal import butter, filtfilt
from scipy.integrate import cumtrapz

## PROCESS PARAMETER FILE : FIRST COL: SAMPLE ID, THEN VARIABLES
#***** Function: load_process_param_df *****
def load_process_param_df(PATH):
    process_param = pd.read_excel(PATH)
    # sample_IDs = process_param['sample ID'].to_list() # get a list of all chips
    process_param.set_index('sample ID', inplace=True) # Set the first column (sample ID) as the index
    process_param = process_param.astype(str)
    print(process_param)
    
    # Get the column names
    process_param_names = process_param.columns
    print('\nNumber of process parameters:', len(process_param_names))
    print('Process parameter names:', ', '.join(map(str,process_param_names)))
    return process_param

## GEOMETRICAL PARAMETER FILE : NO INDICATION OF CHIP / SAMPLE IN FILE
#***** Function: load_geom_param_df *****
def load_geom_param_df(PATH):
    geom_param = pd.read_excel(PATH)
    geom_param = geom_param.astype(str)
    print(geom_param)

    # Get the column names
    geom_param_names = geom_param.columns
    print('\nNumber of geometrical parameters:', len(geom_param_names))
    print('Geometrical parameter names:', ', '.join(map(str,geom_param_names)))
    return geom_param


#***** Function: extract_pattern_in_string *****
def extract_info_in_capa_name(capa_name, chip_list, process_exp_list, geom_exp_list):
    rest_parts = capa_name

    # get chip name
    chip_name = ""
    for chip in chip_list:
        if re.search(chip, rest_parts):
            rest_parts_l = re.split(chip, rest_parts) # returns full string if pattern cannot be found
            rest_parts = ''.join(rest_parts_l)
            chip_name = chip

    # get geometrical parameter
    geom_param = ""
    for param in geom_exp_list:
        if re.search(param, rest_parts):
            rest_parts_l = re.split("_"+param+"_", rest_parts) # returns full string if pattern cannot be found
            #chip_name = rest_parts_l[0]
            rest_parts = ''.join(rest_parts_l)
            geom_param = param

    # get process parameter
    process_param = ""
    for param in process_exp_list:
        if re.search(param, rest_parts):
            rest_parts_l = re.split("_"+param, rest_parts) # returns full string if pattern cannot be found
            rest_parts = ''.join(rest_parts_l)
            process_param = param

    # get placement 
    #rest_parts_l = re.split("_", rest_parts) # returns full string if pattern cannot be found
    placement = rest_parts

    return chip_name, geom_param, placement, process_param

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

    pattern = mmnt_type + r' (.*?)_'
    match = re.search(pattern, graph_type)
    if match:
        voltage = match.group(1)
    return voltage

#***** Function: get_chips_from_experience *****
def get_chips_from_experience(experience_string, param_df, get_str = True):
    experience_parts = experience_string.split('-')
    # Get the number of parameter
    nb_params = len(param_df.columns)
    nb_exp_parts = len(experience_parts)
    # Initialisation
    chip_list_final = ""
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

        chip_list_final = df_temp.index.tolist()
        chip_list_final_str = "_".join(df_temp.index)
    else:
        print('Error: Number of parameters are not equal')
    if chip_list_final_str == "":
        print('No chips for the experience', experience_string, 'found')
    if get_str:
        return chip_list_final_str
    else: 
        return chip_list_final


#***** Function: get_experience_from_chip *****
def get_experience_from_chip(chip_name, param_df):
    if chip_name not in param_df.index:
        print("WARNING: chip", chip_name, "not in param_df")
    experience_list = param_df.loc[chip_name].to_list()
    experience_string = '-'.join(map(str,experience_list))
    return experience_string


#***** Function: select_capas_with_parameter *****
# Input: list of all file names, a specific process experience, a specific geometry experience
# Output: list of selected files names which correspond do the given process and geometry experience
# Note: indicate "" if you don't want to give a process or geometry
def select_capas_with_parameter(file_names, experiences, position):
    selected_files = []
    if experiences == []:
        selected_files = file_names
    else:
        for exp in experiences: 
            found = False
            for file in file_names: # Iterate over the files in the current directory
                val = file.split("_")[position]
                if val == exp:
                    selected_files.append(file)
                    found = True
            if not found:
                print("\nERROR: capacitors with parameter", exp, "were not found\n")
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

#***** Function: butter_lowpass_filter *****
# Input: y values, x values, (cutoff frequency), (order)
# Output: less noisy measurement
# Note: only change cutoff frequency in case of error, and do so consistently to keep comparisons relevant
def butter_lowpass_filter(data, data_time, cutoff=2000000, order=5):
    fs = 1 / (data_time[1] - data_time[0])
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    padlen = min(len(data) - 1, 3 * max(len(a), len(b)))  
    filtered_data = filtfilt(b, a, data, padlen=padlen)  
    return filtered_data

PUND_TIMES = [ 25e-6,  50e-6, 150e-6, 175e-6, #1st edge of 1st two pulses
              100e-6, 125e-6, 225e-6, 250e-6, #2nd         1st
              275e-6, 300e-6, 400e-6, 425e-6, #1st         2nd
              350e-6, 375e-6, 475e-6, 500e-6] #2nd         2nd

#***** Function: integrate_pund *****
# Input: dataframe of PUND, negative (false for pos, true for neg), (timestamps of PUND)
# Output: polarisation without residual participations
def integrate_pund(data, negative, times = PUND_TIMES):
    start1    = (data['t'] >= times[0+8*negative]).idxmax()
    end1      = (data['t'] >= times[1+8*negative]).idxmax()
    start2    = (data['t'] >= times[2+8*negative]).idxmax()
    end2      = (data['t'] >= times[3+8*negative]).idxmax()
    integral1 = simps(data['I'][start1:end1], data['t'][start1:end1])
    integral2 = simps(data['I'][start2:end2], data['t'][start2:end2])
    result = integral1 - integral2

    return result

#***** Function: integrate_pund_lkg *****
# Input: dataframe of PUND, negative (false for pos, true for neg), (timestamps of PUND)
# Output: only second ramps, to be able to compare leakages
def integrate_pund_lkg(data, negative, times = PUND_TIMES):
    start2    = (data['t'] >= times[2+8*negative]).idxmax()
    end2      = (data['t'] >= times[3+8*negative]).idxmax()
    integral2 = simps(data['I'][start2:end2], data['t'][start2:end2])
    result = integral2

    return result

#***** Function: PUND_to_PV *****
# Input: dataframe of PUND, (timestamps of PUND)
# Output: PV 5V plot
# Note: change timestamps if they differ from original PUND 5V
def PUND_to_PV(data, times=PUND_TIMES):
    pv_plot = pd.DataFrame({'Charge': [], 'Vforce': [], 't': []})
    V_array, I_array, Q_array, t_array = [], [], [], []
    for i in range(4):
        start1    = (data['t'] >= times[4*i+0]).idxmax() #start of first ramp
        end1      = (data['t'] >= times[4*i+1]).idxmax()
        start2    = (data['t'] >= times[4*i+2]).idxmax() #start of second ramp
        end2      = (data['t'] >= times[4*i+3]).idxmax()
        min_length = min(end1 - start1, end2 - start2)
        V_array.extend(data['V'][start1:start1+min_length])
        I1 = np.array(data['I'][start1:start1+min_length])
        I2 = np.array(data['I'][start2:start2+min_length])
        
        I_array.extend(I1 - I2)
        delay = 0
        if len(t_array) != 0:
            delay = data['t'][start1] - t_array[len(t_array) - 1]
        t_array.extend(data['t'][start1:start1+min_length] - delay)
        
    Q_array = cumtrapz(I_array, t_array, initial=0)
    
    pv_plot['Charge'], pv_plot['Vforce'], pv_plot['t'] = Q_array, V_array, t_array
    return pv_plot

