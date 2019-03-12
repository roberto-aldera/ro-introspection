# python path
import module

module.set_sys_paths()

# std includes
import subprocess

# custom includes
import settings
import fs_utils


def reset():
    fs_utils.empty_delete(settings.LIVE_CV_DIR)


def live():
    # clear live images
    reset()

    # monolithic listener
    unet_live_cmd = module.unet_live_app + \
        " --host_name " + settings.MOOS_HOST + \
        " --host_port " + str(settings.MOOS_PORT) + \
        " --input_raw_scan_channel " + settings.INPUT_RAW_SCAN_CHANNEL + \
        " --output_raw_scan_channel " + settings.OUTPUT_RAW_SCAN_CHANNEL + \
        " --jit_model_path " + fs_utils.get_jit_model_path() + \
        " --num_azi_msgs " + str(settings.NUM_AZI_MSGS) + \
        " --num_bins " + str(settings.NUM_BINS) + \
        " --output_dir " + settings.LIVE_CV_DIR + \
        " --logtostderr"

    # run player
    subprocess.Popen(unet_live_cmd, shell=True).wait()


def main():
    live()


if __name__ == "__main__":
    main()
