# python path
import module

# std includes
import subprocess

# custom includes
import settings
import fs_utils


def board():
    # board
    logs_dir = settings.MODELS_DIR + "/logs/tb_logs"
    tensorboard_cmd = "tensorboard " + \
        " --logdir " + logs_dir + \
        " --port 6006"

    # run player
    subprocess.Popen(tensorboard_cmd, shell=True).wait()


def main():
    board()


if __name__ == "__main__":
    main()
