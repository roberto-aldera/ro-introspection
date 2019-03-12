import module

module.set_sys_paths()

from figs import plot
import motion
import dsp
import log_utils

from mrg.logging import IndexedMonolithic
from mrg.adaptors.pointcloud import PbSerialisedPointCloudToPython


def plot_landmarks_detected(job_id,
                            landmark_pointclouds_monolithic):
    # produce index
    log_utils.index(
        landmark_pointclouds_monolithic,
        landmark_pointclouds_monolithic +
        ".index")

    # collect samples
    timestamps = []
    landmarks_detected = []

    # open data
    print(
        "opening landmark_pointclouds_monolithic: " +
        landmark_pointclouds_monolithic)
    indexed_monolithic = IndexedMonolithic(landmark_pointclouds_monolithic)

    # iterate pointclouds
    for pb_serialised_pointcloud, _, _ in indexed_monolithic:
        serialised_pointcloud = PbSerialisedPointCloudToPython(
            pb_serialised_pointcloud)
        timestamps.append(serialised_pointcloud.timestamp)
        landmarks_detected.append(len(serialised_pointcloud.get_xyz()))

    return timestamps, landmarks_detected, timestamps


def main():
    plot(
        "landmarks_detected",
        plot_landmarks_detected,
        "Time [s]",
        "Landmarks detected")


if __name__ == "__main__":
    main()
