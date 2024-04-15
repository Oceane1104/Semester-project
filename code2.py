import pandas as pd
import matplotlib.pyplot as plt


#url = "https://docs.google.com/spreadsheets/d/16pNcfR5_Rw4r4JDUJ-Vr5JXtDCX747Yd/edit?usp=drive_link&ouid=113537870160569752188&rtpof=true&sd=true"
#url_for_pandas = url.replace("/edit?usp=share_link", "/export?format=xlsx")
#df = pd.read_excel(url_for_pandas)



# Charger les données depuis le fichier Excel
file_path = 'C:\Documents\EPFL\MA4\Projet_de_semestre/br_100_s1_1a_P-V 1V_1#1.xls'
data = pd.read_excel(file_path, sheet_name='br_100_s1_1a_P-V 1V_1#1.xls') 