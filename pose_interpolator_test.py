import pose_interpolator
import settings


def main():
    pose_interpolator.interpolate_pose(settings.TEST_POSE_DIR,
                                       settings.TEST_RELATIVE_POSES_PATH,
                                       settings.TEST_POSE_CSV_FILE,
                                       settings.TEST_FRAMES_DIR)


if __name__ == "__main__":
    main()
