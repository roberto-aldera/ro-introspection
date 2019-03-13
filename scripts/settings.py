import os

from config.data import *
from config.illust import *
from config.vids import *
from config.radar import *
from config.moos import *
from config.motion_est import *
from config.unet import *
from config.labeller import *
from config.fs import *
from config.camera import *

# datastore
DATASTORE = os.path.join(MOUNT, DSTORE)
LOGS = os.path.join(DATASTORE, "Logs", PLATFORM)
METALOGS = os.path.join(DATASTORE, "MetaLogs", PLATFORM)

# scratchdata
SCRATCH = LOCAL_FS if OVERRIDE_LOCAL_FS else os.path.join(MOUNT, "ScratchData")
DATA = os.path.join(SCRATCH, BASE_DIR, BASE_OUTPUT)
FIGS_DIR = os.path.join(DATA, "figs")
MODELS_DIR = os.path.join(DATA, "models")
MONO_DIR = os.path.join(DATA, "mono")
MOT_EST_DIR = os.path.join(DATA, "motion_estimation")
ODOM_DIR = os.path.join(DATA, "odom")
PNG_DIR = os.path.join(DATA, "png")
VID_DIR = os.path.join(DATA, "vids")

# find training data
TRAIN_FORAY = TRAINING_DATA[TRAINING_DATA_IDX]["foray"]
TRAIN_RADAR_LOG_DATESTAMP = TRAINING_DATA[TRAINING_DATA_IDX]["radar_log_datestamp"]
TRAIN_ODOM_LOG_DATESTAMP = TRAINING_DATA[TRAINING_DATA_IDX]["odom_log_datestamp"]
TRAIN_START_FRAME_IND = TRAINING_DATA[TRAINING_DATA_IDX]["start_frame_ind"]
TRAIN_FRAME_SKIP = TRAINING_DATA[TRAINING_DATA_IDX]["frame_skip"]
TRAIN_NUM_FRAMES = TRAINING_DATA[TRAINING_DATA_IDX]["num_frames"]

# find testing data
TEST_FORAY = TESTING_DATA[TESTING_DATA_IDX]["foray"]
TEST_RADAR_LOG_DATESTAMP = TESTING_DATA[TESTING_DATA_IDX]["radar_log_datestamp"]
TEST_ODOM_LOG_DATESTAMP = TESTING_DATA[TESTING_DATA_IDX]["odom_log_datestamp"]
TEST_START_FRAME_IND = TESTING_DATA[TESTING_DATA_IDX]["start_frame_ind"]
TEST_NUM_FRAMES = TESTING_DATA[TESTING_DATA_IDX]["num_frames"]

# set up training data
TRAIN_RADAR_CONFIG_MONO_PATH = os.path.join(
    LOGS,
    TRAIN_FORAY, "logs",
    "radar",
    RADAR_ID,
    TRAIN_RADAR_LOG_DATESTAMP,
    "cts350x_config.monolithic")
TRAIN_RADAR_MONO_PATH = os.path.join(
    LOGS,
    TRAIN_FORAY, "logs", "radar", RADAR_ID,
    TRAIN_RADAR_LOG_DATESTAMP,
    "cts350x_raw_scan.monolithic")
TRAIN_RADAR_MONO_INDEX_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TRAIN_FORAY, "logs", "radar", RADAR_ID,
    TRAIN_RADAR_LOG_DATESTAMP,
    "cts350x_raw_scan.monolithic.index")
TRAIN_BB_MONO_PATH = os.path.join(
    LOGS,
    TRAIN_FORAY, "logs", "stereo", CAMERA_ID,
    TRAIN_ODOM_LOG_DATESTAMP,
    "BUMBLEBEE3_IMAGES.monolithic")
TRAIN_BB_MONO_INDEX_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TRAIN_FORAY, "logs", "stereo", CAMERA_ID,
    TRAIN_ODOM_LOG_DATESTAMP,
    "BUMBLEBEE3_IMAGES.monolithic.index")

# set up testing data
TEST_RADAR_CONFIG_MONO_PATH = os.path.join(
    LOGS,
    TEST_FORAY, "logs",
    "radar",
    RADAR_ID,
    TEST_RADAR_LOG_DATESTAMP,
    "cts350x_config.monolithic")
TEST_RADAR_MONO_PATH = os.path.join(
    LOGS,
    TEST_FORAY, "logs",
    "radar",
    RADAR_ID,
    TEST_RADAR_LOG_DATESTAMP,
    "cts350x_raw_scan.monolithic")
TEST_RADAR_MONO_INDEX_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TEST_FORAY, "logs", "radar", RADAR_ID,
    TEST_RADAR_LOG_DATESTAMP,
    "cts350x_raw_scan.monolithic.index")
