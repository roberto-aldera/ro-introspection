import monolithic_converter
import settings


def main():
    monolithic_converter.convert_monolithic(
        settings.TRAIN_RADAR_MONO_PATH,
        settings.TRAIN_RADAR_MONO_INDEX_PATH,
        settings.TRAIN_FRAMES_DIR,
        settings.TRAIN_START_FRAME_IND,
        settings.TRAIN_NUM_FRAMES * settings.TRAIN_FRAME_SKIP,
        1)


if __name__ == "__main__":
    main()
