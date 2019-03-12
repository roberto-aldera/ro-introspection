# std includes
import subprocess

# custom includes
import module
import settings
import fs_utils


def reset(output_log_folder_path):
    fs_utils.empty_delete(output_log_folder_path)


# TODO: to mernos.py


def get_motion_estimation_cmd(
        output_log_folder_path,
        input_raw_scan_channel,
        app_name):
    return module.motion_estimation_raw_navtech_one_step_app + \
        " --radar_config_mono_path=" + settings.TEST_RADAR_CONFIG_MONO_PATH + \
        " --replay_from_monolithic=0" + \
        " --input_raw_scan_channel=" + input_raw_scan_channel + \
        " --app_name=" + app_name + \
        " --app_host=" + settings.MOOS_HOST + \
        " --app_port=" + str(settings.MOOS_PORT) + \
        " --platform_config_path=" + str(settings.PLATFORM_CONFIG_PATH) + \
        " --output_log_folder_path=" + str(output_log_folder_path) + \
        " --save_mono" + \
        " --overwrite_motion_ests_mono" + \
        " --input_frame=" + settings.INPUT_FRAME + \
        " --visualize_scan_matching=0" + \
        " --des_num_bins=" + str(settings.NUM_BINS) + \
        " --identity_correction=" + str(settings.IDENTITY_CORRECTION) + \
        " --alsologtostderr"


def listen(output_log_folder_path, input_raw_scan_channel, app_name):
    # clear motion estimation outputs
    reset(output_log_folder_path)

    # run motion estimator with moos inputs
    motion_estimation_cmd = get_motion_estimation_cmd(
        output_log_folder_path, input_raw_scan_channel, app_name)
    subprocess.Popen(motion_estimation_cmd, shell=True).wait()
