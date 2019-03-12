import module
import settings
import fs_utils
import log_utils

import subprocess


def reset(output_dir):
    fs_utils.empty_delete(output_dir)


def get_motion_estimation_cmd(
        radar_mono_path,
        output_dir,
        start_frame_ind,
        num_frames):
    return module.motion_estimation_raw_navtech_one_step_app + \
        " --raw_radar_mono_path=" + settings.TEST_RADAR_MONO_PATH + \
        " --mask_radar_mono_path=" + radar_mono_path + \
        " --radar_config_mono_path=" + settings.TEST_RADAR_CONFIG_MONO_PATH + \
        " --platform_config_path=" + str(settings.PLATFORM_CONFIG_PATH) + \
        " --output_log_folder_path=" + str(output_dir) + \
        " --save_mono" + \
        " --overwrite_motion_ests_mono" + \
        " --input_frame=" + settings.INPUT_FRAME + \
        " --visualise_scan_matching=0" + \
        " --start_frame_ind1=" + str(log_utils.get_start_frame_ind()) + \
        " --num_frames1=" + str(log_utils.get_num_frames()) + \
        " --start_frame_ind2=" + str(start_frame_ind) + \
        " --num_frames2=" + str(num_frames) + \
        " --replay_delay=" + str(settings.REPLAY_DELAY) + \
        " --des_num_bins=" + str(settings.NUM_BINS) + \
        " --identity_correction=" + str(settings.IDENTITY_CORRECTION) + \
        " --alsologtostderr"


def motion_estimation(
        output_dir,
        radar_mono_path,
        start_frame_ind,
        num_frames):
    # clear motion estimation outputs
    reset(output_dir)

    # run motion estimation
    motion_estimation_cmd = get_motion_estimation_cmd(
        radar_mono_path,
        output_dir,
        start_frame_ind,
        num_frames)
    subprocess.Popen(
        motion_estimation_cmd,
        shell=True).wait()
