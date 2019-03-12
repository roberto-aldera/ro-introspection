import numpy as np
from numpy import fft
import settings


def read_one_column_CSV_file(csv_file, col=0, type=str):
    column = []
    print("reading CSV file: " + csv_file)
    with open(csv_file, "r") as file_handle:
        for line in file_handle:
            split = line.strip("\n").split(",")
            column.append(split[col])
    return map(type, column)
