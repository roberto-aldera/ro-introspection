import os

# data to run
D1 = "standard-ro"
D2 = "enhanced-ro"

# which data to use
TRAINING_DATA_IDX = 0
TESTING_DATA_IDX = 0

# platform
PLATFORM = "Muttley"
PLATFORM_CONFIG_PATH = os.path.expanduser(
    "~/code/corelibs/src/platform-configurations/"
    "robotcar/2018-04-25-10-00-00/final_platform_config.xml")

# data store
DSTORE = "mrgdatastore5"

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
    {  # cloudy
        "foray": "2017-08-21-10-48-51-oxford-10k-with-radar-2",
        "radar_log_datestamp": "2017-08-21-09-48-53",
        "odom_log_datestamp": "2017-08-21-09-48-52",
        "start_frame_ind": 50,
        "num_frames": 7200
    },
    {  # rain
        "foray": "2017-09-08-11-32-38-oxford-10k-with-radar-rain",
        "radar_log_datestamp": "2017-09-08-10-32-41",
        "odom_log_datestamp": "2017-09-08-10-32-39",
        "start_frame_ind": 50,
        "num_frames": 7900
    },
    {  # night
        "foray": "2017-08-22-22-53-02-oxford-10k-with-radar-night-4",
        "radar_log_datestamp": "2017-08-22-21-53-04",
        "odom_log_datestamp": "2017-08-22-21-53-03",
        "start_frame_ind": 25,
        "num_frames": 5400
    }
]
