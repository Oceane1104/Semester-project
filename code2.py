import pandas as pd
import matplotlib.pyplot as plt


url = "https://docs.google.com/spreadsheets/d/16pNcfR5_Rw4r4JDUJ-Vr5JXtDCX747Yd/edit?usp=drive_link&ouid=113537870160569752188&rtpof=true&sd=true"
url_for_pandas = url.replace("/edit?usp=share_link", "/export?format=xlsx")
df = pd.read_excel(url_for_pandas)



