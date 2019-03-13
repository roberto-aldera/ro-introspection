from apply import apply_masks
import fs_utils
import settings


def main():
    # apply predicted masks
    apply_masks(fs_utils.get_non_blurred_files(), settings.MASKED_GT_DIR, GT)


if __name__ == "__main__":
    main()
