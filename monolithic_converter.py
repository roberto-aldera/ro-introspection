import settings
import fs_utils
import module
import subprocess


def reset(png_dir_out):
    fs_utils.empty_delete(png_dir_out)


def get_monolithic_converter_cmd(radar_mono_input_path,
                                 radar_mono_input_index_path,
                                 png_dir_out,
                                 start_frame_ind,
                                 num_frames,
                                 frame_skip):
    return module.monolithic_converter_app + \
        " --radar_mono_input_path=" + radar_mono_input_path + \
        " --radar_mono_input_index_path=" + radar_mono_input_index_path + \
        " --png_dir_out=" + png_dir_out + \
        " --start_frame_ind=" + str(start_frame_ind) + \
        " --num_frames=" + str(num_frames) + \
        " --frame_skip=" + str(frame_skip) + \
        " --num_azi_msgs=" + str(settings.NUM_AZI_MSGS) + \
        " --num_bins=" + str(settings.NUM_BINS) + \
        " --logtostderr"


def convert_monolithic(radar_mono_input_path,
                       radar_mono_input_index_path,
                       png_dir_out,
                       start_frame_ind,
                       num_frames,
                       frame_skip):
    # reset output
    reset(png_dir_out)

    # run monolithic converter
    monolithic_converter_cmd = get_monolithic_converter_cmd(
        radar_mono_input_path,
        radar_mono_input_index_path,
        png_dir_out,
        start_frame_ind,
        num_frames,
        frame_skip)
    subprocess.Popen(monolithic_converter_cmd, shell=True).wait()
