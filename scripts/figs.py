import settings
import fs_utils
import dsp

import numpy as np
import matplotlib as mpl

mpl.use('TkAgg')
mpl.rcParams['font.size'] = settings.FONT_SIZE
mpl.rcParams['ytick.labelsize'] = 'large'
mpl.rcParams['xtick.labelsize'] = 'large'


def reset(fig_file):
    if not fs_utils.make_if_not_exists(settings.FIG_DIR):
        fs_utils.delete_if_exists(fig_file)


def add_to_plot(plt,
                job_id,
                X_data,
                Y_data,
                scale_x_axis,
                x_axis_scale,
                shift_x_axis):
    # convert and check incoming data
    X_data = np.array(X_data)
    Y_data = np.array(Y_data)
    # assert len(X_data) == len(Y_data)

    # apply truncate
    bottom_x = int(len(X_data) * settings.RES_MIN / 100.)
    top_x = int(len(X_data) * settings.RES_MAX / 100.)
    X_data = X_data[bottom_x:top_x]
    bottom_y = int(len(Y_data) * settings.RES_MIN / 100.)
    top_y = int(len(Y_data) * settings.RES_MAX / 100.)
    Y_data = Y_data[bottom_y:top_y]

    # scale x-axis
    if scale_x_axis:
        X_data = X_data / x_axis_scale

    # shift x-axis
    if shift_x_axis:
        X_data = X_data - np.min(X_data)

    # do plot
    plt.plot(X_data,
             Y_data,
             linewidth=settings.LINE_WIDTH,
             label=job_id, color=settings.COLOR_MAP[job_id])

    return plt


def plot(comparison,
         plot_fn,
         x_label,
         y_label,
         scale_x_axis=True,
         x_axis_scale=settings.TIMESTAMP_CONVERSION,
         shift_x_axis=True,
         square=False):
    print("figs is starting...")

    # output file
    fig_file = fs_utils.get_fig_file(comparison)
    print("got fig_file: " + fig_file)
    reset(fig_file)

    # invisible plot
    import matplotlib.pyplot as plt

    # text
    plt.rc("text", usetex=True)
    plt.rc("font", family=settings.FONT_FAMILY)

    # clipping base data
    min_T = None
    max_T = None

    # iterate jobs
    for job_id in settings.JOB_IDS:
        # job
        file = fs_utils.get_file(
            comparison,
            job_id)

        # some plotting methods require job id for calibration
        X_data, Y_data, T = plot_fn(job_id, file)

        # use first job to clip base data
        if not min_T and not max_T:
            min_T = min(T)
            max_T = max(T)

        # convert data to array
        X_data = np.array(X_data)
        Y_data = np.array(Y_data)

        # add to plot
        plt = add_to_plot(
            plt,
            job_id,
            X_data,
            Y_data,
            scale_x_axis,
            x_axis_scale,
            shift_x_axis)

    # base job data
    if settings.BASE_FIGS:
        try:
            # get base signal
            X_data_base, Y_data_base, T_base = plot_fn(
                settings.BASE_JOB_ID, fs_utils.get_file(
                    comparison, settings.BASE_JOB_ID))

            # truncate base signal
            # TODO: refactor with tabulate.py
            X_interp = [
                x_data_base for x_data_base,
                t in zip(
                    X_data_base,
                    T_base) if t >= min_T and t <= max_T]
            Y_interp = [
                y_data_base for y_data_base,
                t in zip(
                    Y_data_base,
                    T_base) if t >= min_T and t <= max_T]

            # plot base signal
            plt = add_to_plot(
                plt,
                settings.BASE_JOB_ID,
                X_interp,
                Y_interp,
                scale_x_axis,
                x_axis_scale,
                shift_x_axis)
        except BaseException:
            print("no base data!")

    # xlim
    # TODO: automatic xlim/ylim
    if shift_x_axis:
        plt.xlim(left=0)

    # square axes
    # TODO: is this working?
    if square:
        plt.gca().set_aspect('equal', adjustable='box')

    # legend
    if settings.JOB_LEGENDS:
        plt.legend(loc="best", fontsize=settings.FONT_SIZE)

    # axes labels
    if settings.LABEL_AXES:
        plt.xlabel(x_label, fontsize=settings.FONT_SIZE)
        plt.ylabel(y_label, fontsize=settings.FONT_SIZE)

    # grid
    plt.grid(
        color="k",
        linestyle="--",
        linewidth=settings.GRID_LINE_WIDTH)

    # save
    print("saving fig_file: " + fig_file)
    plt.savefig(fig_file, bbox_inches='tight')
    plt.show()
    plt.close()

    print("figs is finished!")
