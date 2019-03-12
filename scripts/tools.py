import torch
import settings


def get_device():
    if settings.DEVICE is not 'cpu' and not torch.cuda.is_available():
        print('No GPU available -> fallback to cpu')
        settings.DEVICE = 'cpu'
    DEVICE = torch.device(settings.DEVICE)
    print("Running on {}".format(settings.DEVICE))
    return DEVICE


def get_learning_rate(optimizer):
    lr = []
    for param_group in optimizer.param_groups:
        lr += [param_group['lr']]
    return lr


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
