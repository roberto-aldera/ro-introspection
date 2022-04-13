# std includes
import subprocess
import os
from config.data import *

fix_novatel_timestamps_app = os.path.expanduser(
    "~/code/corelibs/build/base-cpp/bin/NovAtelDevice")

fix_novatel_timestamps_cmd = fix_novatel_timestamps_app + \
                         " --recover_timestamps " + \
                         " --read_file " + \
                         " --read_file_path " + RAW_NOVATEL_PACKET_PATH + \
                         " --logdir " + INS_LOGS_PATH + \
                         " --log "

# run process
print('Fixing timestamps for Novatel pose chain from', RAW_NOVATEL_PACKET_PATH, 'to', NOVATEL_POSE_OUTPUT_PATH)
subprocess.Popen(fix_novatel_timestamps_cmd, shell=True).wait()
