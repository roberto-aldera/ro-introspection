import pose_interpolator
import settings


def main():
    pose_interpolator.interpolate_pose(
        settings.TRAIN_POSE_DIR,
        settings.TRAIN_RELATIVE_POSES_PATH,
        settings.TRAIN_POSE_CSV_FILE,
        settings.TRAIN_FRAMES_DIR)


if __name__ == "__main__":
    main()
