import torch
from torchvision import transforms as tfs
import numpy as np
import settings


class Callback:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class PredictionsSaverCallback(Callback):
    def __init__(
            self,
            to_file,
            origin_img_size,
            threshold,
            rle_threshold, timestamps):
        self.threshold = threshold
        self.rle_threshold = rle_threshold
        self.origin_img_size = origin_img_size
        self.to_file = to_file
        self.index = 0
        self.timestamps = timestamps

    def get_mask_rle(self, prediction):
        mask = prediction > self.rle_threshold
        return mask

    def __call__(self, *args, **kwargs):
        if kwargs["step_name"] != "predict":
            return

        probs = kwargs["probs"]
        files_name = kwargs["files_name"]

        # Save the predictions
        for (pred, name) in zip(probs, files_name):
            rle = torch.tensor(pred)
            tfs.ToPILImage()(
                rle.reshape(
                    1,
                    settings.NUM_AZI_MSGS,
                    settings.NUM_BINS)).point(
                lambda x: 255 if x > self.threshold *
                255 else 0).convert("L").save(
                settings.MASKS_PRED_DIR +
                "/" +
                str(self.timestamps[self.index]) +
                ".png")
            self.index += 1

    def close_saver(self):
        print("Predictions wrote in {} file".format(self.to_file))
