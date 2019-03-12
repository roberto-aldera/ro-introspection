import fs_utils
import settings
import tools

from PIL import Image

import polar_cart_transf as pct

from torchvision import transforms as tfs
import torch


def reset():
    fs_utils.empty_delete(settings.GT_POLAR_VIEWER_FRAMES_DIR)
    fs_utils.empty_delete(settings.GT_CART_VIEWER_FRAMES_DIR)
    fs_utils.empty_delete(settings.PRED_POLAR_VIEWER_FRAMES_DIR)
    fs_utils.empty_delete(settings.PRED_CART_VIEWER_FRAMES_DIR)


def viewer_frames(
        device,
        polar_to_cartesian,
        frame,
        mask,
        polar_viewer_frame_file,
        cart_viewer_frame_file):
    # perform color composition
    polar_viewer_frame = torch.zeros(
        1, 3, settings.NUM_AZI_MSGS, settings.CROP_NUM_BINS).to(device)
    polar_viewer_frame[:, 1, :, :] = frame[0, 0, :, 0:settings.CROP_NUM_BINS]
    polar_viewer_frame[:, 0, :, :] = mask[0, 0, :, 0:settings.CROP_NUM_BINS]

    # save polar viewer frame
    print("writing polar_viewer_frame_file: " + polar_viewer_frame_file)
    tfs.ToPILImage()(
        polar_viewer_frame.reshape(
            3,
            settings.NUM_AZI_MSGS,
            settings.CROP_NUM_BINS).to("cpu")).save(polar_viewer_frame_file)

    # transform to cartesian image
    cart_viewer_frame = polar_to_cartesian(polar_viewer_frame)

    # save cartesian image
    print("writing cart_viewer_frame_file: " + cart_viewer_frame_file)
    tfs.ToPILImage()(
        cart_viewer_frame.reshape(
            3,
            settings.CROP_NUM_BINS,
            settings.CROP_NUM_BINS).to("cpu")).save(cart_viewer_frame_file)


def main():
    print("make_labeller_video is starting...")

    # clear labels
    reset()

    # gpu device
    device = tools.get_device()

    # p2c
    polar_to_cartesian = pct.P2C(cart_shape=settings.CROP_NUM_BINS).to(device)

    # get original data, groundtruth, and predicted masks
    frame_files = fs_utils.get_frame_files()
    non_blurred_files = fs_utils.get_non_blurred_files()
    predict_files = fs_utils.get_predict_files()
    assert len(frame_files) == len(non_blurred_files)
    assert len(frame_files) == len(predict_files)

    # iterate frame/mask
    for i, frame_file, non_blurred_file, predict_file in zip(
            range(len(frame_files)), frame_files, non_blurred_files, predict_files):
        # check triplet
        print("processing scan " + str(i))
        fs_utils.check_timestamps(frame_file, non_blurred_file)
        fs_utils.check_timestamps(frame_file, predict_file)

        # read images and convert to tensors
        frame = tfs.ToTensor()(Image.open(frame_file)).reshape(
            1, 1, settings.NUM_AZI_MSGS, settings.NUM_BINS).to(device)
        non_blurred = tfs.ToTensor()(Image.open(non_blurred_file)).reshape(
            1, 1, settings.NUM_AZI_MSGS, settings.NUM_BINS).to(device)
        predict = tfs.ToTensor()(Image.open(predict_file)).reshape(
            1, 1, settings.NUM_AZI_MSGS, settings.NUM_BINS).to(device)

        # prepare and save viewer frames
        # TODO: parallelise
        viewer_frames(
            device,
            polar_to_cartesian,
            frame,
            non_blurred,
            fs_utils.get_gt_polar_viewer_frame_file(frame_file),
            fs_utils.get_gt_cart_viewer_frame_file(frame_file))
        viewer_frames(
            device,
            polar_to_cartesian,
            frame,
            predict,
            fs_utils.get_pred_polar_viewer_frame_file(frame_file),
            fs_utils.get_pred_cart_viewer_frame_file(frame_file))

    print("make_labeller_video is finished!")


if __name__ == "__main__":
    main()
