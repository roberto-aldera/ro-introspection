import sys
import os

# apps
mrg_viewer_app = os.path.expanduser(
    "~/code/corelibs/build/mrg-viewer/bin/mrg_viewer")
# motion_estimation_raw_navtech_one_step_app = os.path.expanduser(
#     "~/code/radar/radar-utilities/build/bin/MotionEstimation")
# compare_radar_scans_app = os.path.expanduser(
#     "~/code/radar/radar-utilities/build/bin/CompareRadarScans")
monolithic_index_builder_app = os.path.expanduser(
    "~/code/corelibs/build/tools-cpp/bin/MonolithicIndexBuilder")
# unet_dir = os.path.expanduser(
#     "~/code/vizard/radar-unet/src/unet")
# png_converter_app = os.path.expanduser(
#     "~/code/vizard/radar-unet/build/bin/PNGConverter")
# monolithic_converter_app = os.path.expanduser(
#     "~/code/vizard/radar-unet/build/bin/MonolithicConverter")
# unet_live_app = os.path.expanduser(
#     "~/code/vizard/radar-unet/build/bin/UNetLive")
monolithic_player_console_app = os.path.expanduser(
    "~/code/corelibs/build/tools-cpp/bin/MonolithicPlayerConsole")
image_log_player_qt_app = os.path.expanduser(
    "~/code/gau/tools-qt/build/bin/ImageLogPlayerQt")
monolithic_index_info_app = os.path.expanduser(
    "~/code/corelibs/build/tools-cpp/bin/MonolithicIndexInfo")
moos_app = os.path.expanduser(
    "~/code/corelibs/build/core-moos/bin/MOOSDB")
vo_app = os.path.expanduser(
    "~/code/vo/build/bin/ConsoleVO")


# paths
def set_sys_paths():
    sys.path.append(os.path.expanduser("~/code/corelibs/src/tools-python"))
    sys.path.append(os.path.expanduser("~/code/corelibs/build/datatypes"))
    sys.path.append(os.path.expanduser(
        "~/code/corelibs/build/datatypes/datatypes_python"))
