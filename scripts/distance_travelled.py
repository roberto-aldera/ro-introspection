import settings
import motion


def main():
    se3s, _ = motion.read_motion_estimates(
        settings.RO_TARGET_MOTION_ESTIMATIONS_LM_PATH)
    distance_travelled = motion.get_distance_travelled(se3s)
    print("distance_travelled: " + str(distance_travelled))


if __name__ == "__main__":
    main()
