import module
import subprocess


def play(bb_mono_path):
    image_log_player_qt_cmd = module.image_log_player_qt_app + \
        " -i " + bb_mono_path
    subprocess.Popen(image_log_player_qt_cmd, shell=True)
