# Plot settings
TITLE = "FE 10x10um2"
LABEL_EXP = True
LABEL_PLAC = True
LABEL_GEO = True
LABEL = "" # experience? placement? geometrie? true/false
SIZE_TITLE = 25
SIZE_AXIS = 25
SIZE_GRADUATION = 20
SIZE_PLOTS = (25, 12.5)
#(25, 12.5)
SIZE_LINE = 0.8
SIZE_LABELS = 12
BOX_PLACE = (0.01, 0.05)
LOC_PLACE = "lower left"
#"upper left"
#(0.01, 0.95)

#m, μ, n, p
UNIT_X = "m"
UNIT_Y = 1

units = ""

# Choose experience
SELECTED_CHIPS = []
SELECTED_EXPERIENCES = ["FE"]
SELECTED_GEOMETRIES =  ["10-1x1"]
SELECTED_PLACEMENTS = []

# --> moyenne ?

# Choose graphes ! several at once
GRAPHES_TO_PLOT = ["P-V 1V_2#1","P-V 2V_2#1","P-V 3V_2#1", "P-V 4V_2#1","P-V 5V_1#1", "PUND 5V_1#1", "P-V 7V_1#1", "P-V 10V_1#1",
                   "PUND 7V_1#1","PUND 10V_1#1", "IV 3V_1#1", "CV 3V_1#1", "IV 5V_1#1", "CV 5V_1#1"]
GRAPH_VOLTAGES = ["1"] # currently not used just enter the complet graph name above

SHOW_PLOTS = True # put False if you don't want to show all plots during plot generation

# Choose results to plot
RESULTS_TO_PLOT = []
RESULTS_X_AXIS = "parameter x"
RESULTS_LABELS = ""
