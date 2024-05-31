import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from scipy.integrate import simps

from tools import butter_lowpass_filter, load_process_param_df, load_geom_param_df

from plot_settings import TITLE, LABEL, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE, SHOW_PLOTS, NAME, LABEL_GRAPH, LABEL_NB_EXP
from plot_settings import TITLE_ADD_SIZE, TITLE_ADD_GRAPH

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

# Fonction pour extraire la partie souhaitée
def extract_relevant_part(graph_type):
    pattern = r"P-V \d+V"
    match = re.search(pattern, graph_type)
    return match.group(0) if match else graph_type

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

    label_name = ""

    if(NAME):
        label_name = "Chip: " + chip_name_new 

    if (LABEL_GRAPH):
        if graph_type != "":
            if (label_name == ""):
                label_name = "Graph: "+ extract_relevant_part(graph_type)
            else:
                label_name = label_name + ", Graph: "+ extract_relevant_part(graph_type)
    if (LABEL_EXP):
        if (LABEL_NB_EXP == []):
            for i in range(len(process_names)):
                if (label_name == ""):
                    label_name = process_names[i] + ": " + exp_parts[i]
                else:
                    label_name = label_name + ", " + process_names[i] + ": " + exp_parts[i]
        else:
            for i in range(len(LABEL_NB_EXP)):
                if (label_name == ""):
                    label_name = process_names[LABEL_NB_EXP[i]] + ": " + exp_parts[LABEL_NB_EXP[i]]
                else:
                    label_name = label_name + ", " + process_names[LABEL_NB_EXP[i]] + ": " + exp_parts[LABEL_NB_EXP[i]]
    if(LABEL_GEO):
        for i in range(len(geom_names)):
            if (label_name == ""):
                label_name = geom_names[i] + ": " + geom_parts[i] 
            else:
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
        area = (Size_num*10**(-4))**2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])

        diff_charge = (charge_ma + charge_mi)/2

        label_name = define_label_name(file_name, process_df, geom_df)

        plt.plot(data['Vforce'], (data['Charge'] - diff_charge)*10**6/area, marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)

    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    Finish_title = f"{TITLE}"
    if (TITLE_ADD_GRAPH):
        Finish_title = f"{Finish_title} for {extract_relevant_part(graph_type)}"
    if (TITLE_ADD_SIZE):
        Finish_title = f"{Finish_title} for {size}µm"

    plt.title(Finish_title, fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Polarisation [µC/cm2]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{Finish_title}.png"))
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
        area = (Size_num*10**(-4))**2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])

        diff_charge = (charge_ma + charge_mi)/2

        label_name = define_label_name(file_name, process_df, geom_df, graph_type[i])
        plt.plot(data['Vforce'], (data['Charge'] - diff_charge)*10**6/area, marker='o', label=f"{label_name}", 
                        color=colors[(i-1)%len(colors)], linewidth=SIZE_LINE)
    if nb_plots == 0:
        print("No", graph_type, "data available for for capacitors", data_list)
        return
    #{list(set(special_graph))} 
    plt.title(f"{TITLE}", fontsize=SIZE_TITLE)
    plt.xlabel('Voltage [V]', fontsize=SIZE_AXIS)
    plt.ylabel('Polarisation [µC/cm2]', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_path, f"{TITLE}.png"))
    if SHOW_PLOTS:
        plt.show()
    return

