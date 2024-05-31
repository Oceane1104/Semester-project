import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

from tools import butter_lowpass_filter, load_process_param_df, load_geom_param_df

from plot_settings import TITLE, LABEL, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE, SHOW_PLOTS

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
                print("WARNING: Sheet name",  graph_type ,"inexistant for capacitor", interim_file_name)
    else:
        print("ERROR: File",interim_file_name,"doesn't exist in path", file_path)

    return data_df

def define_label_name(file_name, process_df, geom_df, graph_type = ""):
    chip_name, geometrical, placement, experience = file_name.split("_") 

    process_names = process_df.columns
    geom_names = geom_df.columns

    if len(process_names)>1:
        exp_parts = experience.split("-")
    else:
        exp_parts = [experience]

    if len(geom_names)>1:
        geom_parts = geometrical.split("-")
    else:
        geom_parts = [geometrical]

    # insert "_" in chip name
    name_start = chip_name.split("4")[0]
    name_end = chip_name.split(name_start)[1]
    chip_name_new = name_start + "_" + name_end

    label_name = "Chip: " + chip_name_new 
    if graph_type != "":
        label_name = label_name + "Graph: "+ graph_type
    if (LABEL_EXP):
        for i in range(len(process_names)):
            label_name = label_name + ", " + process_names[i] + ": " + exp_parts[i]
    if(LABEL_GEO):
        for i in range(len(geom_names)):
            label_name = label_name + ", " + geom_names[i] + ": " + geom_parts[i]
    if (LABEL_PLAC):
        label_name = label_name + ", Placement: " + placement
    return label_name

#***** Plot functions *****
def plot_PV(data_list, graph_type, interim_path, output_path, process_df, geom_df):
    nb_plots = 0

    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS # Liste de couleurs pour les courbes
    
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty:
            continue
        nb_plots += 1
        geometrical = file_name.split("_")[1]
        size = geometrical.split("-")[0]
        Size_num = int(size)
        area = (Size_num*10**(-6))**2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])

        diff_charge = (charge_ma + charge_mi)/2

        label_name = define_label_name(file_name, process_df, geom_df)

        plt.plot(data['Vforce'], (data['Charge'] - diff_charge)/area, marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    plt.title(f"{graph_type} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Polarisation [uC/cm2]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{graph_type}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def plot_pund(data_list, graph_type, interim_path, output_path, process_df, geom_df):
    nb_plots = 0
    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty: 
            continue
        nb_plots +=1
        
        filtered_I = butter_lowpass_filter(data['I'], data['t'])
    
        label_name = define_label_name(file_name, process_df, geom_df)
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


def plot_IV(data_list, graph_type, interim_path, output_path, process_df, geom_df):
    nb_plots = 0
    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty: 
            continue
        nb_plots +=1

        label_name = define_label_name(file_name, process_df, geom_df)
        plt.plot(data['AV'], data['AI'], marker='o', label=f"{label_name}", 
                        color=colors[i-1], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    plt.title(f"{graph_type} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Current [A]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{graph_type}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def plot_CV(data_list, graph_type, interim_path, output_path, process_df, geom_df):
    nb_plots = 0
    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty: 
            continue
        nb_plots +=1
        
        label_name = define_label_name(file_name, process_df, geom_df)
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

def plot_PV_special(data_list, graph_type, interim_path, output_path, special_graph, process_df, geom_df):
    nb_plots = 0

    plt.figure(figsize=SIZE_PLOTS)
    colors = COLORS # Liste de couleurs pour les courbes
    
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type[i], interim_path)
        if data.empty:
            continue
        nb_plots += 1
        geometrical =file_name.split("_")[1]
        size = geometrical.split("-")[0]
        Size_num = int(size)
        area = (Size_num*10**(-6))**2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])

        diff_charge = (charge_ma + charge_mi)/2

        label_name = define_label_name(file_name, process_df, geom_df, graph_type)
        plt.plot(data['Vforce'], (data['Charge'] - diff_charge)/area, marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    plt.title(f"{list(set(special_graph))} {TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Polarisation [mC/cm2]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{list(set(special_graph))}_{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def plots_experience(sizes, columns, process_param_df, path_processed_data, path_output):
    param_names = np.array(process_param_df.columns)
    if not input("Do you want summary plots ? (yes/no) ") == 'yes':
        exit()
    primary_var = input(f"Choose your primary parameter (should be a quantitative value) between 0 and {len(param_names) -1} (position in {param_names}) ")
    primary_var = int(primary_var)
    secondary_var = input(f"Choose a secondary parameter (any) between 0 and {len(param_names) -1} (position in {param_names}) ")
    secondary_var = int(secondary_var)
    for j, size in enumerate(sizes):
        folder = path_processed_data  
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
        for column in columns:
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
            full_path = os.path.join(path_output, filename)

            # Enregistrer le graphique dans le dossier spécifié
            plt.savefig(full_path)

            # Fermer la figure après l'enregistrement pour libérer la mémoire
            plt.close()