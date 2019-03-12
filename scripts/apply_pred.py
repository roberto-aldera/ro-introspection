from apply import apply_masks
import fs_utils
import settings


def main():
    # apply predicted masks
    apply_masks(fs_utils.get_predict_files(), settings.MASKED_PRED_DIR, "pred")


if __name__ == "__main__":
    main()
