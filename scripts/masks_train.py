import settings
from masks import label


def main():
    # produce polar images and masks
    label(settings.TRAIN_RADAR_CONFIG_MONO_PATH,
          settings.TRAIN_FRAMES_DIR,
          settings.TRAIN_FRAME_SKIP,
          settings.TRAIN_POSE_CSV_FILE,
          settings.TRAIN_POLAR_IMAGES_DIR,
          settings.TRAIN_MASKS_GT_DIR,
          settings.TRAIN_HISTOGRAMS_DIR,
          settings.PRODUCE_HISTOGRAM_LABELS)


if __name__ == "__main__":
    main()
