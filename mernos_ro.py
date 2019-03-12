import settings
import log_utils
import mernos


def main():
    mernos.motion_estimation(
        settings.RO_OUTPUT_DIR,
        settings.TEST_RADAR_MONO_PATH,
        log_utils.get_start_frame_ind(),
        log_utils.get_num_frames())


if __name__ == "__main__":
    main()
