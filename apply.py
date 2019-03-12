import settings
import fs_utils
import tools

from PIL import Image
from torchvision import transforms as tfs


def reset(masked_dir):
    fs_utils.empty_delete(masked_dir)


def apply_masks(mask_files, masked_dir, ext):
    # reset output
    reset(masked_dir)

    # gpu device
    device = tools.get_device()

    print("got num_mask_files: " + str(len(mask_files)))

    # get frame files
    frame_files = fs_utils.get_frame_files()
    print("got num_frame_files: " + str(len(frame_files)))
    assert len(mask_files) == len(frame_files)

    # iterate frame-predict pairs
    for frame_file, mask_file in zip(frame_files, mask_files):
        # read original frame data
        print("reading frame_file: " + frame_file)
        frame = tfs.ToTensor()(Image.open(frame_file)).reshape(
            1, 1, settings.NUM_AZI_MSGS, settings.NUM_BINS).to(device)

        # read predicted mask data
        print("reading mask_file: " + mask_file)
        predict = tfs.ToTensor()(Image.open(mask_file)).reshape(
            1, 1, settings.NUM_AZI_MSGS, settings.NUM_BINS).to(device)

        # apply mask
        masked = frame * predict

        # save masked image
        masked_file = fs_utils.get_masked_file(frame_file, ext)
        print("writing masked_file: " + masked_file)
        tfs.ToPILImage()(
            masked.reshape(
                1,
                settings.NUM_AZI_MSGS,
                settings.NUM_BINS).to("cpu")).save(masked_file)
