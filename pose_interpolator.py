import settings
import fs_utils
import module
import subprocess

import bisect
import numpy as np
import numpy.matlib as ml

import module

module.set_sys_paths()

from mrg.logging import MonolithicDecoder
from mrg.transform.conversions import build_se3_transform, so3_to_quaternion, se3_to_components
from mrg.adaptors.transform import PbSerialisedTransformToPython


def reset(pose_dir):
    fs_utils.empty_delete(pose_dir)


# TODO: fix autopep8 formatting


class PoseInterpolator:
    def __init__(self, vo_path):
        monolithic_decoder = MonolithicDecoder(vo_path)

        vo_timestamps = [0]
        abs_poses = [ml.identity(4)]

        for pb_serialised_transform, _, _ in monolithic_decoder:
            rel_pose, timestamp = PbSerialisedTransformToPython(
                pb_serialised_transform)

            vo_timestamps.append(timestamp)

            abs_pose = abs_poses[-1] * rel_pose
            abs_poses.append(abs_pose)

        self.vo_timestamps = vo_timestamps
        self.abs_poses = abs_poses

    def interp_abs(self,
                   requested_timestamps,
                   origin_timestamp):
        requested_timestamps.insert(0, origin_timestamp)
        requested_timestamps = np.array(requested_timestamps)
        pose_timestamps = np.array(self.vo_timestamps)
        abs_poses = self.abs_poses

        if len(pose_timestamps) != len(abs_poses):
            raise ValueError('Must supply same number of timestamps as poses')

        abs_quaternions = np.zeros((4, len(abs_poses)))
        abs_positions = np.zeros((3, len(abs_poses)))
        for i, pose in enumerate(abs_poses):
            if i > 0 and pose_timestamps[i - 1] >= pose_timestamps[i]:
                raise ValueError('Pose timestamps must be in ascending order')

            abs_quaternions[:, i] = so3_to_quaternion(pose[0:3, 0:3])
            abs_positions[:, i] = np.ravel(pose[0:3, 3])

        upper_indices = [bisect.bisect(pose_timestamps, pt)
                         for pt in requested_timestamps]
        lower_indices = [u - 1 for u in upper_indices]

        if max(upper_indices) >= len(pose_timestamps):
            upper_indices = [min(i, len(pose_timestamps) - 1)
                             for i in upper_indices]

        fractions = (requested_timestamps - pose_timestamps[lower_indices]) / (
            pose_timestamps[upper_indices] - pose_timestamps[lower_indices])

        quaternions_lower = abs_quaternions[:, lower_indices]
        quaternions_upper = abs_quaternions[:, upper_indices]

        d_array = (quaternions_lower * quaternions_upper).sum(0)

        linear_interp_indices = np.nonzero(d_array >= 1)
        sin_interp_indices = np.nonzero(d_array < 1)

        scale0_array = np.zeros(d_array.shape)
        scale1_array = np.zeros(d_array.shape)

        scale0_array[linear_interp_indices] = 1 - \
            fractions[linear_interp_indices]
        scale1_array[linear_interp_indices] = fractions[linear_interp_indices]

        theta_array = np.arccos(np.abs(d_array[sin_interp_indices]))

        scale0_array[sin_interp_indices] = np.sin(
            (1 - fractions[sin_interp_indices]) * theta_array) / np.sin(theta_array)
        scale1_array[sin_interp_indices] = np.sin(
            fractions[sin_interp_indices] * theta_array) / np.sin(theta_array)

        negative_d_indices = np.nonzero(d_array < 0)
        scale1_array[negative_d_indices] = -scale1_array[negative_d_indices]

        quaternions_interp = np.tile(
            scale0_array, (4, 1)) * quaternions_lower + np.tile(
            scale1_array, (4, 1)) * quaternions_upper

        positions_lower = abs_positions[:, lower_indices]
        positions_upper = abs_positions[:, upper_indices]

        positions_interp = np.multiply(
            np.tile(
                (1 - fractions), (3, 1)), positions_lower) + np.multiply(
            np.tile(
                fractions, (3, 1)), positions_upper)

        poses_mat = ml.zeros((4, 4 * len(requested_timestamps)))

        poses_mat[0,
                  0::4] = 1 - 2 * np.square(quaternions_interp[2,
                                                               :]) - 2 * np.square(quaternions_interp[3,
                                                                                                      :])
        poses_mat[0,
                  1::4] = 2 * np.multiply(quaternions_interp[1,
                                                             :],
                                          quaternions_interp[2,
                                                             :]) - 2 * np.multiply(quaternions_interp[3,
                                                                                                      :],
                                                                                   quaternions_interp[0,
                                                                                                      :])
        poses_mat[0,
                  2::4] = 2 * np.multiply(quaternions_interp[1,
                                                             :],
                                          quaternions_interp[3,
                                                             :]) + 2 * np.multiply(quaternions_interp[2,
                                                                                                      :],
                                                                                   quaternions_interp[0,
                                                                                                      :])

        poses_mat[1,
                  0::4] = 2 * np.multiply(quaternions_interp[1,
                                                             :],
                                          quaternions_interp[2,
                                                             :]) + 2 * np.multiply(quaternions_interp[3,
                                                                                                      :],
                                                                                   quaternions_interp[0,
                                                                                                      :])
        poses_mat[1,
                  1::4] = 1 - 2 * np.square(quaternions_interp[1,
                                                               :]) - 2 * np.square(quaternions_interp[3,
                                                                                                      :])
        poses_mat[1,
                  2::4] = 2 * np.multiply(quaternions_interp[2,
                                                             :],
                                          quaternions_interp[3,
                                                             :]) - 2 * np.multiply(quaternions_interp[1,
                                                                                                      :],
                                                                                   quaternions_interp[0,
                                                                                                      :])

        poses_mat[2,
                  0::4] = 2 * np.multiply(quaternions_interp[1,
                                                             :],
                                          quaternions_interp[3,
                                                             :]) - 2 * np.multiply(quaternions_interp[2,
                                                                                                      :],
                                                                                   quaternions_interp[0,
                                                                                                      :])
        poses_mat[2,
                  1::4] = 2 * np.multiply(quaternions_interp[2,
                                                             :],
                                          quaternions_interp[3,
                                                             :]) + 2 * np.multiply(quaternions_interp[1,
                                                                                                      :],
                                                                                   quaternions_interp[0,
                                                                                                      :])
        poses_mat[2,
                  2::4] = 1 - 2 * np.square(quaternions_interp[1,
                                                               :]) - 2 * np.square(quaternions_interp[2,
                                                                                                      :])

        poses_mat[0:3, 3::4] = positions_interp
        poses_mat[3, 3::4] = 1

        poses_mat = np.linalg.solve(poses_mat[0:4, 0:4], poses_mat)

        poses_out = [0] * (len(requested_timestamps) - 1)
        for i in range(1, len(requested_timestamps)):
            poses_out[i - 1] = poses_mat[0:4, i * 4:(i + 1) * 4]

        return poses_out


def interpolate_pose(pose_dir,
                     relative_pose_file,
                     pose_csv_file,
                     frames_dir):
    # reset output
    reset(pose_dir)

    # set up pose interpolator
    pose_interpolator = PoseInterpolator(relative_pose_file)

    # abs pose interpolation
    timestamps = fs_utils.get_timestamps(frames_dir)
    abs_poses = pose_interpolator.interp_abs(timestamps, timestamps[0])

    # get rel poses
    rel_poses = [np.linalg.inv(abs_poses[i]) * abs_poses[i + 1]
                 for i in range(len(abs_poses) - 1)]

    # write poses to CSV
    with open(pose_csv_file, "w") as f:
        for rel_pose in rel_poses:
            xyzrpy = se3_to_components(rel_pose)
            f_string = ",".join(map(str, xyzrpy)) + "\n"
            f.write(f_string)
