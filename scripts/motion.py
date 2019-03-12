import module
import settings

module.set_sys_paths()

from mrg.logging import MonolithicDecoder
from mrg.adaptors.transform import PbSerialisedTransformToPython
from mrg.transform.conversions import se3_to_components, build_se3_transform

import numpy as np

SE3_ALIGNMENT = build_se3_transform(
    [0, 0, 0, 0, 0, -settings.STATIC_YAW_OFFSET * np.pi / 180.])


def read_motion_estimates(relative_poses_path):
    # open monolithic and iterate frames
    print("reading relative_poses_path: " + relative_poses_path)
    monolithic_decoder = MonolithicDecoder(
        relative_poses_path)

    # iterate mono
    se3s = []
    timestamps = []
    for pb_serialised_transform, _, _ in monolithic_decoder:
        # adapt
        serialised_transform = PbSerialisedTransformToPython(
            pb_serialised_transform)
        se3s.append(serialised_transform[0])
        timestamps.append(serialised_transform[1])

    # TODO: why is first reading a large spike?
    return se3s[1:], timestamps[1:]


def get_poses(se3s, job_id):
    poses = []
    pose = np.identity(
        4) * SE3_ALIGNMENT if job_id != "VO" else np.identity(4)
    for i in range(len(se3s)):
        pose = pose * se3s[i]
        poses.append(pose)
    return poses


def get_xy(poses):
    x = [pose[0, 3] for pose in poses]
    y = [pose[1, 3] for pose in poses]
    return x, y


def get_distance_travelled(se3s):
    distance_travelled = 0.0
    for se3 in se3s:
        translation = se3[0:2, -1]
        incremental_distance = np.linalg.norm(translation)
        distance_travelled += incremental_distance
    return distance_travelled

# TODO: refactor get_speeds and get_yaw_rates


def get_speeds(se3s, timestamps):
    assert len(se3s) == len(timestamps)
    speeds = []
    TIMESTAMPS = []
    for i in range(len(timestamps) - 1):
        # work out speed
        delta_time = timestamps[i + 1] / settings.TIMESTAMP_CONVERSION \
            - timestamps[i] / settings.TIMESTAMP_CONVERSION
        se3 = se3s[i]
        translation = se3[0:2, -1]
        incremental_distance = np.linalg.norm(translation)
        speed = incremental_distance / delta_time
        speeds.append(speed)
        TIMESTAMPS.append(timestamps[i])
    return speeds, TIMESTAMPS


# TODO: divide by zero (delta_time) in get_speeds and get_yaw_rates


def get_yaw_rates(timestamps, se3s):
    assert len(se3s) == len(timestamps)
    yaw_rates = []
    TIMESTAMPS = []
    for i in range(len(timestamps) - 1):
        # work out yaw_rate
        delta_time = timestamps[i + 1] / settings.TIMESTAMP_CONVERSION  \
            - timestamps[i] / settings.TIMESTAMP_CONVERSION
        se3 = se3s[i]
        xyzrpy = se3_to_components(se3)
        yaw_rate = xyzrpy[-1] / delta_time
        yaw_rates.append(yaw_rate)
        TIMESTAMPS.append(timestamps[i])
    return yaw_rates, TIMESTAMPS
