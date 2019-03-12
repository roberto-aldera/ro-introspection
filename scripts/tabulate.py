import module

module.set_sys_paths()

import fs_utils
import settings

import numpy as np


def add_to_table(comparison, plot_fn):
    print("tabulate is starting...")

    # base job data
    X_data_base, Y_data_base = None, None
    try:
        X_data_base, Y_data_base = plot_fn(
            settings.BASE_JOB_ID, fs_utils.get_file(
                comparison, settings.BASE_JOB_ID))
    except BaseException:
        print("no base data!")

    # iterate job IDS
    for job_id in settings.JOB_IDS:
        # get data file
        file = fs_utils.get_file(
            comparison,
            job_id)

        # summarise data
        X_data, Y_data = plot_fn(job_id, file)

        # if there was base data
        if X_data_base and Y_data_base:
            # clip data for comparison
            assert len(Y_data_base) > len(Y_data)
            min_x_data = np.min(X_data)
            max_x_data = np.max(X_data)
            X_interp = [
                x_data_base for x_data_base,
                _ in zip(
                    X_data_base,
                    Y_data_base) if x_data_base >= min_x_data and x_data_base <= max_x_data]
            Y_interp = [
                y_data_base for x_data_base,
                y_data_base in zip(
                    X_data_base,
                    Y_data_base) if x_data_base >= min_x_data and x_data_base <= max_x_data]

            # compare data
            Y_err = np.abs(np.subtract(
                np.interp(X_interp, X_data, Y_data), Y_interp))
            median_Y_err = np.median(Y_err)

            # show comparison
            raw_input(median_Y_err * settings.SCI_NOT_FACT)
        else:
            # show comparison
            raw_input(
                np.sqrt(
                    np.mean(
                        np.array(Y_data) ** 2)) *
                settings.SCI_NOT_FACT)

    print("tabulate is finished!")
