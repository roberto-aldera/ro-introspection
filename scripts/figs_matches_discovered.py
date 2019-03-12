from figs import plot
import settings
import dsp


def plot_matches_discovered(job_id,
                            matches_discovered_file):
    timestamps = dsp.read_one_column_CSV_file(
        matches_discovered_file, col=0, type=int)
    matches_discovered = dsp.read_one_column_CSV_file(
        matches_discovered_file, col=1, type=int)
    return timestamps, matches_discovered, timestamps


def main():
    plot(
        "matches_discovered",
        plot_matches_discovered,
        "Time [s]",
        "Matches discovered")


if __name__ == "__main__":
    main()
