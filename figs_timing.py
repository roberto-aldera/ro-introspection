from figs import plot
import settings
import dsp


# TODO: all plot functions should return summarising statistic


def plot_timing(job_id,
                motion_estimate_timing_file):
    timestamps = dsp.read_one_column_CSV_file(
        motion_estimate_timing_file, col=0, type=int)
    ellapsed_milliseconds = dsp.read_one_column_CSV_file(
        motion_estimate_timing_file, col=1, type=float)
    # TODO: why is first reading a large spike?
    return timestamps[1:], ellapsed_milliseconds[1:], timestamps[1:]


def main():
    plot("timing", plot_timing, "Time [s]", "Time [ms]")


if __name__ == "__main__":
    main()
