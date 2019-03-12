# python path
import module

module.set_sys_paths()

# std includes
import subprocess
import os

# custom includes
import settings


def play():
    # path for player
    # TODO: to fs_utils.py
    path = os.path.join(
        settings.LOGS,
        settings.TEST_FORAY, "logs",
        "radar")

    # monolithic player
    # TODO: set start/end timestamps
    # TODO: filter out all except scan file
    # TODO: set realistic playback delay
    monolithic_player_console_cmd = module.monolithic_player_console_app + \
        " --moos_host " + settings.MOOS_HOST + \
        " --moos_port " + str(settings.MOOS_PORT) + \
        " --path " + path + \
        " --logtostderr"

    # run player
    subprocess.Popen(monolithic_player_console_cmd, shell=True).wait()


def main():
    play()


if __name__ == "__main__":
    main()
