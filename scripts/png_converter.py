import fs_utils
import settings
import module
import log_utils

import subprocess


def reset(converted_dir):
    fs_utils.empty_delete(converted_dir)


def get_png_converter_cmd(masked_dir, radar_mono_path):
    png_converter_cmd = module.png_converter_app
    png_converter_cmd += " --radar_mono_input_path=" + settings.TEST_RADAR_MONO_PATH
    png_converter_cmd += " --radar_mono_input_index_path=" + \
                         settings.TEST_RADAR_MONO_INDEX_PATH
    png_converter_cmd += " --png_dir_in=" + masked_dir
    png_converter_cmd += " --radar_mono_output_path=" + radar_mono_path
    png_converter_cmd += " --num_bins=" + str(settings.NUM_BINS)
    png_converter_cmd += " --logtostderr"
    return png_converter_cmd


def convert(converted_dir, masked_dir, radar_mono_path, radar_mono_index_path):
    # clear output data
    reset(converted_dir)

    # convert metadata + pngs to monolithic
    png_converter_cmd = get_png_converter_cmd(masked_dir, radar_mono_path)
    subprocess.Popen(png_converter_cmd, shell=True).wait()

    # build index into new monolithic
    log_utils.index(radar_mono_path, radar_mono_index_path)
