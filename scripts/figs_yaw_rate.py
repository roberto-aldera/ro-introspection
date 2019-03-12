from figs import plot
import motion


def plot_yaw_rate(job_id,
                  target_motion_estimations_lm_path):
    se3s, timestamps = motion.read_motion_estimates(
        target_motion_estimations_lm_path)
    yaw_rates, timestamps = motion.get_yaw_rates(timestamps, se3s)
    return timestamps, yaw_rates, timestamps[1:]


def main():
    plot("yaw_rate", plot_yaw_rate, "Time [s]", "Yaw rate [rad/s]")


if __name__ == "__main__":
    main()
