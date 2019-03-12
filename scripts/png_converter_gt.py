from png_converter import convert
import settings


def main():
    convert(settings.CONVERTED_GT_DIR,
            settings.MASKED_GT_DIR,
            settings.GT_RADAR_MONO_PATH,
            settings.GT_RADAR_MONO_INDEX_PATH)


if __name__ == "__main__":
    main()
