import torch
import numpy as np
from tensorboardX import SummaryWriter


class Callback:
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class TensorboardLoggerCallback(Callback):
    def __init__(self, path_to_files):
        self.path_to_files = path_to_files

    def __call__(self, *args, **kwargs):
        if kwargs['step_name'] != "epoch":
            return

        epoch_id = kwargs['epoch_id']

        writer = SummaryWriter(self.path_to_files)
        writer.add_scalar('data/train_loss', kwargs['train_loss'], epoch_id)
        writer.add_scalar(
            'data/train_dice_coeff',
            kwargs['train_dice_coeff'],
            epoch_id)
        writer.add_scalar('data/val_loss', kwargs['val_loss'], epoch_id)
        writer.add_scalar(
            'data/val_dice_coeff',
            kwargs['val_dice_coeff'],
            epoch_id)
        writer.close()


class ModelSaverCallback(Callback):
    def __init__(self, path_to_model, verbose=False):
        self.verbose = verbose
        self.path_to_model = path_to_model
        self.suffix = ""

    def set_suffix(self, suffix):
        self.suffix = suffix

    def __call__(self, *args, **kwargs):
        if kwargs['step_name'] != "train" and kwargs['step_name'] != 'epoch':
            print('mmmmmmmm')
            return

        if kwargs['epoch_id'] % 5 == 0 or kwargs['step_name'] == 'train':
            pth = self.path_to_model + self.suffix + \
                '_epoch' + str(kwargs['epoch_id'])
            net = kwargs['net']
            torch.save(net.state_dict(), pth)

            print("Model saved in {}".format(pth))