TEST_BB_MONO_PATH = os.path.join(
    LOGS,
    TEST_FORAY, "logs", "stereo", CAMERA_ID,
    TEST_ODOM_LOG_DATESTAMP,
    "BUMBLEBEE3_IMAGES.monolithic")
TEST_BB_MONO_INDEX_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TEST_FORAY, "logs", "stereo", CAMERA_ID,
    TEST_ODOM_LOG_DATESTAMP,
    "BUMBLEBEE3_IMAGES.monolithic.index")

# plot fs
FIG_DIR = os.path.join(FIGS_DIR, TEST_FORAY)
LANDMARKS_DETECTED_FIG_FILE = os.path.join(FIG_DIR, "landmarks_detected.pdf")
MATCHES_DISCOVERED_FIG_FILE = os.path.join(FIG_DIR, "matches_discovered.pdf")
POSE_FIG_FILE = os.path.join(FIG_DIR, "pose.pdf")
SPEED_FIG_FILE = os.path.join(FIG_DIR, "speed.pdf")
TIMING_FIG_FILE = os.path.join(FIG_DIR, "timing.pdf")
YAW_RATE_FIG_FILE = os.path.join(FIG_DIR, "yaw_rate.pdf")

# pytorch-unet
DEPLOY_DIR = os.path.join(MODELS_DIR, "deploy")
LOG_DIR = os.path.join(MODELS_DIR, "logs")
TRAIN_VALID_CSV = os.path.join(MODELS_DIR, "train_valid.csv")

# predict fs
TEST_MONO_OUTPUT_DIR = os.path.join(MONO_DIR, TEST_FORAY)
CONVERTED_GT_DIR = os.path.join(TEST_MONO_OUTPUT_DIR, "converted_gt")
CONVERTED_PRED_DIR = os.path.join(
    TEST_MONO_OUTPUT_DIR,
    "converted_pred")
GT_RADAR_MONO_PATH = os.path.join(CONVERTED_GT_DIR, "masked.monolithic")
GT_RADAR_MONO_INDEX_PATH = GT_RADAR_MONO_PATH + ".index"
UNET_RADAR_MONO_PATH = os.path.join(CONVERTED_PRED_DIR, "masked.monolithic")
UNET_RADAR_MONO_INDEX_PATH = UNET_RADAR_MONO_PATH + ".index"

# motion estimation
TRAIN_RADAR_UTILS_OUTPUT_DIR = os.path.join(MOT_EST_DIR, TRAIN_FORAY)
TEST_RADAR_UTILS_OUTPUT_DIR = os.path.join(MOT_EST_DIR, TEST_FORAY)

# gpu estimates
GPU_OUTPUT_DIR = os.path.join(TEST_RADAR_UTILS_OUTPUT_DIR, "gpu")
GPU_TARGET_AZI_MSGS_MONOLITHIC_PATH = os.path.join(
    GPU_OUTPUT_DIR, "navtech_scans_as_azi_msgs.monolithic")
GPU_TARGET_LANDMARKS_PATH = os.path.join(
    GPU_OUTPUT_DIR,
    "extracted_landmark_sets.monolithic")
GPU_TARGET_MOTION_ESTIMATIONS_LM_PATH = os.path.join(
    GPU_OUTPUT_DIR, "radar_motion_estimation.monolithic")
GPU_LANDMARK_IMAGES_MONOLITHIC = os.path.join(
    GPU_OUTPUT_DIR, "landmark_images.monolithic")
GPU_MOTION_ESTIMATE_TIMING_FILE = os.path.join(
    GPU_OUTPUT_DIR, "timing.csv")
GPU_LANDMARK_POINTCLOUDS_MONOLITHIC = os.path.join(
    GPU_OUTPUT_DIR, "landmark_pointclouds.monolithic")
GPU_DROPPED_LANDMARKS_FILE = os.path.join(
    GPU_OUTPUT_DIR, "dropped_landmarks.csv")
GPU_MATCHES_DISCOVERED_FILE = os.path.join(
    GPU_OUTPUT_DIR, "matches_discovered.csv")

# gt estimates
GT_OUTPUT_DIR = os.path.join(TEST_RADAR_UTILS_OUTPUT_DIR, GT)
GT_TARGET_AZI_MSGS_MONOLITHIC_PATH = os.path.join(
    GT_OUTPUT_DIR, "navtech_scans_as_azi_msgs.monolithic")
GT_TARGET_LANDMARKS_PATH = os.path.join(
    GT_OUTPUT_DIR,
    "extracted_landmark_sets.monolithic")
