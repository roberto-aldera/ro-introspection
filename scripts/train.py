import classifier as nnclassifier
import model
import helpers
from train_callbacks import TensorboardLoggerCallback, ModelSaverCallback
from utils import *
import random
import torch
import settings
import fs_utils
import tools


def reset():
    # TODO: to fs_utils.py
    fs_utils.empty_delete(settings.MODELS_DIR + "/models")
    fs_utils.empty_delete(settings.MODELS_DIR + "/logs")


def main():
    reset()

    # set up gpu
    device = tools.get_device()

    # set up model
    net = model.UNet1024(
        (1, settings.NUM_AZI_MSGS, settings.NUM_BINS))
    classifier = nnclassifier.CarvanaClassifier(net, settings.EPOCHS, device)

    # read dataset
    dataset = []
    with open(settings.TRAIN_VALID_CSV) as file_handle:
        for line in file_handle:
            dataset.append(line.strip().split(","))

    # shuffle dataset
    # TODO: shuffle dataset in between epochs?
    if settings.SHUFFLE_DATASET:
        dataset = random.sample(dataset, len(dataset))

    # split dataset
    # TODO: don't load all images into memory before network needs them
    split_pt = int(settings.TRAIN_VALID_SPLIT * len(dataset))
    train_dataset, valid_dataset = create_dataset(dataset, [split_pt])

    # set up data loaders
    print(
        "training dataset: {} samples, test dataset: {} samples".format(
            len(train_dataset),
            len(valid_dataset)))
    data_loaders = {
        "train": torch.utils.data.DataLoader(
            train_dataset,
            batch_size=settings.BATCH_SIZE,
            shuffle=settings.SHUFFLE_BATCHES,
            num_workers=settings.NUM_WORKERS,
            collate_fn=Augmentator()),
        "valid": torch.utils.data.DataLoader(
            valid_dataset,
            batch_size=settings.BATCH_SIZE,
            shuffle=settings.SHUFFLE_BATCHES,
            num_workers=settings.NUM_WORKERS,
            collate_fn=Augmentator())}

    # log callback
    tb_logs_cb = TensorboardLoggerCallback(
        settings.MODELS_DIR + "/logs/tb_logs")

    # model saving callback
    model_saver_cb = ModelSaverCallback(
        settings.MODELS_DIR + "/models/model_" +
        helpers.get_model_timestamp(),
        verbose=True)

    # set up optimiser
    optimiser = torch.optim.RMSprop(
        net.parameters(), lr=settings.LEARNING_RATE)

    # train model
    # TODO: get tensorboard working, with vis callback
    classifier.train(data_loaders["train"],
                     data_loaders["valid"],
                     optimiser,
                     settings.EPOCHS,
                     callbacks=[
                         tb_logs_cb,
                         model_saver_cb])


if __name__ == "__main__":
    main()
