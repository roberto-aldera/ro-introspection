import monolithic_converter
import settings


def main():
    monolithic_converter.convert_monolithic(
        settings.TEST_RADAR_MONO_PATH,
        settings.TEST_RADAR_MONO_INDEX_PATH,
        settings.TEST_FRAMES_DIR,
        settings.TEST_START_FRAME_IND,
        settings.TEST_NUM_FRAMES,
        1)


if __name__ == "__main__":
    main()