GT_TARGET_MOTION_ESTIMATIONS_LM_PATH = os.path.join(
    GT_OUTPUT_DIR, "flattened_novatel_generated_poses.monolithic")
GT_LANDMARK_IMAGES_MONOLITHIC = os.path.join(
    GT_OUTPUT_DIR, "landmark_images.monolithic")
GT_MOTION_ESTIMATE_TIMING_FILE = os.path.join(
    GT_OUTPUT_DIR, "timing.csv")
GT_LANDMARK_POINTCLOUDS_MONOLITHIC = os.path.join(
    GT_OUTPUT_DIR, "landmark_pointclouds.monolithic")
GT_MATCHES_DISCOVERED_FILE = os.path.join(
    GT_OUTPUT_DIR, "matches_discovered.csv")

# moos estimates
MOOS_OUTPUT_DIR = os.path.join(TEST_RADAR_UTILS_OUTPUT_DIR, "moos")
MOOS_TARGET_AZI_MSGS_MONOLITHIC_PATH = os.path.join(
    MOOS_OUTPUT_DIR, "navtech_scans_as_azi_msgs.monolithic")
MOOS_TARGET_LANDMARKS_PATH = os.path.join(
    MOOS_OUTPUT_DIR,
    "extracted_landmark_sets.monolithic")
MOOS_TARGET_MOTION_ESTIMATIONS_LM_PATH = os.path.join(
    MOOS_OUTPUT_DIR, "radar_motion_estimation.monolithic")
MOOS_LANDMARK_IMAGES_MONOLITHIC = os.path.join(
    MOOS_OUTPUT_DIR, "landmark_images.monolithic")
MOOS_MOTION_ESTIMATE_TIMING_FILE = os.path.join(
    MOOS_OUTPUT_DIR, "timing.csv")
MOOS_LANDMARK_POINTCLOUDS_MONOLITHIC = os.path.join(
    MOOS_OUTPUT_DIR, "landmark_pointclouds.monolithic")
MOOS_DROPPED_LANDMARKS_FILE = os.path.join(
    MOOS_OUTPUT_DIR, "dropped_landmarks.csv")
MOOS_MATCHES_DISCOVERED_FILE = os.path.join(
    MOOS_OUTPUT_DIR, "matches_discovered.csv")

# RO estimates
RO_OUTPUT_DIR = os.path.join(TEST_RADAR_UTILS_OUTPUT_DIR, D1)
RO_TARGET_AZI_MSGS_MONOLITHIC_PATH = os.path.join(
    RO_OUTPUT_DIR, "navtech_scans_as_azi_msgs.monolithic")
RO_TARGET_LANDMARKS_PATH = os.path.join(
    RO_OUTPUT_DIR,
    "extracted_landmark_sets.monolithic")
RO_TARGET_MOTION_ESTIMATIONS_LM_PATH = os.path.join(
    RO_OUTPUT_DIR, "radar_motion_estimation.monolithic")
RO_LANDMARK_IMAGES_MONOLITHIC = os.path.join(
    RO_OUTPUT_DIR, "landmark_images.monolithic")
RO_MOTION_ESTIMATE_TIMING_FILE = os.path.join(
    RO_OUTPUT_DIR, "timing.csv")
RO_LANDMARK_POINTCLOUDS_MONOLITHIC = os.path.join(
    RO_OUTPUT_DIR, "landmark_pointclouds.monolithic")
RO_MATCHES_DISCOVERED_FILE = os.path.join(
    RO_OUTPUT_DIR, "matches_discovered.csv")

# unet estimates
UNET_OUTPUT_DIR = os.path.join(TEST_RADAR_UTILS_OUTPUT_DIR, D2)
UNET_TARGET_AZI_MSGS_MONOLITHIC_PATH = os.path.join(
    UNET_OUTPUT_DIR, "navtech_scans_as_azi_msgs.monolithic")
UNET_TARGET_LANDMARKS_PATH = os.path.join(
    UNET_OUTPUT_DIR,
    "extracted_landmark_sets.monolithic")
UNET_TARGET_MOTION_ESTIMATIONS_LM_PATH = os.path.join(
    UNET_OUTPUT_DIR, "radar_motion_estimation.monolithic")
UNET_LANDMARK_IMAGES_MONOLITHIC = os.path.join(
    UNET_OUTPUT_DIR, "landmark_images.monolithic")
UNET_MOTION_ESTIMATE_TIMING_FILE = os.path.join(
    UNET_OUTPUT_DIR, "timing.csv")
UNET_LANDMARK_POINTCLOUDS_MONOLITHIC = os.path.join(
    UNET_OUTPUT_DIR, "landmark_pointclouds.monolithic")
