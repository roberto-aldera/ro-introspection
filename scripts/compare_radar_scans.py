import module
import settings
import log_utils

import subprocess

if __name__ == "__main__":
    compare_radar_scans_cmd = module.compare_radar_scans_app + \
        " --raw_radar_mono_path1=" + settings.TEST_RADAR_MONO_PATH + \
        " --raw_radar_mono_path2=" + settings.GT_RADAR_MONO_PATH + \
        " --des_num_bins=" + str(settings.NUM_BINS) + \
        " --start_frame_ind1=" + str(log_utils.get_start_frame_ind()) + \
        " --start_frame_ind2=" + str(0) + \
        " --num_frames1=" + str(log_utils.get_num_frames()) + \
        " --num_frames2=" + str(-1) + \
        " --logtostderr"
    subprocess.Popen(compare_radar_scans_cmd, shell=True).wait()
