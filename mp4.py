import fs_utils
import settings

import subprocess


def reset():
    fs_utils.empty_delete(settings.VIDS_DIR)


def get_ffmpeg_cmd(viewer_frames_dir, mp4_file):
    return "ffmpeg " + \
           " -framerate " + str(settings.FRAME_RATE) + \
           " -pattern_type glob -i \"" + viewer_frames_dir + "/*.png\" " + \
           "-vcodec h264 " + \
           mp4_file


if __name__ == "__main__":
    # clear videos
    reset()

    # collect processes
    pids = []

    # gt polar video
    pids.append(
        subprocess.Popen(
            get_ffmpeg_cmd(
                settings.GT_POLAR_VIEWER_FRAMES_DIR,
                settings.GT_POLAR_MP4_FILE),
            shell=True))

    # gt cartesian video
    pids.append(
        subprocess.Popen(
            get_ffmpeg_cmd(
                settings.GT_CART_VIEWER_FRAMES_DIR,
                settings.GT_CART_MP4_FILE),
            shell=True))

    # pred polar video
    pids.append(
        subprocess.Popen(
            get_ffmpeg_cmd(
                settings.PRED_POLAR_VIEWER_FRAMES_DIR,
                settings.PRED_POLAR_MP4_FILE),
            shell=True))

    # pred cartesian video
    pids.append(
        subprocess.Popen(
            get_ffmpeg_cmd(
                settings.PRED_CART_VIEWER_FRAMES_DIR,
                settings.PRED_CART_MP4_FILE),
            shell=True))

    # pred histogram video
    if settings.PRODUCE_HISTOGRAM_VID:
        pids.append(
            subprocess.Popen(
                get_ffmpeg_cmd(
                    settings.TEST_HISTOGRAMS_DIR,
                    settings.HISTOGRAM_MP4_FILE),
                shell=True))

    # wait on video preparation tasks to finish
    for pid in pids:
        pid.wait()
