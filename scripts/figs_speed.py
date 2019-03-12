from figs import plot
import motion


def plot_speed(job_id,
               target_motion_estimations_lm_path):
    se3s, timestamps = motion.read_motion_estimates(
        target_motion_estimations_lm_path)
    speeds, timestamps = motion.get_speeds(se3s, timestamps)
    return timestamps, speeds, timestamps


def main():
    plot("speed", plot_speed, "Time [s]", "Translational speed [m/s]")


if __name__ == "__main__":
    main()
