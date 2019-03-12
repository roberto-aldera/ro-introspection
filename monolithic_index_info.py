import module
import subprocess


def get_info(radar_mono_index_path):
    monolithic_index_info_cmd = module.monolithic_index_info_app + \
        " --index " + radar_mono_index_path
    subprocess.Popen(monolithic_index_info_cmd, shell=True)
