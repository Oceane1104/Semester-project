import os
import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np
from make_dataset import load_interim_data
from plot_settings import TITLE

def plot_data(data_list, output_type_folder, graph_type):
    plt.figure(figsize=(25, 12.5))
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    
    for i, chip_name in enumerate(data_list):
        data = load_interim_data(chip_name, graph_type)
        name, geometrical, placement, experience =chip_name.split("_") 
        size = geometrical.split("-")[0]
        Size_num = int(size)
        area = (Size_num*10**(-6))**2
        
        charge_ma = max(data['Charge'])
        charge_mi = min(data['Charge'])

        diff_charge = (charge_ma + charge_mi)/2
        plt.plot(data['Vforce'], (data['Charge'] - diff_charge)/area, marker='o', label=f"{name} - {experience} - {placement} - {geometrical}", 
                        color=colors[i-1], linewidth=0.8)
    plt.title(f'Polarisation vs Voltage ({placement}, Size {size}, graphe {graph_type}, experience {experience})', fontsize=25)
    plt.xlabel('Voltage', fontsize=25)
    plt.ylabel('Polarisation', fontsize=25)
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=25)
    plt.tick_params(axis='both', labelsize=20)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_type_folder, f"Polarisation_vs_Voltage_{placement}_{size}_{graph_type}_{experience}.png"))
    plt.close()

def plot_pump(data_list, output_type_folder, graph_type):
    plt.figure(figsize=(25, 12.5))
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    for chip_name in enumerate(data_list):
        data = load_interim_data(chip_name, graph_type)
        name, size, placement, experience =chip_name.split("_") 
        plt.plot(data['t'], data['I'], marker='o', label=f"{chip_name} - {graph_type}", 
                        color=colors[i-1], linewidth=0.8)
    plt.title(f'Current vs Time ({placement}, Size {size}, experience {graph_type}, Type {experience})', fontsize=25)
    plt.xlabel('Time', fontsize=25)
    plt.ylabel('Current', fontsize=25)
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=25)
    plt.tick_params(axis='both', labelsize=20)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_type_folder, f"Current_vs_Time_{placement}_{size}_{graph_type}_{experience}.png"))
    plt.close()


def plot_leakage(data_list, experience, placement, size, new_chip_list, output_type_folder, graph_type):
    plt.figure(figsize=(25, 12.5))
    colors = ['blue', 'red', 'green', 'orange', 'purple', 'yellow', 'orange', 'cyan']  # Liste de couleurs pour les courbes
    for i, chip_name in enumerate(new_chip_list):
        data = data_list[i]
        plt.plot(data['AV'], data['AI'], marker='o', label=f"{chip_name} - {graph_type}", 
                        color=colors[i-1], linewidth=0.8)
    plt.title(f'Current vs Voltage ({placement}, Size {size}, experience {graph_type}, Type {experience})', fontsize=25)
    plt.xlabel('Time', fontsize=25)
    plt.ylabel('Current', fontsize=25)
    plt.grid(True)
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=25)
    plt.tick_params(axis='both', labelsize=20)
    # Sauvegarder le plot dans le dossier spécifié avec le titre comme nom de fichier
    plt.savefig(os.path.join(output_type_folder, f"Current_vs_voltage_{placement}_{size}_{graph_type}_{experience}.png"))
    plt.close()