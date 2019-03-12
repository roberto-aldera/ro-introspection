import classifier as nnclassifier
import model
from test_callbacks import PredictionsSaverCallback
from utils import *
import torch
import settings
import fs_utils
import train
import time
import tools
from glob import glob
import os


def reset():
    fs_utils.empty_delete(settings.MASKS_PRED_DIR)


def main():
    reset()

    # get original polar images
    frame_files = fs_utils.get_frame_files()
    non_blurred_files = fs_utils.get_non_blurred_files()
    print("got num_frame_files: " +
          str(len(frame_files)) +
          ", num_non_blurred_files: " +
          str(len(non_blurred_files)))
    assert len(frame_files) == len(non_blurred_files)
    dataset = zip(non_blurred_files, frame_files)

    # create dataset
    test_dataset = create_dataset(dataset, None)[0]
    dataloaders = {
        "test": torch.utils.data.DataLoader(
            test_dataset,
            batch_size=1,
            num_workers=settings.NUM_WORKERS)}

    # callback
    timestamps = fs_utils.get_timestamps(settings.TEST_POLAR_IMAGES_DIR)
    # TODO: get timestamp within prediction saver callback
    pred_saver_cb = PredictionsSaverCallback(
        settings.MODELS_DIR +
        "/submit.csv.gz",
        (settings.NUM_AZI_MSGS,
         settings.NUM_BINS),
        settings.TEST_CALLBACK_THRESHOLD,
        settings.TEST_RLE_THRESHOLD, timestamps)

    # set up gpu
    device = tools.get_device()

    # set up model
    net = model.UNet1024(
        (1, settings.NUM_AZI_MSGS, settings.NUM_BINS))
    classifier = nnclassifier.CarvanaClassifier(net, 1, device)

    # get model path
    model_path = fs_utils.get_model_path()

    # restore trained weights
    print("restoring model_path: " + model_path)
    classifier.restore_model(model_path)
    classifier.net = classifier.net.to(device)

    # do predictions
    start_time = time.time()
    classifier.predict(dataloaders["test"],
                       callbacks=[pred_saver_cb])

    # measure prediction time
    # TODO: get dice coefficient/loss from predictions
    stop_time = time.time()
    print("finished predictions with rate: " +
          str(len(frame_files) / (stop_time - start_time)) + " frames/second")


if __name__ == "__main__":
    main()
