# paths
import module

module.set_sys_paths()

# std includes
import os
import time

# 3rd party includes
import numpy as np
import torch
from torchvision import transforms as tfs
from PIL import Image

# custom includes
import settings
import affine_transf as at
import polar_cart_transf as pct
import fs_utils
import tools

# mrg includes
from mrg.transform.conversions import build_se3_transform, se3_to_components
from mrg.logging import IndexedMonolithic


def reset(polar_images_dir,
          masks_dir,
          histograms_dir,
          produce_histograms):
    fs_utils.empty_delete(polar_images_dir)
    fs_utils.empty_delete(masks_dir)
    fs_utils.empty_delete(histograms_dir)
    if not produce_histograms:
        fs_utils.delete(histograms_dir)


# TODO: produce masks in parallel


def label(radar_config_mono_path,
          frames_dir,
          frame_skip,
          pose_csv_file,
          polar_images_dir,
          masks_dir,
          histograms_dir,
          produce_histograms):
    # clear polar images and masks and histograms
    reset(polar_images_dir,
          masks_dir,
          histograms_dir,
          produce_histograms)

    # set up pose interpolator
    print(
        "getting poses from pose_csv_file: " +
        pose_csv_file)
    rel_poses = []
    # TODO: use timestamp lookup for rel poses
    # TODO: use monolithic not CSV
    with open(pose_csv_file, "r") as file_handle:
        for line in file_handle:
            split = line.strip("\n").split(",")
            xyzrpy = [
                float(
                    split[0]), float(
                    split[1]), float(
                    split[2]), float(
                    split[3]), float(
                    split[4]), float(
                    split[5])]
            rel_pose = build_se3_transform(xyzrpy)
            rel_poses.append(rel_pose)
    print("got num_rel_poses: " + str(len(rel_poses)))

    # gpu device
    device = tools.get_device()

    # polar-cartesian converters
    polar_to_cartesian = pct.P2C(cart_shape=settings.NUM_BINS).to(device)
    cartesian_to_polar = pct.C2P(
        polar_shape=[
            settings.NUM_AZI_MSGS,
            settings.NUM_BINS]).to(device)

    # read bin_size_metres from config
    bin_size_metres = IndexedMonolithic(radar_config_mono_path)[
        0][0].bin_size_or_resolution * 0.0001

    # unit conversions
    F = 1. / (bin_size_metres * settings.NUM_BINS)
    THETA = settings.STATIC_YAW_OFFSET * np.pi / 180.

    # window rotation
    AFF = at.AFF(torch.Tensor([[[np.cos(-THETA),
                                 np.sin(-THETA),
                                 0],
                                [-np.sin(-THETA),
                                 np.cos(-THETA),
                                 0]]]).to(device),
                 img_shape=[settings.NUM_BINS,
                            settings.NUM_BINS]).to(device)

    # timestamps to interpolate for pose at
    polar_image_files = fs_utils.get_png_files(frames_dir)
    TIMESTAMPS = fs_utils.get_timestamps(frames_dir)
    num_frames = len(TIMESTAMPS)
    print("got num_frames: " + str(num_frames))
    assert len(rel_poses) == num_frames - 1
    print("got num_frames: " + str(num_frames))

    # iterate frame windows
    time_diffs = []
    # TODO: one frame too few
    for i in range(0, num_frames - 1, frame_skip):
        # measure start time
        print("processing scan with timestamp: " + str(TIMESTAMPS[i]))
        start_time = time.time()

        # work out which scans should be used for labelling by
        # applying motion constraint
        lin_motion = 0.0
        ang_motion = 0.0

        # window, one anchor will not necessarily share window frames with the
        # next
        timestamps = []
        polar_images = []

        # anchored poses
        anchored_relative_poses = []
        anchored_relative_pose = np.identity(4)

        # reverse iterator to get spaced out frames for window anchored from
        # this point
        for j in range(i, 0, -1):
            # apply motion constraint, this frame should be first in window
            if j == i or lin_motion > settings.LIN_MOTION_THRESHOLD or ang_motion > settings.ANG_MOTION_THRESHOLD:
                # reset accumulated incremental motion
                lin_motion = 0.0
                ang_motion = 0.0

                # get timestamp
                timestamp = TIMESTAMPS[j]

                # get polar image file
                polar_image_file = polar_image_files[j]

                # get polar image and convert to PIL
                polar_image = Image.open(polar_image_file)

                # get dimensions
                _, height = polar_image.size
                assert settings.NUM_AZI_MSGS == height

                # convert to tensor and pad if necessary
                polar_image = tfs.ToTensor()(polar_image).reshape(
                    1, 1, settings.NUM_AZI_MSGS, settings.NUM_BINS).to(device)

                # save window vars
                timestamps.append(timestamp)
                polar_images.append(polar_image)
                anchored_relative_poses.append(anchored_relative_pose)

            # interpolate for relative pose between each scan
            # TODO: check this index
            rel_pose = rel_poses[j]
            rel_xyzrpy = se3_to_components(rel_pose)
            anchored_relative_pose = rel_pose * anchored_relative_pose

            # update distance travelled
            # TODO: check that motion should be backwards and not forwards
            lin_motion += np.linalg.norm(rel_xyzrpy[0:2])
            ang_motion += rel_xyzrpy[5]

            # pop scan from front of window
            if len(polar_images) == settings.WINDOW_SIZE:
                # check window vars
                assert len(anchored_relative_poses) == settings.WINDOW_SIZE
                assert len(timestamps) == settings.WINDOW_SIZE
                assert len(polar_images) == settings.WINDOW_SIZE
                assert len(anchored_relative_poses) == settings.WINDOW_SIZE

                # start populating histogram
                histogram = torch.zeros(
                    settings.WINDOW_SIZE,
                    1,
                    settings.NUM_BINS,
                    settings.NUM_BINS).to(device)

                # iterate window scans
                for k in range(settings.WINDOW_SIZE):
                    # get and adapt window scans
                    polar_image = polar_images[k]

                    # transform to cartesian image
                    cartesian_img = polar_to_cartesian(polar_image)

                    # get pose of robot wrt to start of window
                    anchored_relative_pose = anchored_relative_poses[k]

                    # project onto ground plane
                    xyzrpy = se3_to_components(anchored_relative_pose)

                    # scale
                    x = xyzrpy[0] * F
                    y = xyzrpy[1] * F
                    theta = THETA - xyzrpy[5]

                    # rotate into vo frame
                    r = torch.Tensor([[np.cos(theta), np.sin(theta)],
                                      [-np.sin(theta), np.cos(theta)]]).to(device)
                    v = torch.Tensor([x, y]).reshape(2, 1).to(device)
                    mvmt = torch.cat((r, r.mm(v)), 1).reshape(1, 2, 3)

                    # prepare affine transformation
                    aff = at.AFF(
                        mvmt,
                        img_shape=[
                            settings.NUM_BINS,
                            settings.NUM_BINS]).to(device)

                    # apply affine
                    cartesian_img = aff(cartesian_img)

                    # store
                    histogram[k] = AFF(cartesian_img)

                # save rgb histogram
                # TODO: what happens when histogram has more than 3 channels?
                # massively slows down pipeline on 2000 bins
                if produce_histograms:
                    histogram_file = os.path.join(
                        histograms_dir,
                        str(timestamps[0]) + ".png")
                    print("saving histogram_file: " + histogram_file)
                    tfs.ToPILImage()(
                        histogram.reshape(
                            settings.WINDOW_SIZE,
                            settings.NUM_BINS,
                            settings.NUM_BINS).to("cpu")).save(histogram_file)

                # collapse for labels
                cartesian_mask = histogram.sum(0)
                cartesian_mask -= torch.min(
                    cartesian_mask[cartesian_mask != 0])
                cartesian_mask /= torch.max(cartesian_mask)

                # apply thresholds
                cartesian_mask[cartesian_mask >
                               settings.HISTOGRAM_THRESHOLD] = 1
                cartesian_mask[cartesian_mask < 1] = 0

                # get polar mask
                polar_mask = cartesian_to_polar(
                    cartesian_mask.reshape(
                        1, 1, settings.NUM_BINS, settings.NUM_BINS))
                polar_mask[polar_mask > settings.LABEL_THRESHOLD] = 1

                # save polar image
                polar_image_file = os.path.join(
                    polar_images_dir,
                    str(timestamps[0]) + ".png")
                print("saving polar_image_file: " + polar_image_file)
                tfs.ToPILImage()(
                    (polar_images[0]).reshape(
                        1,
                        settings.NUM_AZI_MSGS,
                        settings.NUM_BINS).to("cpu")).save(polar_image_file)

                # save polar mask
                mask_file = os.path.join(
                    masks_dir,
                    str(timestamps[0]) + ".png")
                print("saving mask_file: " + mask_file)
                tfs.ToPILImage()(
                    polar_mask.reshape(
                        1,
                        settings.NUM_AZI_MSGS,
                        settings.NUM_BINS).to("cpu")).save(mask_file)

                # stop backwards search, start to produce mask for next frame
                break

        # TODO: hard throw in PoseInterpolator for no movement before this

        # measure time ellapsed
        stop_time = time.time()
        time_diff = stop_time - start_time
        time_diffs.append(time_diff)
        ave_time_diff = np.mean(time_diffs)
        remaining = ave_time_diff * (num_frames - 1 - i) / frame_skip
        print("mask write rate (s): " +
              str(time_diff) +
              ", average (s): " +
              str(ave_time_diff) + ", remaining (s): " + str(remaining))

    # total time ellapsed
    print("total time ellapsed (s): " +
          str(np.sum(time_diffs)))
