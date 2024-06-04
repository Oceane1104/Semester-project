# Plot settings
TITLE = "prl_4mar01 (FE)"
FOLDER = "TEST 3\\10-10x10"
#Evolution of DE1FE5x8 with 450°C from 5V to 30V for 200µm capacitor

TITLE_ADD_SIZE = True
TITLE_ADD_AREA = False
TITLE_ADD_GRAPH = True

LABEL_NAME = False
LABEL_GRAPH = False
LABEL_PLAC = True
LABEL_EXP = False
LABEL_GEO = False
LABEL_NB_EXP = []   # put =[] if you want to show all parameters (works only if LABEL_EXP=True)
                    # put for example =[1,0] if you want to show the first process param but not the second

SIZE_TITLE = 25
SIZE_AXIS = 25
SIZE_GRADUATION = 20
SIZE_PLOTS = (25, 12.5)
#(25, 12.5)
#(50, 25)
SIZE_LINE = 0.8
SIZE_LABELS = 25
BOX_PLACE = (0.01, 0.95)
LOC_PLACE = "upper left"
#En haut à gauche: "upper left" et (0.01, 0.95)
#En bas à gauche: "lower left" et (0.01, 0.05)

#m, μ, n, p  ------ not implemented yet
UNIT_X = "m"
UNIT_Y = 1

PARALLEL_CAPAS = True
INTEGRAL = False

# Choose experience
SELECTED_CHIPS = []
SELECTED_EXPERIENCES = ["FE"]
SELECTED_GEOMETRIES =  ["10-10x10"]
SELECTED_PLACEMENTS = []

# --> moyenne ?

# Choose graphes ! several at once
GRAPHES_TO_PLOT = ["P-V 1V_1#1","P-V 2V_1#1","P-V 3V_1#1", "P-V 4V_1#1","P-V 1V_2#1","P-V 2V_2#1","P-V 3V_2#1", 
                  "P-V 4V_2#1","P-V 5V_1#1", "PUND 5V_1#1", "P-V 7V_1#1", 
                  "P-V 10V_1#1","PUND 7V_1#1","PUND 10V_1#1", "IV 3V_1#1", "CV 3V_1#1", "IV 5V_1#1", "CV 5V_1#1"]
#GRAPHES_TO_PLOT = ["P-V 15V_1#1"]

SHOW_PLOTS = False # put False if you don't want to show all plots during plot generation

# Choose results to plot
RESULTS_TO_PLOT = []
RESULTS_X_AXIS = "parameter x"
RESULTS_LABELS = ""

SPECIAL = False
SPECIAL_EXPERIENCES = []
SPECIAL_GEOMETRIES = ["200"]
SPECIAL_PLACEMENT = ["s1-a1"]

SPECIAL_PLOT = ["P-V 5V_1#1", "P-V 7V_1#1", "P-V 8V_1#1", "P-V 10V_1#1", "P-V 12V_1#1", "P-V 14V_1#1", "P-V 15V_1#1", 
                  "P-V 17V_1#1", "P-V 18V_1#1","P-V 19V_1#1", "P-V 20V_1#1", "P-V 21V_1#1", "P-V 22V_1#1", "P-V 23V_1#1", 
                  "P-V 24V_1#1", "P-V 25V_1#1", "P-V 28V_1#1", "P-V 29V_1#1", "P-V 30V_1#1","P-V 32V_1#1"]
SPECIAL_CHIPS =  ["ml4apr06"] * len(SPECIAL_PLOT)

#Need same length * len(SPECIAL_PLOT)
# "ml4apr01",
#"P-V 7V_1#1",

PLOT_RESULT_ENERGY = False
ELECTRIC_FIELD = True
CHIP_RESULT_ENERGY = ["ml4may07", "ml4apr01"]
THICKNESS = [20, 20]

PLOT_RESULT_MEAN = False
