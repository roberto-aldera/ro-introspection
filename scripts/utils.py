import torch
from torchvision import transforms
import settings
import random
from PIL import Image as img
import fs_utils


def create_dataset(
        dataset,
        splits=None,
        imsize=(
            settings.NUM_AZI_MSGS,
            settings.NUM_BINS)):
    if splits is None:
        splits = [len(dataset)]

    datasets = [dataset[:splits[0]]]
    for s1, s2 in zip(splits[:-1], splits[1:]):
        datasets.append(dataset[s1:s2])

    if not splits[-1] == len(dataset):
        datasets.append(dataset[splits[-1]:])

    preprocess = transforms.Compose([
        transforms.ToTensor(),
    ])

    img1Tensors = []
    img2Tensors = []
    for ds in datasets:

        im1s = []
        im2s = []
        for d in ds:
            print(d[0] + " -> " + d[1])

            # check pair
            fs_utils.check_timestamps(d[0], d[1])

            img_label = img.open(d[0]).convert('L')
            img_original = img.open(d[1]).convert('L')

            im1s.append(preprocess(img_original))
            im2s.append(preprocess(img_label))

        lds = len(im1s)
        img1Tensors.append(
            torch.cat(im1s).reshape(
                lds, 1, imsize[0], imsize[1]))
        img2Tensors.append(
            torch.cat(im2s).reshape(
                lds, 1, imsize[0], imsize[1]))

    datasets = [
        torch.utils.data.dataset.TensorDataset(
            img1Tensors[i],
            img2Tensors[i]) for i in range(
            len(datasets))]
    return datasets


# TODO: parameters to settings
class Augmentator(object):
    def __init__(self):
        pass

    def process(self, img, lbl):

        if settings.DO_AUGMENTATION:

            img += torch.rand_like(img) / 100

            if random.random() > settings.AUGMENTATION_THRESHOLD:
                img = img.flip(1)
                lbl = lbl.flip(1)

        return img, lbl

    def __call__(self, batch):
        imgs, labels = zip(*batch)
        imgs = list(imgs)
        labels = list(labels)

        for i in range(len(imgs)):
            imgs[i], labels[i] = self.process(imgs[i], labels[i])

        imgs = torch.stack(imgs)
        labels = torch.stack(labels)

        return (imgs, labels)
