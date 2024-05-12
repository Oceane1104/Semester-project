import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
#from make_dataset_V2 import load_interim_data
#from plot_settings import TITLE, LABEL, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, PATH_OUTPUT, LABEL_EXP, LABEL_PLAC, LABEL_GEO


def plot_PV(data_list, graph_type):
    from make_dataset_V2 import load_interim_data
    from plot_settings import TITLE, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, PATH_OUTPUT, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE


    plt.figure(figsize=SIZE_PLOTS)
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type)
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
                        color=colors[i-1], linewidth=SIZE_LINE)
    plt.title(f'Polarisation vs Voltage {TITLE}', fontsize=SIZE_TITLE)
    plt.xlabel('Voltage', fontsize=SIZE_AXIS)
    plt.ylabel('Polarisation', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(PATH_OUTPUT, f"{graph_type}_{TITLE}.png"))
    plt.show()

def plot_pund(data_list, graph_type):
    from make_dataset_V2 import load_interim_data
    from plot_settings import TITLE, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, PATH_OUTPUT, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE

    plt.figure(figsize=SIZE_PLOTS)
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type)
        name, geometrical, placement, experience =file_name.split("_") 

        label_name = name
        if (LABEL_EXP):
            label_name = label_name + "_" + experience
        if (LABEL_PLAC):
            label_name = label_name + "_" + placement
        if(LABEL_GEO):
            label_name = label_name + "_" + geometrical

        plt.plot(data['t'], data['I'], marker='o', label=f"{label_name}", 
                        color=colors[i-1], linewidth=SIZE_LINE)
    plt.title(f'Current vs Time {TITLE}', fontsize=SIZE_TITLE)
    plt.xlabel('Time', fontsize=SIZE_AXIS)
    plt.ylabel('Current', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(PATH_OUTPUT, f"{graph_type}_{TITLE}.png"))
    plt.show()


def plot_IV(data_list, graph_type):
    from make_dataset_V2 import load_interim_data
    from plot_settings import TITLE, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, PATH_OUTPUT, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE

    plt.figure(figsize=SIZE_PLOTS)
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type)
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
    plt.title(f'Current vs Voltage {TITLE}', fontsize=SIZE_TITLE)
    plt.xlabel('Time', fontsize=SIZE_AXIS)
    plt.ylabel('Current', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(PATH_OUTPUT, f"{graph_type}_{TITLE}.png"))
    plt.show()

def plot_CV(data_list, graph_type):
    from make_dataset_V2 import load_interim_data
    from plot_settings import TITLE, SIZE_TITLE, SIZE_AXIS, SIZE_LABELS, SIZE_GRADUATION, SIZE_PLOTS, SIZE_LINE, PATH_OUTPUT, LABEL_EXP, LABEL_PLAC, LABEL_GEO, BOX_PLACE, LOC_PLACE

    plt.figure(figsize=SIZE_PLOTS)
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    for i, file_name in enumerate(data_list):
        data = load_interim_data(file_name, graph_type)
        name, geometrical, placement, experience =file_name.split("_") 

        label_name = name
        if (LABEL_EXP):
            label_name = label_name + "_" + experience
        if (LABEL_PLAC):
            label_name = label_name + "_" + placement
        if(LABEL_GEO):
            label_name = label_name + "_" + geometrical
        plt.plot(data['DCV_AB'], data['Cp_AB'], marker='o', label=f"{label_name}", 
                        color=colors[i-1], linewidth=SIZE_LINE)
    plt.title(f'Charge vs Voltage {TITLE}', fontsize=SIZE_TITLE)
    plt.xlabel('Charge', fontsize=SIZE_AXIS)
    plt.ylabel('Voltage', fontsize=SIZE_AXIS)
    plt.grid(True)
    plt.legend(loc=LOC_PLACE, bbox_to_anchor=BOX_PLACE, fontsize=SIZE_LABELS)
    plt.tick_params(axis='both', labelsize=SIZE_GRADUATION)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(PATH_OUTPUT, f"{graph_type}_{TITLE}.png"))
    plt.show()

    