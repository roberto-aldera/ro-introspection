from tabulate import add_to_table
from figs_yaw_rate import plot_yaw_rate
import settings

if __name__ == "__main__":
    add_to_table("yaw_rate", plot_yaw_rate)
