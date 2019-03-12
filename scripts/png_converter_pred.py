from png_converter import convert
import settings


def main():
    convert(settings.CONVERTED_PRED_DIR,
            settings.MASKED_PRED_DIR,
            settings.UNET_RADAR_MONO_PATH,
            settings.UNET_RADAR_MONO_INDEX_PATH)


if __name__ == "__main__":
    main()
