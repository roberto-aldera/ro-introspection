import settings
from masks import label


def main():
    # produce frames and gt masks
    label(settings.TEST_RADAR_CONFIG_MONO_PATH,
          settings.TEST_FRAMES_DIR,
          1,
          settings.TEST_POSE_CSV_FILE,
          settings.TEST_POLAR_IMAGES_DIR,
          settings.TEST_MASKS_GT_DIR,
          settings.TEST_HISTOGRAMS_DIR,
          settings.PRODUCE_HISTOGRAM_VID)


if __name__ == "__main__":
    main()
