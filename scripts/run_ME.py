# Running motion estimation for radar

import subprocess
from config.data import *

motion_estimation_app = os.path.expanduser(
    "~/code/radar-utilities/build/bin/MotionEstimation")

motion_estimation_cmd = motion_estimation_app + \
                        " -raw_radar_mono_path " + RADAR_RAW_SCAN_MONO + \
                        " --alsologtostderr" + \
                        " -stderrthreshold " + "1" + \
                        " -radar_motion_estimation_mono_path " + RO_ODOMETRY_FILENAME + \
                        " -output_log_folder_path " + RO_OUTPUT_MONO_FOLDER + \
                        " -visualise_scan_matching=" + str(int(DO_VISUALISER)) + \
                        " -save_mono=" + str(int(DO_SAVE_MONO)) + \
                        " -use_prior=" + str(int(DO_USE_PRIOR)) + \
                        " -use_classifier_for_prior=" + str(int(DO_USE_CLASSIFIER_FOR_PRIOR)) + \
                        " -motion_prior_type=" + MOTION_PRIOR_TYPE + \
                        " -start_frame_ind " + str(START_FRAME_IDX)

print(motion_estimation_cmd)

# run process
print('Running motion estimation from', RADAR_RAW_SCAN_MONO, "to", RO_OUTPUT_MONO_FOLDER)
subprocess.Popen(motion_estimation_cmd, shell=True).wait()
