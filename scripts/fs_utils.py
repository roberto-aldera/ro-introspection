import settings
from config.data import *

import os
import shutil
from glob import glob


# TODO: move subdirectory names from settings.py here


def get_model_path():
    # TODO: choose model with best prediction accuracy automatically
    model_paths = glob(settings.MODELS_DIR + "/models/*")
    return max(model_paths, key=os.path.getctime)


def get_jit_model_path():
    return os.path.join(settings.DEPLOY_DIR, "model.pt")


def delete(directory):
    shutil.rmtree(directory, ignore_errors=True)


def empty_delete(directory):
    if os.path.exists(directory):
        delete(directory)
    os.makedirs(directory)


def make_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return False
    return True


def delete_if_exists(file):
    if os.path.exists(file):
        os.remove(file)


def glob_sort_files(directory, extension):
    files = glob(directory + "/*." + extension)
    return sorted(files)


def get_png_files(directory):
    return glob_sort_files(directory, "png")


def get_csv_files(directory):
    return glob_sort_files(directory, "csv")


def get_mask_files():
    return get_png_files(settings.TRAIN_MASKS_GT_DIR)


def get_polar_image_files():
    return get_png_files(settings.TRAIN_POLAR_IMAGES_DIR)


def get_frame_files():
    return get_png_files(settings.TEST_POLAR_IMAGES_DIR)


def get_predict_files():
    return get_png_files(settings.MASKS_PRED_DIR)


def get_non_blurred_files():
    return get_png_files(settings.TEST_MASKS_GT_DIR)


def get_histogram_files():
    return get_png_files(settings.TEST_HISTOGRAMS_DIR)


def get_masked_file(frame_file, ext):
    return frame_file.replace("/polar_images", "/masked_" + ext)


def get_gt_polar_viewer_frame_file(frame_file):
    return frame_file.replace("/polar_images", "/polar_viewer_frames_gt")


def get_gt_cart_viewer_frame_file(frame_file):
    return frame_file.replace("/polar_images", "/cart_viewer_frames_gt")


def get_pred_polar_viewer_frame_file(frame_file):
    return frame_file.replace("/polar_images", "/polar_viewer_frames_pred")


def get_pred_cart_viewer_frame_file(frame_file):
    return frame_file.replace("/polar_images", "/cart_viewer_frames_pred")


def check_timestamps(left, right):
    # TODO: check foray as well
    assert os.path.splitext(
        os.path.basename(
            left))[0] == os.path.splitext(
        os.path.basename(
            right))[0]


def get_timestamps(directory):
    polar_image_files = get_png_files(directory)
    return [int(os.path.splitext(
        os.path.basename(
            polar_image_file))[0]) for polar_image_file in polar_image_files]


def get_file(comparison, job_id):
    if comparison in ["speed", "pose", "yaw_rate"]:
        if job_id == D1:
            return settings.RO_TARGET_MOTION_ESTIMATIONS_LM_PATH
        elif job_id == D2:
            return settings.UNET_TARGET_MOTION_ESTIMATIONS_LM_PATH
        elif job_id == GT:
            return settings.GT_TARGET_MOTION_ESTIMATIONS_LM_PATH
        elif job_id == "moos":
            return settings.MOOS_TARGET_MOTION_ESTIMATIONS_LM_PATH
        elif job_id == "gpu":
            return settings.GPU_TARGET_MOTION_ESTIMATIONS_LM_PATH
        elif job_id == "VO":
            return settings.TEST_RELATIVE_POSES_PATH
    elif comparison == "timing":
        if job_id == D1:
            return settings.RO_MOTION_ESTIMATE_TIMING_FILE
        elif job_id == D2:
            return settings.UNET_MOTION_ESTIMATE_TIMING_FILE
        elif job_id == GT:
            return settings.GT_MOTION_ESTIMATE_TIMING_FILE
        elif job_id == "moos":
            return settings.MOOS_MOTION_ESTIMATE_TIMING_FILE
        elif job_id == "gpu":
            return settings.GPU_MOTION_ESTIMATE_TIMING_FILE
    elif comparison == "landmarks_detected":
        if job_id == D1:
            return settings.RO_LANDMARK_POINTCLOUDS_MONOLITHIC
        elif job_id == D2:
            return settings.UNET_LANDMARK_POINTCLOUDS_MONOLITHIC
        elif job_id == GT:
            return settings.GT_LANDMARK_POINTCLOUDS_MONOLITHIC
        elif job_id == "moos":
            return settings.MOOS_LANDMARK_POINTCLOUDS_MONOLITHIC
        elif job_id == "gpu":
            return settings.GPU_LANDMARK_POINTCLOUDS_MONOLITHIC
    elif comparison == "matches_discovered":
        if job_id == D1:
            return settings.RO_MATCHES_DISCOVERED_FILE
        elif job_id == D2:
            return settings.UNET_MATCHES_DISCOVERED_FILE
        elif job_id == GT:
            return settings.GT_MATCHES_DISCOVERED_FILE
        elif job_id == "moos":
            return settings.MOOS_MATCHES_DISCOVERED_FILE
        elif job_id == "gpu":
            return settings.GPU_MATCHES_DISCOVERED_FILE
    raise IOError("check comparison and job id!")


def get_fig_file(comparison):
    if comparison == "speed":
        fig_file = settings.SPEED_FIG_FILE
    elif comparison == "yaw_rate":
        fig_file = settings.YAW_RATE_FIG_FILE
    elif comparison == "pose":
        fig_file = settings.POSE_FIG_FILE
    elif comparison == "timing":
        fig_file = settings.TIMING_FIG_FILE
    elif comparison == "landmarks_detected":
        fig_file = settings.LANDMARKS_DETECTED_FIG_FILE
    elif comparison == "dropped_landmarks":
        fig_file = settings.DROPPED_LANDMARKS_FIG_FILE
    elif comparison == "matches_discovered":
        fig_file = settings.MATCHES_DISCOVERED_FIG_FILE
    else:
        raise IOError("check comparison!")
    return fig_file.replace(".pdf", "_" +
                            str(settings.RES_MIN) +
                            "_" +
                            str(settings.RES_MAX) +
                            ".pdf")
