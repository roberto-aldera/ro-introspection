import fs_utils
import settings

import csv


def reset():
    fs_utils.make_if_not_exists(settings.MODELS_DIR)


def write_train_test_csv(polar_image_files, mask_files):
    img_mask_pairs = zip(mask_files, polar_image_files)
    print("preparing TRAIN_VALID_CSV: " + settings.TRAIN_VALID_CSV)
    with open(settings.TRAIN_VALID_CSV, "a") as f:
        writer = csv.writer(f)
        writer.writerows(img_mask_pairs)


def main():
    # clear outputs
    reset()

    # generate masks from csv data
    mask_files = fs_utils.get_mask_files()

    # resized polar (preprocessing for training)
    polar_image_files = fs_utils.get_polar_image_files()

    assert len(polar_image_files) == len(mask_files)

    # write training pairs to csvs
    write_train_test_csv(polar_image_files, mask_files)


if __name__ == "__main__":
    main()