UNET_DROPPED_LANDMARKS_FILE = os.path.join(
    UNET_OUTPUT_DIR, "dropped_landmarks.csv")
UNET_MATCHES_DISCOVERED_FILE = os.path.join(
    UNET_OUTPUT_DIR, "matches_discovered.csv")

# train odom
TRAIN_ODOM_DIR = os.path.join(ODOM_DIR, TRAIN_FORAY)
TRAIN_POSE_DIR = os.path.join(TRAIN_ODOM_DIR, "pose")
TRAIN_POSE_CSV_FILE = os.path.join(TRAIN_POSE_DIR, "pose.csv")
TRAIN_RELATIVE_POSES_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TRAIN_FORAY, "logs", "stereo", CAMERA_ID,
    TRAIN_ODOM_LOG_DATESTAMP,
    "relative_poses.monolithic")
TRAIN_RELATIVE_POSES_INDEX_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TRAIN_FORAY, "logs", "stereo", CAMERA_ID,
    TRAIN_ODOM_LOG_DATESTAMP,
    "relative_poses.monolithic.index")

# test odom dirs
TEST_ODOM_DIR = os.path.join(ODOM_DIR, TEST_FORAY)
TEST_POSE_DIR = os.path.join(TEST_ODOM_DIR, "pose")
TEST_POSE_CSV_FILE = os.path.join(TEST_POSE_DIR, "pose.csv")
TEST_RELATIVE_POSES_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TEST_FORAY, "logs", "stereo", CAMERA_ID,
    TEST_ODOM_LOG_DATESTAMP,
    "relative_poses.monolithic")
TEST_RELATIVE_POSES_INDEX_PATH = os.path.join(
    MOUNT,
    METALOGS,
    TEST_FORAY, "logs", "stereo", CAMERA_ID,
    TEST_ODOM_LOG_DATESTAMP,
    "relative_poses.monolithic.index")

# train-test output dirs
TRAIN_OUTPUT_DIR = os.path.join(PNG_DIR, TRAIN_FORAY)
TEST_OUTPUT_DIR = os.path.join(PNG_DIR, TEST_FORAY)

# train fs
TRAIN_FRAMES_DIR = os.path.join(TRAIN_OUTPUT_DIR, "frames")
TRAIN_HISTOGRAMS_DIR = os.path.join(TRAIN_OUTPUT_DIR, "histograms")
TRAIN_MASKS_GT_DIR = os.path.join(TRAIN_OUTPUT_DIR, "masks_gt")
TRAIN_POLAR_IMAGES_DIR = os.path.join(TRAIN_OUTPUT_DIR, "polar_images")

# test fs
GT_CART_VIEWER_FRAMES_DIR = os.path.join(
    TEST_OUTPUT_DIR, "cart_viewer_frames_gt")
PRED_CART_VIEWER_FRAMES_DIR = os.path.join(
    TEST_OUTPUT_DIR, "cart_viewer_frames_pred")
TEST_FRAMES_DIR = os.path.join(TEST_OUTPUT_DIR, "frames")
TEST_HISTOGRAMS_DIR = os.path.join(TEST_OUTPUT_DIR, "histograms")
LIVE_CV_DIR = os.path.join(TEST_OUTPUT_DIR, "live_cv")
MASKED_GT_DIR = os.path.join(TEST_OUTPUT_DIR, "masked_gt")
MASKED_PRED_DIR = os.path.join(TEST_OUTPUT_DIR, "masked_pred")
TEST_MASKS_GT_DIR = os.path.join(TEST_OUTPUT_DIR, "masks_gt")
MASKS_PRED_DIR = os.path.join(TEST_OUTPUT_DIR, "masks_pred")
TEST_POLAR_IMAGES_DIR = os.path.join(TEST_OUTPUT_DIR, "polar_images")
GT_POLAR_VIEWER_FRAMES_DIR = os.path.join(
    TEST_OUTPUT_DIR, "polar_viewer_frames_gt")
PRED_POLAR_VIEWER_FRAMES_DIR = os.path.join(
    TEST_OUTPUT_DIR, "polar_viewer_frames_pred")

# vid fs
VIDS_DIR = os.path.join(VID_DIR, TEST_FORAY)
GT_CART_MP4_FILE = os.path.join(VIDS_DIR, "cart_gt.mp4")
PRED_CART_MP4_FILE = os.path.join(VIDS_DIR, "cart_pred.mp4")
HISTOGRAM_MP4_FILE = os.path.join(VIDS_DIR, "histogram.mp4")
GT_POLAR_MP4_FILE = os.path.join(VIDS_DIR, "polar_gt.mp4")
PRED_POLAR_MP4_FILE = os.path.join(VIDS_DIR, "polar_pred.mp4")
