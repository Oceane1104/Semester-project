import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

from tools import butter_lowpass_filter, load_process_param_df, PATH_PROCESS_PARAM_FILE, load_geom_param_df, PATH_GEOM_PARAM_FILE

from plot_settings import TITLE, LABEL, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE, SHOW_PLOTS, PATH_PROCESSED_DATA

COLORS = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan', 'brown', 'gray', 'olive', 'pink']

#***** Function: load_interim_data *****
# Loads and returns data for a specific file and graph type
def load_interim_data(interim_file_name, graph_type, interim_path):
    # filename: chip name _ geometrical parameters _ capa placement _ process parameters
    chip_name = interim_file_name.split("_")[0]
    file_path = interim_path + "\\" + chip_name + "\\" + interim_file_name + ".xlsx"

    data_df = pd.DataFrame()

    if os.path.exists(file_path): # check if file_path exists
        with pd.ExcelFile(file_path) as xls:
            sheet_names = xls.sheet_names
            if graph_type in sheet_names: # check if sheet name exists
                # Read the Excel file
                data_df = pd.read_excel(file_path, sheet_name=graph_type)
            else:
                print("Sheet name",  graph_type ,"inexistant for capacitor", interim_file_name)
    else:
        print("ERROR: File",interim_file_name,"doesn't exist in path", file_path)

    return data_df



#***** Plot functions *****
def plot_PV(data_list, graph_type, interim_path, output_path):
    nb_plots = 0

    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS # Liste de couleurs pour les courbes
    
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty:
            continue
        nb_plots += 1
        name, geometrical, placement, experience =file_name.split("_") 
        size = geometrical.split("-")[0]
        Size_num = int(size)
        area = (Size_num*10**(-6))**2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])

        diff_charge = (charge_ma + charge_mi)/2
        label_name = name
        if (LABEL_EXP):
            label_name = label_name + "_" + experience
        if (LABEL_PLAC):
            label_name = label_name + "_" + placement
        if(LABEL_GEO):
            label_name = label_name + "_" + geometrical

        plt.plot(data['Vforce'], (data['Charge'] - diff_charge)/area, marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    plt.title(f"{graph_type} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Polarisation [mC/cm2]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{graph_type}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def plot_pund(data_list, graph_type, interim_path, output_path):
    nb_plots = 0
    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty: 
            continue
        nb_plots +=1
        
        filtered_I = butter_lowpass_filter(data['I'], data['t'])
        name, geometrical, placement, experience =file_name.split("_") 

        label_name = name
        if (LABEL_EXP):
            label_name = label_name + "_" + experience
        if (LABEL_PLAC):
            label_name = label_name + "_" + placement
        if(LABEL_GEO):
            label_name = label_name + "_" + geometrical

        plt.plot(data['t'], filtered_I, marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    plt.title(f"{graph_type} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Time [s]', fontsize=SIZE_AXIS)
    plt.ylabel('Current [A]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{graph_type}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return


def plot_IV(data_list, graph_type, interim_path, output_path):
    nb_plots = 0
    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty: 
            continue
        nb_plots +=1
        name, geometrical, placement, experience =file_name.split("_") 

        label_name = name
        if (LABEL_EXP):
            label_name = label_name + "_" + experience
        if (LABEL_PLAC):
            label_name = label_name + "_" + placement
        if(LABEL_GEO):
            label_name = label_name + "_" + geometrical
        plt.plot(data['AV'], data['AI'], marker='o', label=f"{label_name}", 
                        color=colors[i-1], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    plt.title(f"{graph_type} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Current [?]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{graph_type}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def plot_CV(data_list, graph_type, interim_path, output_path):
    nb_plots = 0
    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty: 
            continue
        nb_plots +=1
        name, geometrical, placement, experience =file_name.split("_") 

        label_name = name
        if (LABEL_EXP):
            label_name = label_name + "_" + experience
        if (LABEL_PLAC):
            label_name = label_name + "_" + placement
        if(LABEL_GEO):
            label_name = label_name + "_" + geometrical
        plt.plot(data['DCV_AB'], data['Cp_AB'], marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return    
    plt.title(f"{graph_type} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Capacitance [F/m2]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{graph_type}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def load_files_from_processed(names, voltage, sign, types, uniques_values):

    data = []

    for filename in os.listdir(PATH_PROCESSED_DATA):
        if os.path.splitext(filename)[0] in names:
            file_path = os.path.join(PATH_PROCESSED_DATA, filename)
            try:
                df = pd.read_csv(file_path) 
                #Pos Polarisation 3V_2
                if f"{sign} Polarization {types}" in df.columns:
                    data.extend(df[f"{sign} {types} {voltage}"].tolist())
                else:
                    print(f"Le fichier {filename} ne contient pas de colonne 'type'.")
            except Exception as e:
                print(f"Erreur lors du chargement du fichier {filename}: {e}")
    return data

def plot_mean_pol(voltage, types, output_path, sign, x_param):
    process_param_df = load_process_param_df(PATH_PROCESS_PARAM_FILE)
    geom_param_df = load_geom_param_df(PATH_GEOM_PARAM_FILE)
    ### GET LIST OF EXPERIENCES
    exp_list_process = ['-'.join(map(str, row)) for row in process_param_df.values.astype(str).tolist()]
    exp_list_process = np.unique(exp_list_process)
    exp_list_geometry = ['-'.join(map(str, row)) for row in geom_param_df.values.astype(str).tolist()]
    exp_list_geometry = np.unique(exp_list_geometry)
    #print("\nList of all possible geometry experiences:\n", exp_list_geometry)
    exp_list_all = []
    for process in exp_list_process:
        for geom in exp_list_geometry:
            exp_list_all.append(geom + "_" + process)

    # Trouver l'index de x_param dans la première ligne de process_param_df
    try:
        index_x_param = process_param_df.columns.get_loc(x_param)
        adjusted_index = index_x_param - 1
        print(f"Index de '{x_param}' dans la première ligne : {index_x_param}, Index ajusté : {adjusted_index}")
    except KeyError:
        print(f"'{x_param}' n'est pas une colonne de process_param_df.")
        return
    
    # Lister toutes les valeurs uniques dans la colonne x_param
    unique_values = process_param_df[x_param].unique()
    print(f"Valeurs uniques dans la colonne '{x_param}': {unique_values}")

    data = load_files_from_processed(exp_list_all, voltage, sign, types, unique_values)

    nb_plots = 0
    return