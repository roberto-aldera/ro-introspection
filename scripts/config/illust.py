from data import *

# plot params
GRID_LINE_WIDTH = 0.5
FONT_FAMILY = "serif"
FONT_SIZE = 8
LINE_WIDTH = 1

# colors
COLOR_MAP = {VO: "black",
             D1: "red",
             D2: "blue",
             GT: "green"}

# comparison type
JOB_IDS = [D1,D2]
BASE_FIGS = True
BASE_JOB_ID = GT #VO

# axes
JOB_LEGENDS = True
LABEL_AXES = True

# scaling
TIMESTAMP_CONVERSION = 1e6

# truncate results (percentage)
RES_MIN = 0
RES_MAX = 10

# scientific notation
SCI_NOT_FACT = 1000
