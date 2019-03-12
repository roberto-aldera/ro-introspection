import settings
import fs_utils
import model

import os
from glob import glob

import torch


def reset():
    fs_utils.empty_delete(settings.DEPLOY_DIR)


def main():
    reset()

    # get model path
    model_path = fs_utils.get_model_path()

    # set up model
    net = model.UNet1024(
        (1, settings.NUM_AZI_MSGS, settings.NUM_BINS))

    # load pre-trained weights
    net.load_state_dict(torch.load(model_path))

    # dummy input
    example = torch.randn(1,
                          1, settings.NUM_AZI_MSGS, settings.NUM_BINS,
                          requires_grad=True)

    # Use torch.jit.trace to generate a torch.jit.ScriptModule via tracing.
    traced_script_module = torch.jit.trace(net, example)

    # exported path
    jit_model_path = fs_utils.get_jit_model_path()

    # export
    traced_script_module.save(jit_model_path)


if __name__ == "__main__":
    main()
