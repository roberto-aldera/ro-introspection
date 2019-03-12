from figs import plot
import motion


def plot_pose(job_id,
              target_motion_estimations_lm_path):
    se3s, timestamps = motion.read_motion_estimates(
        target_motion_estimations_lm_path)
    poses = motion.get_poses(se3s, job_id)
    x, y = motion.get_xy(poses)
    return x, y, timestamps


def main():
    plot("pose", plot_pose, "Displacement [m]", "Displacement [m]",
         shift_x_axis=False, scale_x_axis=False, square=True)


if __name__ == "__main__":
    main()
