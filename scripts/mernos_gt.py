import settings
import mernos


def main():
    # TODO: replay_until time doesn't exactly match ro.py
    mernos.motion_estimation(
        settings.GT_OUTPUT_DIR,
        settings.GT_RADAR_MONO_PATH,
        0,
        -1)


if __name__ == "__main__":
    main()
