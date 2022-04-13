# std includes
import subprocess
import os
from config.data import *

make_pose_chain_app = os.path.expanduser(
    "~/code/geography/build/bin/NovatelINSPositionVelocityAttitudeToPosechain")

make_pose_chain_cmd = make_pose_chain_app + \
                      " --app_name " + "sdif" + \
                      " --input_type " + "FILE" + \
                      " --file_input_path " + RAW_NOVATEL_PATH + \
                      " --file_output " + \
                      " --file_output_path " + NOVATEL_POSE_OUTPUT_PATH

# run process
print('Generating pose chain from', RAW_NOVATEL_PATH, 'to', NOVATEL_POSE_OUTPUT_PATH)
subprocess.Popen(make_pose_chain_cmd, shell=True).wait()
