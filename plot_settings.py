# Plot settings
TITLE = "Energy density for all chip"
FOLDER = "Energy density plot"
#Evolution of DE1FE5x8 with 450°C from 5V to 30V for 200µm capacitor

TITLE_ADD_SIZE = True
TITLE_ADD_GRAPH = True

NAME = False
LABEL_EXP = True
LABEL_NB_EXP = [0, 1, 2]
LABEL_PLAC = False
LABEL_GEO = False
LABEL_GRAPH = False
LABEL = "" # experience? placement? geometrie? true/false
SIZE_TITLE = 50
SIZE_AXIS = 50
SIZE_GRADUATION = 40
SIZE_PLOTS = (25, 12.5)
#(25, 12.5)
#(50, 25)
SIZE_LINE = 5
#0.8 before
SIZE_LABELS = 35
LOC_PLACE = "lower left"
BOX_PLACE = (0.01, 0.4)
BOX_PLACE2 = (0.90, 0.25)
#En haut à gauche: "upper left" et (0.01, 0.95)
#En bas à gauche: "lower left" et (0.01, 0.05)
#En bas à droite: "lower right" et (0.95, 0.05) for energy: (0.98, 0.05)



#m, μ, n, p
UNIT_X = "m"
UNIT_Y = 1

units = ""
INTEGRAL = False
# Choose experience
SELECTED_CHIPS = ["ml4may01","ml4may02", "ml4may03"]
SELECTED_EXPERIENCES = []
SELECTED_GEOMETRIES =  ["100"]
SELECTED_PLACEMENTS = ["s2-a3", "s1-a1"]

# --> moyenne ?

# Choose graphes ! several at once
#GRAPHES_TO_PLOT = ["P-V 1V_2#1","P-V 2V_2#1","P-V 3V_2#1", "P-V 4V_2#1","P-V 5V_1#1", "PUND 5V_1#1", "P-V 7V_1#1", "P-V 10V_1#1",
#                   "PUND 7V_1#1","PUND 10V_1#1", "IV 3V_1#1", "CV 3V_1#1", "IV 5V_1#1", "CV 5V_1#1"]
GRAPHES_TO_PLOT = ["P-V 25V_1#1"]
GRAPH_VOLTAGES = ["1"] # currently not used just enter the complet graph name above

SHOW_PLOTS = True # put False if you don't want to show all plots during plot generation

# Choose results to plot
RESULTS_TO_PLOT = []
RESULTS_X_AXIS = "parameter x"
RESULTS_LABELS = ""

SPECIAL = False
E_F = True
SPECIAL_EXPERIENCES = []
SPECIAL_GEOMETRIES = ["100"]
SPECIAL_PLACEMENT = []
# 
SPECIAL_PLOT = ["P-V 15V_1#1","P-V 29V_1#1", "P-V 15V_1#1","P-V 29V_1#1"]
SPECIAL_CHIPS =  ["ml4may07", "ml4may02", "ml4apr01", "ml4apr06"] 

# "CV 3V_1#1", "CV 6V_1#1", "CV 8V_1#1", "CV 10V_1#1", "CV 11V_1#1", "CV 12V_1#1", "CV 13V_1#1", "CV 14V_1#1",
#                   "CV 15V_1#1", "CV 18V_1#1", "CV 20V_1#1", "CV 22V_1#1", "CV 23V_1#1", "CV 24V_1#1"

#"P-V 29V_1#1", "P-V 15V_1#1","P-V 29V_1#1", "P-V 15V_1#1"
#Need same length * len(SPECIAL_PLOT)
# "ml4apr01",
#"P-V 7V_1#1",

PLOT_RESULT_ENERGY = True
ELECTRIC_FIELD = True
CHIP_RESULT_ENERGY = ["ml4may02", "ml4may07","ml4apr01", "ml4apr06"]
#"ml4may02", "ml4may07","ml4apr01", "ml4apr06"
THICKNESS = {
    'ml4may07': 20,
    'ml4may02': 40,
    'ml4apr01': 20,
    'ml4apr06': 40,
    'ml4may01': 40,
    'ml4may03': 40
}
TABLE_VOLTAGE = {
    'ml4may07': [40],
    'ml4may02': [40, 30, 29],
    'ml4apr01': [40, 15,16],
    'ml4apr06': [40, 29],
    'ml4may01': [40, 30, 29],
    'ml4may03': [40, 30, 29]
}
    

PLOT_RESULT_MEAN = False

SUMMARY = False