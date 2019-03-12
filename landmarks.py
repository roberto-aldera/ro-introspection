import module
import subprocess


def landmarks(landmarks_images_monolithic):
    image_log_player_qt_cmd = module.image_log_player_qt_app + \
        " -i " + landmarks_images_monolithic
    subprocess.Popen(image_log_player_qt_cmd, shell=True)
