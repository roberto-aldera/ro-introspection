# std includes
import subprocess
import os
from config.data import *

flatten_pose_chain_app = os.path.expanduser(
    "~/code/corelibs/build/tools-cpp/bin/FlattenPosechain")

flatten_pose_chain_cmd = flatten_pose_chain_app + \
                         " --app_name " + "sdif" + \
                         " --input_type " + "FILE" + \
                         " --file_input_path " + NOVATEL_POSE_OUTPUT_PATH + \
                         " --file_output " + \
                         " --file_output_path " + FLAT_POSE_OUTPUT_PATH

# run process
print('Flattening pose chain from', NOVATEL_POSE_OUTPUT_PATH, 'to', FLAT_POSE_OUTPUT_PATH)
subprocess.Popen(flatten_pose_chain_cmd, shell=True).wait()
