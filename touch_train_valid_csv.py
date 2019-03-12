import settings
import fs_utils

if __name__ == "__main__":
    fs_utils.make_if_not_exists(settings.MODELS_DIR)
    with open(settings.TRAIN_VALID_CSV, 'w'):
        pass
