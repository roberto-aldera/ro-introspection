# python path
import module

module.set_sys_paths()

# std includes
import subprocess

# custom includes
import settings
import fs_utils


def reset():
    fs_utils.empty_delete(settings.LIVE_CV_DIR)


def main():
    # clear live images
    reset()

    # monolithic listener
    moos_cmd = module.moos_app

    # run player
    subprocess.Popen(moos_cmd, shell=True).wait()


if __name__ == "__main__":
    main()
