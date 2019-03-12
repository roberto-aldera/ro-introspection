import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as fcts


class C2P(nn.Module):
    def __init__(self, polar_shape=[400, 1000]):
        super(C2P, self).__init__()

        i = np.linspace(-1, 1, polar_shape[1])
        j = np.linspace(-1, 1, polar_shape[0])

        I, J = np.meshgrid(i, j)
        I = torch.from_numpy(I).float() / 2 + 0.5
        J = np.pi * (torch.from_numpy(J).float() + 0.5)

        X = I * torch.cos(J)
        self.X = X.reshape([1, polar_shape[0], polar_shape[1], 1]).float()

        Y = I * torch.sin(J)
        self.Y = Y.reshape([1, polar_shape[0], polar_shape[1], 1]).float()

        self.grid = nn.Parameter(torch.cat([self.X, self.Y], 3).float())

    def forward(self, x):
        return fcts.grid_sample(x, self.grid)


class P2C(nn.Module):
    def __init__(self, cart_shape=1000):
        super(P2C, self).__init__()

        i = np.linspace(-1, 1, cart_shape)
        j = np.linspace(-1, 1, cart_shape)

        I, J = np.meshgrid(i, j)
        I = torch.from_numpy(I).float()
        J = torch.from_numpy(J).float()

        # negative to flip
        A = -torch.atan2(I, J) / np.pi
        self.A = A.reshape([1, cart_shape, cart_shape, 1]).float()

        R = torch.sqrt(I ** 2 + J ** 2)
        R /= torch.max(R) / np.sqrt(2)
        R = 2 * R - 1
        self.R = R.reshape([1, cart_shape, cart_shape, 1]).float()

        self.grid = nn.Parameter(torch.cat([self.R, self.A], 3).float())

    def forward(self, x):
        return fcts.grid_sample(x, self.grid)
