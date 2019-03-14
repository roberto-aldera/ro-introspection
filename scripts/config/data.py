import os

# New paths
INS_LOGS_PATH = os.path.expanduser("~/data/odometry-comparisons/novatel-outputs")
RAW_NOVATEL_PATH = os.path.expanduser("~/data/odometry-comparisons/"
                                      "2018-06-21-16-24-39-long-hanborough-to-ori-V4-radar-leopon-trial-sunny-long-range/"
                                      "novatel-fixed-timestamps/NovAtel_INSPositionVelocityAttitude.monolithic")
NOVATEL_POSE_OUTPUT_PATH = os.path.join(INS_LOGS_PATH, "novatel_generated_poses.monolithic")
FLAT_POSE_OUTPUT_PATH = os.path.join(INS_LOGS_PATH, "flattened_novatel_generated_poses.monolithic")

# Motion estimation parameters
RADAR_RAW_SCAN_MONO = "/Volumes/mrgdatastore6/Logs/Muttley/2019-01-10-12-32-52-radar-oxford-10k/" \
                      "logs/radar/cts350x_103517/2019-01-10-12-32-57/cts350x_raw_scan.monolithic"
DO_VISUALISER = True
RO_OUTPUT_MONO_FOLDER = os.path.expanduser("~/data/odometry-comparisons/ro-outputs")
RO_ODOMETRY_FILENAME = "radar_odometry.monolithic"
DO_SAVE_MONO = True
DO_USE_PRIOR = False
DO_USE_CLASSIFIER_FOR_PRIOR = True
MOTION_PRIOR_TYPE = "NONE"
START_FRAME_IDX = 0

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
