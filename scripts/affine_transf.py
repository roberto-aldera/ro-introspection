import PIL.Image as img

import numpy as np

import torch
from torchvision import transforms as tfs
import torch.nn as nn
import torch.nn.functional as fcts


class AFF(nn.Module):
    def __init__(self, theta, img_shape=[1000, 1000]):
        super(AFF, self).__init__()

        self.grid = fcts.affine_grid(
            theta, torch.Size(
                (1, 1, img_shape[0], img_shape[1])))

    def forward(self, x):
        return fcts.grid_sample(x, self.grid)
