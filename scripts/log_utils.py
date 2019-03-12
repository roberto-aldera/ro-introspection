import module
module.set_sys_paths()

from mrg.logging import IndexedMonolithic

import fs_utils
import settings

import subprocess


def get_start_frame_ind():
    return IndexedMonolithic(
        settings.TEST_RADAR_MONO_PATH).timestamps.index(
        fs_utils.get_timestamps(
            settings.TEST_POLAR_IMAGES_DIR)[0])


def get_num_frames():
    return IndexedMonolithic(
        settings.TEST_RADAR_MONO_PATH).timestamps.index(
        fs_utils.get_timestamps(
            settings.TEST_POLAR_IMAGES_DIR)[-1]) - get_start_frame_ind()


def get_monolithic_index_builder_cmd(mono_path, mono_index_path):
    monolithic_index_builder_cmd = module.monolithic_index_builder_app
    monolithic_index_builder_cmd += " --overwrite"
    monolithic_index_builder_cmd += " --logtostderr"
    monolithic_index_builder_cmd += " -i " + mono_path
    monolithic_index_builder_cmd += " -o " + mono_index_path
    return monolithic_index_builder_cmd


def index(mono_path, mono_index_path):
    monolithic_index_builder_cmd = get_monolithic_index_builder_cmd(
        mono_path, mono_index_path)
    subprocess.Popen(monolithic_index_builder_cmd, shell=True).wait()
