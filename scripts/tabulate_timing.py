from tabulate import add_to_table
from figs_timing import plot_timing
import settings

if __name__ == "__main__":
    add_to_table("timing", plot_timing)
