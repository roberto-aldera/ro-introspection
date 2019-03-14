import os

# data to run
D1 = "standard-ro"
D2 = "enhanced-ro"
GT = "ground-truth"
VO = "VO"

# which data to use
TRAINING_DATA_IDX = 0
TESTING_DATA_IDX = 0

# platform
PLATFORM = "Muttley"
PLATFORM_CONFIG_PATH = os.path.expanduser(
    "~/code/corelibs/src/platform-configurations/"
    "robotcar/2018-04-25-10-00-00/final_platform_config.xml")

# data store
DSTORE = "mrgdatastore6"

# scratch
BASE_DIR = "rugged_ro"
BASE_OUTPUT = "dataset-name"

# training data
TRAINING_DATA = [
    {  # sunny
        "foray": "2017-08-18-11-21-04-oxford-10k-with-radar-1",
        "radar_log_datestamp": "2017-08-18-10-21-06",
        "odom_log_datestamp": "2017-08-18-10-21-05",
        "start_frame_ind": 200,
        "frame_skip": 5,
        "num_frames": 1600
    }
]

# testing data
TESTING_DATA = [
    {  # rural RO
        "foray": "2018-06-21-16-24-39-long-hanborough-to-ori-V4-radar-leopon-trial-sunny-long-range",
        "radar_log_datestamp": "2018-06-21-15-24-44",
        "odom_log_datestamp": "2018-06-21-15-24-40",
        "start_frame_ind": 50,
        "num_frames": 7200
    }
]