def plot_PV_and_calculate_energy(data_list, graph_type, interim_path, output_path, process_df, geom_df):
    results = []
    
    plt.figure(figsize=(10, 6))
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_list)))
    
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type, interim_path)
        if data.empty:
            continue
        
        geometrical = file_name.split("_")[1]
        size = geometrical.split("-")[0]
        Size_num = int(size)
        area = (Size_num * 10**(-6)) ** 2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])
        diff_charge = (charge_ma + charge_mi) / 2
        
        Vforce = data['Vforce']
        Polarisation = (data['Charge'] - diff_charge) / area
        
        # Find the index of the maximum voltage
        max_voltage_idx = np.argmax(Vforce)

        # Calculate energy densities
        n = len(Vforce)
        energy_total = simps(Vforce[:max_voltage_idx], Polarisation[:max_voltage_idx])
        energy_density = -simps(Vforce[max_voltage_idx:n//2], Polarisation[max_voltage_idx:n//2])
        energy_lost = energy_total - energy_density

        print(f"L'energy density est {energy_density}")
        print(f"L'energy perdue est {energy_lost}")

        label_name = f"L'energy total: {energy_total} L'energy density: {energy_density} et L'energy perdue: {energy_lost}"
        
        # Plot PV curve
        plt.plot(Vforce, Polarisation, marker='o', label=f"{label_name}", color=colors[i], linewidth=2)

        results.append({
            'File': file_name,
            'Energy Total (uJ)': energy_total,
            'Energy Density (uJ/cm^2)': energy_density,
            'Energy Lost (uJ)': energy_lost
        })
        
        # Shade areas under the curves
        plt.fill_between(Vforce[:max_voltage_idx], Polarisation[:max_voltage_idx], color=colors[i], alpha=0.1)
        plt.fill_between(Vforce[max_voltage_idx:n//2], Polarisation[max_voltage_idx:n//2], color=colors[i], alpha=0.3)

        # Add red points for energy_total integration range
        plt.scatter([Vforce[max_voltage_idx], Vforce[n//2]], [Polarisation[max_voltage_idx], Polarisation[n//2]], color='red', zorder=5)

        # Add blue points for energy_density integration range
        plt.scatter([Vforce[0], Vforce[max_voltage_idx]], [Polarisation[0], Polarisation[max_voltage_idx]], color='blue', zorder=5)
    
    if not results:
        print("No", graph_type, "data available for capacitors", data_list)
        return
    
    # Save results to Excel
    results_df = pd.DataFrame(results)
    results_df.to_excel(os.path.join(output_path, "energy_results.xlsx"), index=False)
    
    # Plot configuration
    plt.title(f"{graph_type} PV Curves", fontsize=14)
    plt.xlabel('Voltage [V]', fontsize=12)
    plt.ylabel('Polarisation [µC/cm²]', fontsize=12)
    plt.grid(True)
    plt.legend(loc='best', fontsize=10)
    plt.savefig(os.path.join(output_path, f"{graph_type}_PV_plot.png"))
    plt.show()

    return results_df

#Result of charge energy
def load_process_parameters(file_path):
    return pd.read_excel(file_path)

def load_results(file_path):
    return pd.read_excel(file_path)

def extract_energy_data(process_df, data_list, result_folder):
    results = []
    for chip in data_list:
        # Trouvez l'index de la ligne correspondant à la chip spécifique dans la première colonne
        chip_index = process_df.index[process_df['sample ID'] == chip]

        if len(chip_index) == 0:
            print(f"Chip {chip} n'a pas été trouvé dans le DataFrame.")
        else:
            # Récupérez la ligne complète correspondant à la chip
            row = process_df.loc[chip_index[0]]

            # Générer le nom de fichier en joignant les valeurs de la ligne avec des tirets
            file_name = "-".join(row.iloc[1:].astype(str)) + f"_{chip}.xlsx"
            print(f"Ceci est {file_name}")
            file_path = os.path.join(result_folder, file_name)

            if not os.path.exists(file_path):
                print(f"Le fichier {file_path} n'existe pas.")
            else:
                # Chargez les résultats si le fichier existe
                data = load_results(file_path)
                # Vous pouvez maintenant travailler avec les données chargées
        for col in data.columns:
                if col.startswith("Energy density"):
                    voltage = int(col.split()[2].replace('V_1', ''))
                    energy_density_mean = data[col][data['Chip'] == 'MEA'].values[0]
                    energy_total_col = col.replace("Energy density", "Energy total")
                    energy_total_mean = data[energy_total_col][data['Chip'] == 'MEA'].values[0]
                    efficiency = (energy_density_mean / energy_total_mean) * 100

                    results.append({
                        'Chip': chip,
                        'Voltage': voltage,
                        'Energy_density': energy_density_mean,
                        'Efficiency': efficiency
                    })
    return pd.DataFrame(results)
