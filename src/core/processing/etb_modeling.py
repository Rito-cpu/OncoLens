import sys
import math
import os
import pandas as pd
import numpy as np
import time
import matplotlib.axes
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings( "ignore")#, module = "matplotlib\..*" )

from src.core.pyqt_core import *
from src.core.keyword_store import *
from matplotlib.patches import Rectangle
from scipy.integrate import odeint

_sim_max: float = 1e-11

# **** Getters and Setters ****
def set_detect_size(size: float):
    global DETECT_SIZE
    DETECT_SIZE = size

def set_detect_line(value: float):
    global DETECT_LINE
    DETECT_LINE = value

def set_death_threshold(threshold: float):
    global DEATH_THRESHOLD
    DEATH_THRESHOLD = threshold

def set_sim_max(value: float):
    global _sim_max
    _sim_max = value

def get_sim_max():
    global _sim_max
    return _sim_max

def set_excel_file_path(path: str):
    global modeling_excel_path
    modeling_excel_path = os.path.abspath(path)

# **** ETB Modeling Helper Methods ****
def is_treatment_segment(date_segment, treatment_dates):
    """Function that compares current date segment against 2D array of treatment dates"""

    treatment_dates = treatment_dates.flatten()
    if len(treatment_dates)/2 == math.floor(len(treatment_dates)/2):
        num_of_pulses = int(len(treatment_dates)/2)
        for pulse in range(num_of_pulses):
            if date_segment[0] >= treatment_dates[2 * pulse] and date_segment[1] <= treatment_dates[2 * pulse + 1]:
                return 1
        return 0
    else:
        sys.exit('Needs an even input vector!')

def gdrs_model(init_state, time_range, *params):
    """GDRS equation method to be used with odeint"""
    current_dates, tx_dates, tx_IDS, is_active_tx, growth_rate, efficacy_rate, resistance_list, sensitivity_list = params

    init_size = init_state[0]
    treatment_efficacies = init_state[1:]
    modeled_efficacies = np.zeros(len(treatment_efficacies))
    treatment_killsum = 0
    rs_switch = np.zeros(len(treatment_efficacies))

    for index in range(len(tx_IDS)):
        if is_active_tx[index]:
            formatted_ID = tx_IDS[index] - 1
            drug_active = is_treatment_segment(current_dates, tx_dates[index, :])
            if drug_active:
                rs_switch[formatted_ID] = 1
            treatment_killsum = treatment_killsum + efficacy_rate[index] * growth_rate * treatment_efficacies[formatted_ID] * drug_active

    for index in range(len(treatment_efficacies)):
        if rs_switch[index]:
            modeled_efficacies[index] = -treatment_efficacies[index] * resistance_list[index]
        else:
            modeled_efficacies[index] = treatment_efficacies[index] * sensitivity_list[index] * (1 - treatment_efficacies[index])

    modeled_size = init_size * (growth_rate - treatment_killsum)
    modeled_state = np.append(modeled_size, modeled_efficacies)

    return modeled_state   # Returning [dT dE dE ... dE]

def combine_treatments(historical_treatments, available_treatments):
    # **** Combine treatment groups ****
    tx_abbr_combined = historical_treatments["abbr"] + available_treatments["abbr"]
    on_dates_combined = historical_treatments["date_on"] + available_treatments["date_on"]
    off_dates_combined = historical_treatments["date_off"] + available_treatments["date_off"]
    delta_values_combined = historical_treatments["efficacy"] + available_treatments["efficacy"]
    res_values_combined = historical_treatments["resistance"] + available_treatments["resistance"]
    sens_values_combined = historical_treatments["sensitivity"] + available_treatments["sensitivity"]

    # **** Sort treatment data ****
    temp = np.asarray(on_dates_combined)
    sorted_indices = np.argsort(temp)
    on_dates_combined = temp[sorted_indices]

    temp = np.asarray(off_dates_combined)
    off_dates_combined = temp[sorted_indices]

    temp = np.asarray(tx_abbr_combined)
    tx_abbr_combined = temp[sorted_indices]

    temp = np.asarray(delta_values_combined)
    delta_values_combined = temp[sorted_indices]

    temp = np.asarray(res_values_combined)
    res_values_combined = temp[sorted_indices]

    temp = np.asarray(sens_values_combined)
    sens_values_combined = temp[sorted_indices]

    # **** Assign ID's to treatments ****
    treatment_ID_tracker = {}
    treatment_ID = 1
    treatment_ID_values =  []

    for tx in tx_abbr_combined:
        if tx not in treatment_ID_tracker.keys():
            treatment_ID_tracker[tx] = treatment_ID
            treatment_ID += 1
        treatment_ID_values.append(treatment_ID_tracker[tx])

    # **** Package and return ****
    combined_treatments_dict = {
        "abbr": tx_abbr_combined,
        "date_on": pd.to_datetime(on_dates_combined),
        "date_off": pd.to_datetime(off_dates_combined),
        "efficacy": delta_values_combined,
        "resistance": res_values_combined,
        "sensitivity": sens_values_combined,
        "id_list": treatment_ID_values,
        "id_dict": treatment_ID_tracker
    }

    return combined_treatments_dict

def assign_plot_treatments(treatment_data: dict, extra_treatment: dict=None, dos=None):
    if extra_treatment:
        regimens = extra_treatment['data']['regimens']
        num_regimens = len(regimens.keys())

        num_tx = treatment_data['num_tx'] + num_regimens
        plot_list = np.concatenate([treatment_data["plot"], np.ones(num_regimens)])

        cone_start, cone_end = [], []
        for regimen, tx_list in regimens.items():
            start, end = extra_treatment['lengths'][regimen]
            delta = (start-dos).days
            cone_start.append(delta)
            delta = (end-dos).days
            cone_end.append(delta)

        days_to_start = np.concatenate([treatment_data["days_to_start"], np.asarray(cone_start)])
        days_to_end = np.concatenate([treatment_data["days_to_end"], np.asanyarray(cone_end)])

        # num_tx = treatment_data["num_tx"] + len(extra_treatment["abbr"])
        # plot_list = np.concatenate([treatment_data["plot"], np.ones(len(extra_treatment["abbr"]))])
        # extra_days_to_start, extra_days_to_end = days_calculation(extra_treatment["date_on"], extra_treatment["date_off"], dos)
        # days_to_start = np.concatenate([treatment_data["days_to_start"], extra_days_to_start])
        # days_to_end = np.concatenate([treatment_data["days_to_end"], extra_days_to_end])
    else:
        # if not using cone settings, create default case variables
        num_tx = treatment_data["num_tx"]
        plot_list = treatment_data["plot"]
        days_to_start = treatment_data["days_to_start"]
        days_to_end = treatment_data["days_to_end"]

    # treatment_order = np.arange(0, treatment_data["num_tx"], 1)
    treatment_order = np.arange(0, num_tx, 1)
    # assigned_treatment_rows = np.zeros(treatment_data["num_tx"])
    assigned_treatment_rows = np.zeros(num_tx)
    min_treatment_index = min(treatment_order)
    assigned_treatment_rows[min_treatment_index] = 1
    max_row_assign = 1
    max_rows = 1

    # for index in range(min_treatment_index, treatment_data["num_tx"]):
    for index in range(min_treatment_index, num_tx):
        # if treatment_data["plot"][index] == 1:
        if plot_list[index] == 1:
            need_assignment = True
            row_assignment = 1
            while need_assignment:
                more_than_all = True
                chi = 0
                for y in range(chi, index):
                    if assigned_treatment_rows[y] == row_assignment:
                        # if treatment_data["days_to_start"][index] < treatment_data["days_to_end"][y]:
                        if days_to_start[index] < days_to_end[y]:
                            more_than_all = False
                if more_than_all:
                    assigned_treatment_rows[index] = row_assignment
                    need_assignment = False
                else:
                    row_assignment += 1
                    if row_assignment > max_row_assign:
                        assigned_treatment_rows[index] = row_assignment
                        need_assignment = False
                        max_row_assign += 1

    for row in assigned_treatment_rows:
        if row > max_rows:
            max_rows = row

    return assigned_treatment_rows, max_rows

def days_calculation(on_date, off_date, dos=None):
    days_to_start = []
    days_to_end = []

    for start_date, end_date in zip(on_date, off_date):
        day_delta = (start_date - dos).days
        days_to_start.append(day_delta)
        day_delta = (end_date - dos).days
        days_to_end.append(day_delta)

    return days_to_start, days_to_end

def format_matrix(name_abbr: np.ndarray, num_lesions: int, matrix_array: np.ndarray):
    tx_switch_array = []
    counter = 0

    for name in name_abbr:
        switch_values = []
        if name.lower() == "rad" or name.lower() == "surg":
            if counter <= len(matrix_array):
                switch_values = matrix_array[counter]
                counter += 1
            else:
                # print("Out of bounds for nonsystemic treatments - redo matrix!")
                break
        else:
            switch_values = np.ones(num_lesions)
        tx_switch_array.append(switch_values)

    return np.array(tx_switch_array)

def identify_nonsystemic_lesions(name_abbr: np.ndarray, num_lesions: int, matrix_array: np.ndarray):
    matrix_tx_rows = name_abbr
    nonsystemic_treatments = {
        "surgery": [],
        "surgery_index": [],
        "radiation": [],
        "radiation_index": []
    }

    for index in range(len(matrix_tx_rows)):
        if "surg" in matrix_tx_rows[index].lower() or "surgery" in matrix_tx_rows[index].lower():
            nonsystemic_treatments["surgery"].append(index)
        elif "rad" in matrix_tx_rows[index].lower() or "radiation" in matrix_tx_rows[index].lower():
            nonsystemic_treatments["radiation"].append(index)

    for lesion in range(num_lesions):
        if nonsystemic_treatments["surgery"]:
            for s in nonsystemic_treatments["surgery"]:
                if matrix_array[s, lesion] == 1:
                    nonsystemic_treatments["surgery_index"].append(lesion) if lesion not in nonsystemic_treatments["surgery_index"] else None
        if nonsystemic_treatments["radiation"]:
            for r in nonsystemic_treatments["radiation"]:
                if matrix_array[r, lesion] == 1:
                    nonsystemic_treatments["radiation_index"].append(lesion) if lesion not in nonsystemic_treatments["radiation_index"] else None

    return nonsystemic_treatments

def remove_lesion_scans(clean_lesions: bool, nonsystemic_treatments: dict, matrix_array: np.ndarray, scan_dates: np.ndarray, joined_dates: np.ndarray):
    lesion_scan_removal = {}
    if clean_lesions:
        if len(nonsystemic_treatments["radiation_index"]) != 0:
            for target in nonsystemic_treatments["radiation_index"]:
                for tx in nonsystemic_treatments["radiation"]:
                    if matrix_array[tx, target] == 1:
                        lesion_scan_removal[target] = []
                        for index, date in enumerate(scan_dates):
                            if date > joined_dates[tx][1]:
                                lesion_scan_removal[target].append(index)
                        break
        if len(nonsystemic_treatments["surgery_index"]) != 0:
            for lesion_index in nonsystemic_treatments["surgery_index"]:
                for tx in nonsystemic_treatments["surgery"]:
                    if matrix_array[tx, lesion_index] == 1:
                        lesion_scan_removal[lesion_index] = []
                        for index, date in enumerate(scan_dates):
                            if date > joined_dates[tx][1] and index not in lesion_scan_removal[lesion_index]:
                                lesion_scan_removal[lesion_index].append(index)
                        break

    return lesion_scan_removal

def get_scan_volumes(num_lesions: int, lesion_data: np.ndarray, scan_dates: np.ndarray, scan_df: pd.DataFrame):
    recist_scans = []
    lesion_volumes = []

    for index in range(num_lesions):
        recist_scans.append(lesion_data[index, 2])
        volume_instance = []

        for current_date in scan_dates:
            column_index = scan_df.columns.get_loc(current_date)
            scan_vol = scan_df.iloc[index + 1, column_index]
            if isinstance(scan_vol, str):
                scan_vol = np.nan
            elif scan_vol == 0 or scan_vol < 0:
                # scan_vol = 0.99 * get_detect_size()
                scan_vol = 0.99 * DETECT_SIZE
            volume_instance.append(scan_vol)
        lesion_volumes.append(volume_instance)

    return recist_scans, np.asarray(lesion_volumes)

def get_maximum_volume(num_lesions: int, plot: np.ndarray, lesion_volumes: np.ndarray):
    normal_y_max = 0

    for index in range(num_lesions):
        if plot[index]:
            temp_max = np.nanmax(lesion_volumes[index])
            if temp_max is not np.nan and temp_max > normal_y_max:
                normal_y_max = temp_max

    return normal_y_max

def model_simulation(
        lesion_data: dict,
        treatment_data: dict,
        active_tx: np.ndarray,
        lesion_volumes: np.ndarray,
        matrix_array: np.ndarray,
        t_breaks: np.ndarray,
        unique_all_dates: np.ndarray
    ):
    simulation_dates = [None] * lesion_data["num_lesions"]
    simulation_data = [None] * lesion_data["num_lesions"]

    for lesion_index in range(lesion_data["num_lesions"]):
        if lesion_data["simulate"][lesion_index]:
            existing_lesion_index = np.argwhere(~pd.isna(lesion_volumes[lesion_index])).flatten()
            model_gamma = lesion_data["growth"][lesion_index] * lesion_data["growth_mults"][lesion_index]
            model_delta = (treatment_data["efficacy"] * lesion_data["efficacy_mults"][lesion_index]) * matrix_array[:, lesion_index].T
            model_res = treatment_data["resistance"] * lesion_data["resistance_mults"][lesion_index]
            model_sens = treatment_data["sensitivity"] * lesion_data["sensitivity_mults"][lesion_index]
            initial_state = np.ones(treatment_data["num_tx"]+1)
            initial_state[0] = 0
            ys, xs = [], [0]
            volume_start_index = existing_lesion_index[0]
            lesion_exist = np.argwhere(t_breaks == lesion_data["scan_dates"][volume_start_index]).flatten()

            for index, date in enumerate(t_breaks[:-1]):
                if date == unique_all_dates[lesion_exist]:
                    initial_state[0] = lesion_volumes[lesion_index][volume_start_index] * (10**lesion_data["offset"][lesion_index])
                    ys.append(initial_state[0])
                first_date = (t_breaks[index] - lesion_data["dos"]).days
                second_date = (t_breaks[index+1] - lesion_data["dos"]).days
                step_size = (second_date-first_date) # * 2    # Half-a-day
                time_range = np.linspace(first_date, second_date, step_size+1)
                current_dates = np.array([t_breaks[index], t_breaks[index+1]])
                params = (current_dates, treatment_data["joined_dates"], treatment_data["id_list"], active_tx, model_gamma, model_delta, model_res, model_sens)
                ode_result = odeint(gdrs_model, initial_state, time_range, args=params)
                initial_state = ode_result[-1, :]
                ys.append(ode_result[1:, 0])
                xs.append(time_range[1:])
                if initial_state[0] < DEATH_THRESHOLD:
                    initial_state[0] = 0
            ys, xs = np.hstack(ys), np.hstack(xs)
            first_time = (np.argwhere(xs == (lesion_data["scan_dates"][volume_start_index] - lesion_data["dos"]).days)).flatten()
            first_time = first_time[0]
            simulation_dates[lesion_index] = xs[first_time:]
            ys = np.where(ys == 0, 10**-10, ys)
            simulation_data[lesion_index] = ys[first_time:]
            new_max = max(get_sim_max(), max(ys))
            set_sim_max(new_max)

    return simulation_dates, simulation_data

def plot_normal_points(normal_y_min: float, lesion_data: dict, clean_lesions: bool, lesion_volumes: np.ndarray, les_scan_removal: dict,
                    plot_start_time: int, nonsystemic_treatments: dict, normal_ax: matplotlib.axes.Axes,
                    detected_args: list, lesion_args: list, misc_args: list):
    detected_lesion_offset, detected_lesion_marker_size, detected_lesion_marker_width = detected_args
    lesion_marker_size, lesion_text_offset_ticks, lesion_color_list = lesion_args
    text_size, text_offset, label_percent_OS, up_down_OS, plot_up_lesion_list = misc_args

    y_axis_min = normal_y_min
    detected_lesion_offset_ticks = np.zeros(lesion_data["num_scans"])

    for lesion_index in range(lesion_data["num_lesions"]):
        lesion_label_needed = True
        if lesion_data["plot"][lesion_index]:
            if clean_lesions:
                firstInstance = np.argwhere(~pd.isna(lesion_volumes[lesion_index])).flatten()
                firstInstance = firstInstance[0]
                plotCondition = lesion_index in les_scan_removal.keys()#  and len(lesScanRemoval[li]) != 0
            for scan_index in range(lesion_data["num_scans"]):
                if (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days >= plot_start_time:
                    if clean_lesions:
                        if plotCondition and scan_index == firstInstance:
                            if lesion_index in nonsystemic_treatments["surgery_index"]:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index], color='gold',
                                            marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                            elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index], color='black',
                                            marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                        elif plotCondition and scan_index in les_scan_removal[lesion_index]:
                            continue
                        # Plot everything else normally
                        # if lesion_volumes[lesion_index][scan_index] <= get_detect_size():
                        if lesion_volumes[lesion_index][scan_index] <= DETECT_SIZE:
                            normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days,
                                        lesion_volumes[lesion_index][scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                        color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                        linewidth=detected_lesion_marker_width)
                            detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                        # Plot normal points
                        else:
                            if lesion_data["recist"][lesion_index]:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index],
                                            color=lesion_color_list[lesion_index],
                                            marker='^', markersize=lesion_marker_size / 2)
                            else:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index],
                                            color=lesion_color_list[lesion_index],
                                            marker='.', markersize=lesion_marker_size)
                        if lesion_label_needed and ~np.isnan(lesion_volumes[lesion_index][scan_index]):
                            # if lesion_volumes[lesion_index][scan_index] <= get_detect_size():
                            if lesion_volumes[lesion_index][scan_index] <= DETECT_SIZE:
                                yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                if yPlotVal + text_offset < y_axis_min:
                                    y_axis_min = yPlotVal + text_offset
                                    normal_y_min = y_axis_min
                                normal_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal,
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
                                lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                            else:
                                yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset
                                normal_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
                    else:
                        # X'ing out small points
                        # if lesion_volumes[lesion_index][scan_index] <= get_detect_size():
                        if lesion_volumes[lesion_index][scan_index] <= DETECT_SIZE:
                            normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days,
                                        lesion_volumes[lesion_index][scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                        color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                        linewidth=detected_lesion_marker_width)
                            detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                        # Plot normal points
                        else:
                            if lesion_index in nonsystemic_treatments["surgery_index"]:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index], color='gold',
                                            marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                            elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index], color='black',
                                            marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                            if lesion_data["recist"][lesion_index]:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                            marker='^', markersize=lesion_marker_size / 2)
                            else:
                                normal_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                            marker='.', markersize=lesion_marker_size)
                        if lesion_label_needed and ~np.isnan(lesion_volumes[lesion_index][scan_index]):
                            # if lesion_volumes[lesion_index][scan_index] <= get_detect_size():
                            if lesion_volumes[lesion_index][scan_index] <= DETECT_SIZE:
                                yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                if yPlotVal + text_offset < y_axis_min:
                                    y_axis_min = yPlotVal + text_offset
                                    normal_y_min = y_axis_min
                                normal_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal,
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
                                lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                            else:
                                yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset
                                normal_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False

    return normal_ax

def plot_log_points(log_y_min: float, lesion_data: dict, clean_lesions: bool, log_lesion_volumes: np.ndarray, les_scan_removal: dict,
                    plot_start_time, nonsystemic_treatments: dict, log_ax: matplotlib.axes.Axes, detected_args: list, lesion_args: list, misc_args: list):
    log_detect_size, log_detected_lesion_offset, detected_lesion_marker_size, detected_lesion_marker_width = detected_args
    lesion_marker_size, lesion_text_offset_ticks, lesion_color_list = lesion_args
    text_size, text_offset, label_percent_OS, up_down_OS, plot_up_lesion_list = misc_args

    yPlotValMin = log_y_min
    detected_lesion_offset_ticks = np.zeros(lesion_data["num_scans"])

    for lesion_index in range(lesion_data["num_lesions"]):
        lesion_label_needed = True
        if lesion_data["plot"][lesion_index]:
            if clean_lesions:
                firstInstance = np.argwhere(~pd.isna(log_lesion_volumes[lesion_index])).flatten()
                firstInstance = firstInstance[0]
                plotCondition = lesion_index in les_scan_removal.keys()#  and len(lesScanRemoval[li]) != 0
            for scan_index in range(lesion_data["num_scans"]):
                if (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days >= plot_start_time:
                    if clean_lesions:
                        if plotCondition and scan_index == firstInstance:
                            if lesion_index in nonsystemic_treatments["surgery_index"]:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='gold',
                                            marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                            elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='black',
                                            marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                        elif plotCondition and scan_index in les_scan_removal[lesion_index]:
                            continue
                        # Plot everything else normally
                        if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                            log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days,
                                        log_lesion_volumes[lesion_index][scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                        color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                        linewidth=detected_lesion_marker_width)
                            detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                        # Plot normal points
                        else:
                            if lesion_data["recist"][lesion_index]:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index],
                                            color=lesion_color_list[lesion_index],
                                            marker='^', markersize=lesion_marker_size / 2)
                            else:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index],
                                            color=lesion_color_list[lesion_index],
                                            marker='.', markersize=lesion_marker_size)
                        if lesion_label_needed and ~np.isnan(log_lesion_volumes[lesion_index][scan_index]):
                            if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                                yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                if yPlotVal + text_offset < yPlotValMin:
                                    yPlotValMin = yPlotVal + text_offset
                                    log_y_min = yPlotValMin
                                log_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal,
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
                                lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                            else:
                                yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset
                                log_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
                    else:
                        # X'ing out small points
                        if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                            log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days,
                                        log_lesion_volumes[lesion_index][scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                        color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                        linewidth=detected_lesion_marker_width)
                            detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                        # Plot normal points
                        else:
                            if lesion_index in nonsystemic_treatments["surgery_index"]:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='gold',
                                            marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                            elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='black',
                                            marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                            if lesion_data["recist"][lesion_index]:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                            marker='^', markersize=lesion_marker_size / 2)
                            else:
                                log_ax.plot((lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                            marker='.', markersize=lesion_marker_size)
                        if lesion_label_needed and ~np.isnan(log_lesion_volumes[lesion_index][scan_index]):
                            if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                                yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                if yPlotVal + text_offset < yPlotValMin:
                                    yPlotValMin = yPlotVal + text_offset
                                    log_y_min = yPlotValMin
                                log_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal,
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
                                lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                            else:
                                yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset
                                log_ax.text(
                                    (lesion_data["scan_dates"][scan_index] - lesion_data["dos"]).days - label_percent_OS,
                                    yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                    lesion_data["abbr"][lesion_index],
                                    fontsize=text_size,
                                    color=lesion_color_list[lesion_index],
                                    horizontalalignment='right',
                                    clip_on=True
                                )
                                lesion_label_needed = False
    return log_ax

def format_treatment_plot(
        treatment_data: dict,
        assigned_treatment_rows: np.ndarray,
        x_limit,
        lesion_marker_size: int,
        normal_axes: matplotlib.axes.Axes,
        log_axes: matplotlib.axes.Axes,
        nonsystemic_treatments: dict,
        extra_treatment: dict=None,
        cone_colors: dict=None,
        dos=None
    ):
    if extra_treatment:
        regimen_cocktails = {}
        regimens = extra_treatment['data']['regimens']
        num_regimens = len(regimens.keys())

        cone_start, cone_end = [], []
        cocktail_list = []
        for regimen, tx_list in regimens.items():
            cocktail = tx_list[0]

            if len(tx_list) == 2:
                cocktail += '+' + tx_list[1]
            elif len(tx_list) > 2:
                for index, tx_name in enumerate(tx_list[:-1]):
                    cocktail += '+' + tx_list[index+1]

            start, end = extra_treatment['lengths'][regimen]
            delta = (start-dos).days
            cone_start.append(delta)
            delta = (end-dos).days
            cone_end.append(delta)
            length = (end-start).days

            regimen_cocktails[cocktail] = regimen
            cocktail_list.append(cocktail)

        num_tx = treatment_data['num_tx'] + num_regimens
        plot_list = np.concatenate([treatment_data['plot'], np.ones(num_regimens)])
        days_to_start = np.concatenate([treatment_data['days_to_start'], np.asarray(cone_start)])
        days_to_end = np.concatenate([treatment_data['days_to_end'], np.asarray(cone_end)])
        extra_duration = [end-start for start, end in zip(cone_start, cone_end)]
        duration_list = np.concatenate([treatment_data['duration'], extra_duration])
        names_list = np.concatenate([treatment_data['abbr'], cocktail_list])

        #num_tx = treatment_data["num_tx"] + len(extra_treatment["abbr"])
        #plot_list = np.concatenate([treatment_data["plot"], np.ones(len(extra_treatment["abbr"]))])
        #extra_days_to_start, extra_days_to_end = days_calculation(extra_treatment["date_on"], extra_treatment["date_off"], dos)
        #days_to_start = np.concatenate([treatment_data["days_to_start"], extra_days_to_start])
        #days_to_end = np.concatenate([treatment_data["days_to_end"], extra_days_to_end])
        #extra_duration = [end-start for start, end in zip(extra_days_to_start, extra_days_to_end)]
        #duration_list = np.concatenate([treatment_data["duration"], extra_duration])
        #names_list = np.concatenate([treatment_data["abbr"], extra_treatment["abbr"]])
    else:
        # if not using cone settings, create default case variables
        num_tx = treatment_data["num_tx"]
        plot_list = treatment_data["plot"]
        days_to_start = treatment_data["days_to_start"]
        days_to_end = treatment_data["days_to_end"]
        duration_list = treatment_data["duration"]
        names_list = treatment_data["abbr"]

    tx_color_list = plt.cm.turbo(np.linspace(0, 1, num_tx + 1))
    tx_color_list[:, 1] = tx_color_list[:, 1] * 0.85

    for index in range(num_tx):
        if plot_list[index] == 1:
            start = days_to_start[index]
            row_num = assigned_treatment_rows[index] - 1
            length = duration_list[index]
            name = names_list[index]
            # Check if we need to use cone-specific colors
            if extra_treatment and name in regimen_cocktails.keys():
                bar_color = cone_colors[regimen_cocktails[name]]
            else:
                bar_color = tx_color_list[index]
            if start+length > x_limit:
                new_length = x_limit - start
                rectangle = Rectangle(
                    (start, row_num),
                    new_length + 10,
                    1.0,
                    color=bar_color,
                    alpha=0.5,
                    linewidth=0.5
                )
                rectangle_dup = Rectangle(
                    (start, row_num),
                    new_length + 10,
                    1.0,
                    color=bar_color,
                    alpha=0.5,
                    linewidth=0.5
                )
            else:
                rectangle = Rectangle(
                    (start, row_num),
                    length,
                    1.0,
                    color=bar_color,
                    alpha=0.8,
                    linewidth=0.5,
                    zorder=2
                )
                rectangle_dup = Rectangle(
                    (start, row_num),
                    length,
                    1.0,
                    color=bar_color,
                    alpha=0.8,
                    linewidth=0.5,
                    zorder=2
                )
            normal_axes.add_patch(rectangle)
            log_axes.add_patch(rectangle_dup)
            rectangle_x, rectangle_y = rectangle.get_xy()
            center_x = rectangle_x + rectangle.get_width()/2
            center_y = rectangle_y + rectangle.get_height()/2
            normal_axes.annotate(name, (center_x, center_y), color='black', weight='bold', fontsize=7, ha='center', va='center', zorder=2)
            log_axes.annotate(name, (center_x, center_y), color='black', weight='bold', fontsize=7, ha='center', va='center', zorder=2)
            if index in nonsystemic_treatments["radiation"]:
                normal_axes.plot(center_x, center_y+0.025, color='black', marker='D', alpha=0.3, markersize=lesion_marker_size*1.3, zorder=2)
                log_axes.plot(center_x, center_y+0.025, color='black', marker='D', alpha=0.3, markersize=lesion_marker_size*1.3, zorder=2)
            elif index in nonsystemic_treatments["surgery"]:
                normal_axes.plot(center_x, center_y+0.025, color='gold', marker='*', alpha=0.3, markersize=lesion_marker_size*2, zorder=2)
                log_axes.plot(center_x, center_y+0.025, color='gold', marker='*', alpha=0.3, markersize=lesion_marker_size*2, zorder=2)

    return normal_axes, log_axes

# **** Main ETB Modeling Process ****
def etb_process(model_options: list[dict], progress: pyqtSignal):
    general_data, lesion_dict, historical_treatments, available_treatments, cone_settings, matrix_dict = model_options

    set_excel_file_path(general_data["file"])

    if cone_settings["method"] == NO_CONE:
        # If we are not using cones for our model, we can combine all treatments
        tx_dict = combine_treatments(historical_treatments, available_treatments)
    else:
        # If we are using cones, we need to use gdrs with just the historical treatments
        # **** Assign ID's to treatments ****
        treatment_ID_tracker = {}
        treatment_ID = 1
        treatment_ID_values =  []

        for tx in historical_treatments["abbr"]:
            if tx not in treatment_ID_tracker.keys():
                treatment_ID_tracker[tx] = treatment_ID
                treatment_ID += 1
            treatment_ID_values.append(treatment_ID_tracker[tx])
        historical_treatments["date_on"] = pd.to_datetime(historical_treatments["date_on"])
        historical_treatments["date_off"] = pd.to_datetime(historical_treatments["date_off"])
        historical_treatments["efficacy"] = np.asarray(historical_treatments["efficacy"])
        historical_treatments["resistance"] = np.asarray(historical_treatments["resistance"])
        historical_treatments["sensitivity"] = np.asarray(historical_treatments["sensitivity"])
        historical_treatments["id_list"] = treatment_ID_values
        historical_treatments["id_tracker"] = treatment_ID_tracker
        tx_dict = historical_treatments

        available_treatment_dict = cone_settings["toggled_treatments"] # abbr, date on, date off, efficacy, resistance, sensitivity
        available_treatment_dict["date_on"] = pd.to_datetime(available_treatment_dict["date_on"])
        available_treatment_dict["date_off"] = pd.to_datetime(available_treatment_dict["date_off"])
        available_treatment_dict["efficacy"] = np.asarray(available_treatment_dict["efficacy"])
        available_treatment_dict["resistance"] = np.asarray(available_treatment_dict["resistance"])
        available_treatment_dict["sensitivity"] = np.asarray(available_treatment_dict["sensitivity"])
        available_treatment_dict["num_tx"] = len(available_treatment_dict["abbr"])
        available_treatment_dict["plot"] = np.ones(available_treatment_dict["num_tx"])

    tx_dict["num_tx"] = len(tx_dict["abbr"])
    tx_dict["plot"] = np.ones(tx_dict["num_tx"])

    progress.emit(1)
    time.sleep(0.05)

    # --- Retrieve more lesion data from Excel sheets ---
    lesion_scan_df = pd.read_excel(modeling_excel_path, sheet_name=SCAN_DATA_SHEET, header=0)
    lesion_info_df = pd.read_excel(modeling_excel_path, sheet_name=SCAN_DATA_SHEET, header=1)
    lesion_data = lesion_info_df.to_numpy()

    if lesion_data.shape[0] == 0 or lesion_data.shape[1] <= 3:
        sys.exit(f"Clinician data does not meet minimum requirements. Missing values and/or columns.")

    lesion_vol_headers = 1
    lesion_dict["num_lesions"] = len(lesion_dict["abbr"])
    # lesion_dict["scan_dates"] = pd.to_datetime(lesion_scan_df.columns[lesion_scan_df.iloc[0] == "Volume"])
    temp_date_list = []
    for date in lesion_scan_df.columns[lesion_scan_df.iloc[0] == "Volume"]:
        temp_date_list.append(date)
    lesion_dict["scan_dates"] = pd.to_datetime(temp_date_list)
    lesion_dict["num_scans"] = len(lesion_dict["scan_dates"])
    lesion_dict["dos"] = min(lesion_dict["scan_dates"][0], tx_dict["date_on"][0])

    # --- Format Matrix ---
    matrix_dict["array"] = format_matrix(
        tx_dict["abbr"],
        lesion_dict["num_lesions"],
        matrix_dict["array"]
    )

    # --- Gather scan date volumes ---
    lesion_dict["recist"], lesion_volumes = get_scan_volumes(
        lesion_dict["num_lesions"],
        lesion_data,
        lesion_dict["scan_dates"],
        lesion_scan_df
    )

    # --- Gather notable dates from Excel sheet ---
    notable_dates_df = pd.read_excel(modeling_excel_path, sheet_name=NOTABLE_DATES_SHEET, header=0)
    header_names = ["ETBdates", "NextScans", "Expired"]
    notable_dates_dict = {
        "ETBdates": pd.to_datetime(notable_dates_df[header_names[0]]).dropna() if notable_dates_df[header_names[0]].count() != 0 else None,
        "NextScans": pd.to_datetime(notable_dates_df[header_names[1]]).dropna() if notable_dates_df[header_names[1]].count() != 0 else None,
        "Expired": pd.to_datetime(notable_dates_df[header_names[2]]).dropna() if notable_dates_df[header_names[2]].count() != 0 else None
    }

    # --- Find maximum volume for plot ---
    normal_y_max = get_maximum_volume(
        lesion_dict["num_lesions"],
        lesion_dict["plot"],
        lesion_volumes
    )
    y_max_holder = normal_y_max

    progress.emit(15)
    time.sleep(0.05)

    # --- Calculate days between treatment start and end dates ---
    tx_dict["days_to_start"], tx_dict["days_to_end"] = days_calculation(tx_dict["date_on"], tx_dict["date_off"], dos=lesion_dict["dos"])

    # --- Calculate duration of each treatment ---
    tx_dict["duration"] = [end-start for start, end in zip(tx_dict["days_to_start"], tx_dict["days_to_end"])]

    progress.emit(25)
    time.sleep(0.03)


    # progress.emit(45)
    # time.sleep(0.05)

    # --- GDRS Model variable prep ---
    active_tx = np.ones(tx_dict["num_tx"])
    tx_dict["joined_dates"] = np.array([tx_dict["date_on"], tx_dict["date_off"]]).T
    unique_tx_dates = np.unique(tx_dict["joined_dates"], axis=0)
    holder = np.unique(unique_tx_dates.flatten())
    unique_all_dates = np.concatenate((holder, lesion_dict["scan_dates"]), axis=0)
    unique_all_dates = np.unique(unique_all_dates)
    holder = unique_all_dates[len(unique_all_dates)-1] + np.timedelta64(1, "D")
    time_with_breaks = np.append(unique_all_dates, holder)

    if cone_settings["method"] == NO_CONE:
        # We add 80 days here because we put 80 days as a buffer for the last time, and this method is set in stone
        end_time = max(unique_all_dates) + np.timedelta64(80, "D")
    else:
        end_time = max(unique_all_dates)

    t_end_index = np.argwhere(end_time <= time_with_breaks).flatten()
    if len(t_end_index) == 0:
        time_with_breaks = np.append(time_with_breaks, end_time)
    else:
        t_end_index = t_end_index[0]
        time_with_breaks = np.append(time_with_breaks[0:t_end_index], end_time)

    progress.emit(55)
    time.sleep(0.05)

    # --- Targeting lesions with radiation and surgery ---
    nonsystemic_treatments = identify_nonsystemic_lesions(
        tx_dict["abbr"],
        lesion_dict["num_lesions"],
        matrix_dict["array"]
    )

    les_scan_removal = remove_lesion_scans(
        general_data["clean_lesions"],
        nonsystemic_treatments,
        matrix_dict["array"],
        lesion_dict["scan_dates"],
        tx_dict["joined_dates"]
    )

    progress.emit(70)
    time.sleep(0.05)

    # --- Model GDRS ---
    simulation_dates, simulation_data = model_simulation(
        lesion_dict,
        tx_dict,
        active_tx,
        lesion_volumes,
        matrix_dict["array"],
        time_with_breaks,
        unique_all_dates
    )

    progress.emit(85)
    time.sleep(0.05)

    # Model GDRS for Cone
    if cone_settings['method'] == COMPARISON_CONE:
        cone_data = cone_settings['data']
        cone_lesion = cone_data['target_lesion']
        cone_lesion_index = lesion_dict['abbr'].index(cone_lesion)
        cone_settings['lesion_index'] = cone_lesion_index

        if lesion_dict['simulate'][cone_lesion_index]:
            # Go through each regimen - each regimen is a schedule to be modeled
            regimen_data_store = {}
            regimen_lengths = {}

            for regimen, treatments in cone_data['regimens'].items():
                bounds_data = {}

                # Create id's to track the drugs being modeled
                id_track = {}
                id_num = 1
                id_list = []

                # Need to gather regimen drug dates
                regimen_date_on = []
                regimen_date_off = []

                # Lists for minimum parameters
                # In separate lists because we apply mathematical operations per parameter
                regimen_min_efficacies = []
                regimen_min_resistances = []
                regimen_min_sensitivities = []

                # Lists for average parameters
                regimen_avg_efficacies = []
                regimen_avg_resistances = []
                regimen_avg_sensitivities = []

                # Lists for max parameters
                regimen_max_efficacies = []
                regimen_max_resistances = []
                regimen_max_sensitivities = []

                # Gather all drug data to model for this regimen
                for drug in treatments:
                    drug_widget = cone_data['drugs'][drug]

                    drug_min = drug_widget.get_min_values()     # [efficacy, resistance, sensitivity]
                    regimen_min_efficacies.append(drug_min[0])
                    regimen_min_resistances.append(drug_min[1])
                    regimen_min_sensitivities.append(drug_min[2])

                    drug_average = drug_widget.get_average_values()
                    regimen_avg_efficacies.append(drug_average[0])
                    regimen_avg_resistances.append(drug_average[1])
                    regimen_avg_sensitivities.append(drug_average[2])

                    drug_max = drug_widget.get_max_values()
                    regimen_max_efficacies.append(drug_max[0])
                    regimen_max_resistances.append(drug_max[1])
                    regimen_max_sensitivities.append(drug_max[2])

                    tx_index = available_treatment_dict['abbr'].index(drug)
                    date_on = available_treatment_dict['date_on'][tx_index]
                    regimen_date_on.append(date_on)
                    date_off = available_treatment_dict['date_off'][tx_index]
                    regimen_date_off.append(date_off)

                    if drug not in id_track.keys():
                        id_track[drug] = id_num
                        id_num += 1
                    id_list.append(id_track[drug])

                # Turn lists into arrays
                regimen_date_on = pd.to_datetime(np.asarray(regimen_date_on))
                regimen_date_off = pd.to_datetime(np.asarray(regimen_date_off))
                regimen_min_efficacies = np.asarray(regimen_min_efficacies)
                regimen_min_resistances = np.asarray(regimen_min_resistances)
                regimen_min_sensitivities = np.asarray(regimen_min_sensitivities)
                regimen_avg_efficacies = np.asarray(regimen_avg_efficacies)
                regimen_avg_resistances = np.asarray(regimen_avg_resistances)
                regimen_avg_sensitivities = np.asarray(regimen_avg_sensitivities)
                regimen_max_efficacies = np.asarray(regimen_max_efficacies)
                regimen_max_resistances = np.asarray(regimen_max_resistances)
                regimen_max_sensitivities = np.asarray(regimen_max_sensitivities)

                regimen_lengths[regimen] = [regimen_date_on.min(), regimen_date_off.max()]
                cone_settings['lengths'] = regimen_lengths

                # Evaluate dates to model with
                coupled_dates = np.array([regimen_date_on, regimen_date_off]).T
                unique_tx_dates = np.unique(coupled_dates, axis=0)
                holder = np.unique(unique_tx_dates.flatten())
                unique_all_dates = np.concatenate((holder, [time_with_breaks[-1]]), axis=0) # Added this line
                unique_all_dates = np.unique(unique_all_dates)      # Added this line
                # unique_all_dates = np.unique(unique_tx_dates.flatten())
                holder = unique_all_dates[len(unique_all_dates)-1] + np.timedelta64(1, "D")
                cone_time_with_breaks = np.append(unique_all_dates, holder)
                regimen_end_date = max(unique_all_dates) + np.timedelta64(80, "D")
                t_end_index = np.argwhere(regimen_end_date <= cone_time_with_breaks).flatten()
                if len(t_end_index) == 0:
                    cone_time_with_breaks = np.append(cone_time_with_breaks, regimen_end_date)
                else:
                    t_end_index = t_end_index[0]
                    cone_time_with_breaks = np.append(cone_time_with_breaks[0:t_end_index], regimen_end_date)

                first_data_point = simulation_data[cone_lesion_index][-1]
                first_day_point = int(simulation_dates[cone_lesion_index][-1])

                new_matrix_row = np.ones(len(treatments)) # deals with systemic vs nonsystemic
                active_test = np.ones(len(treatments))    # active treatments
                model_growth = lesion_dict["growth"][cone_lesion_index] * lesion_dict["growth_mults"][cone_lesion_index]
                model_min_efficacy = (regimen_min_efficacies * lesion_dict['efficacy_mults'][cone_lesion_index] * new_matrix_row)
                model_min_resistance = regimen_min_resistances * lesion_dict['resistance_mults'][cone_lesion_index]
                model_min_sensitivity = regimen_min_sensitivities * lesion_dict['sensitivity_mults'][cone_lesion_index]

                model_avg_efficacy = (regimen_avg_efficacies * lesion_dict['efficacy_mults'][cone_lesion_index] * new_matrix_row)
                model_avg_resistance = regimen_avg_resistances * lesion_dict['resistance_mults'][cone_lesion_index]
                model_avg_sensitivity = regimen_avg_sensitivities * lesion_dict['sensitivity_mults'][cone_lesion_index]

                model_max_efficacy = (regimen_max_efficacies * lesion_dict['efficacy_mults'][cone_lesion_index] * new_matrix_row)
                model_max_resistance = regimen_max_resistances * lesion_dict['resistance_mults'][cone_lesion_index]
                model_max_sensitivity = regimen_max_sensitivities * lesion_dict['sensitivity_mults'][cone_lesion_index]

                initial_state_min = np.ones(len(treatments)+1)
                initial_state_min[0] = first_data_point
                initial_state_avg = np.ones(len(treatments)+1)
                initial_state_avg[0] = first_data_point
                initial_state_max = np.ones(len(treatments)+1)
                initial_state_max[0] = first_data_point
                min_ys, min_xs = [initial_state_min[0]], [first_day_point]
                avg_ys, avg_xs = [initial_state_avg[0]], [first_day_point]
                max_ys, max_xs = [initial_state_max[0]], [first_day_point]

                for index, date in enumerate(cone_time_with_breaks[:-1]):
                    first_date = (cone_time_with_breaks[index] - lesion_dict["dos"]).days
                    last_day = (cone_time_with_breaks[index+1] - lesion_dict["dos"]).days
                    step_size = (last_day-first_date) # * 2    # Half-a-day
                    time_range = np.linspace(first_day_point, last_day, step_size + 1)
                    current_dates = np.array([cone_time_with_breaks[index], cone_time_with_breaks[index+1]])

                    min_params = (current_dates, coupled_dates, id_list, active_test, model_growth, model_min_efficacy, model_min_resistance, model_min_sensitivity)
                    avg_params = (current_dates, coupled_dates, id_list, active_test, model_growth, model_avg_efficacy, model_avg_resistance, model_avg_sensitivity)
                    max_params = (current_dates, coupled_dates, id_list, active_test, model_growth, model_max_efficacy, model_max_resistance, model_max_sensitivity)

                    min_ode_result = odeint(gdrs_model, initial_state_min, time_range, args=min_params)
                    avg_ode_result = odeint(gdrs_model, initial_state_avg, time_range, args=avg_params)
                    max_ode_result = odeint(gdrs_model, initial_state_max, time_range, args=max_params)

                    initial_state_min = min_ode_result[-1, :]
                    initial_state_avg = avg_ode_result[-1, :]
                    initial_state_max = max_ode_result[-1, :]

                    min_ys.append(min_ode_result[1:, 0])
                    min_xs.append(time_range[1:])
                    avg_ys.append(avg_ode_result[1:, 0])
                    avg_xs.append(time_range[1:])
                    max_ys.append(max_ode_result[1:, 0])
                    max_xs.append(time_range[1:])

                    if initial_state_min[0] < DEATH_THRESHOLD():
                        initial_state_min[0] = 0
                    if initial_state_avg[0] < DEATH_THRESHOLD():
                        initial_state_avg[0] = 0
                    if initial_state_max[0] < DEATH_THRESHOLD():
                        initial_state_max[0] = 0

                    first_day_point = int(time_range[-1])
                min_ys, min_xs = np.hstack(min_ys), np.hstack(min_xs)
                avg_ys, avg_xs = np.hstack(avg_ys), np.hstack(avg_xs)
                max_ys, max_xs = np.hstack(max_ys), np.hstack(max_xs)

                min_ys = np.where(min_ys == 0, 10**-10, min_ys)
                avg_ys = np.where(avg_ys == 0, 10**-10, avg_ys)
                max_ys = np.where(max_ys == 0, 10**-10, max_ys)

                log_min_data = min_ys
                log_min_data = np.where(min_ys != 0, np.log10(min_ys), 0)
                log_avg_data = avg_ys
                log_avg_data = np.where(avg_ys != 0, np.log10(avg_ys), 0)
                log_max_data = max_ys
                log_max_data = np.where(max_ys != 0, np.log10(max_ys), 0)

                new_max = max(get_sim_max(), max(max_ys))
                set_sim_max(new_max)

                bounds_data['min_data'] = min_ys
                bounds_data['avg_data'] = avg_ys
                bounds_data['max_data'] = max_ys
                bounds_data['log_min_data'] = log_min_data
                bounds_data['log_avg_data'] = log_avg_data
                bounds_data['log_max_data'] = log_max_data
                bounds_data['days'] = min_xs
                regimen_data_store[regimen] = bounds_data


    # --- Create treatment plot settings ---
    if cone_settings["method"] == NO_CONE:
        assigned_tx_rows, max_rows = assign_plot_treatments(tx_dict)
    else:
        # Create optimal settings for plot before creating regimen schedule by using base available treatments
        # assigned_tx_rows, max_rows = assign_plot_treatments(tx_dict, available_treatment_dict, lesion_dict["dos"])
        assigned_tx_rows, max_rows = assign_plot_treatments(tx_dict, cone_settings, lesion_dict["dos"])


    # --- defining matplotlib parameters  ---
    lesion_color_list = plt.cm.turbo(np.linspace(0, 1, lesion_dict["num_lesions"] + 1))
    lesion_color_list[:, 1] = lesion_color_list[:, 1] * 0.85
    x_limit = (end_time - lesion_dict["dos"]).days
    plot_start_time = 0 - x_limit * 0.05
    text_offset_mult = 0.028
    xAxisDateTextOffsetMult = 0.2
    detected_lesion_offset_mult = 0.3
    upper_buffer_mult_y_max = 1.05  # 0.447
    legend_buffer_y_max = 0.15
    text_size = 10
    lesion_marker_size = 11
    detected_lesion_marker_size = 12
    detected_lesion_marker_width = 2
    endDateTextOffset = math.ceil(lesion_dict["num_lesions"] / 2)  # 3.1
    up_down_OS = 0.2
    maxSchedPlot = 0.2
    simulation_line_width = 1.75
    label_percent_OS = 3
    plot_up_lesion_list = np.zeros(lesion_dict["num_lesions"])
    normal_line_collect = []

    if cone_settings["method"] == COMPARISON_CONE and lesion_dict['simulate'][cone_settings['lesion_index']]:  # TODO: Adjust x limit for comparison data
        x_limit = (max(cone_time_with_breaks) - lesion_dict["dos"]).days
        # if we want all predictions to end at same time with one global x-limit, track max date in cone process

    # --- Prepare Log parameters ---
    normal_y_min = 0
    normal_y_max *= upper_buffer_mult_y_max
    normal_y_max = normal_y_max + (normal_y_max - normal_y_min) * legend_buffer_y_max
    text_offset = (normal_y_max - normal_y_min) * text_offset_mult
    detected_lesion_offset = 0
    lesion_text_offset_ticks = np.zeros(lesion_dict["num_scans"]) - text_offset

    # --- Setup Plot ---
    normal_figure, normal_axes = plt.subplots(
        2,
        1,
        figsize=(8, 8),
        gridspec_kw={
            'height_ratios': [4, 1]
        },
        sharex=True
    )

    log_figure, log_axes = plt.subplots(
        2,
        1,
        figsize=(8, 8),
        gridspec_kw={
            'height_ratios': [4, 1]
        },
        sharex=True
    )

    plot_title = os.path.split(modeling_excel_path)[1]
    plot_title = plot_title.replace(".xlsx", "")

    normal_axes[0].title.set_text(f'{plot_title}')
    normal_axes[0].set(xlabel=None, ylabel='Volume $(cm^{3})$')

    log_axes[0].title.set_text(f"{plot_title}")
    log_axes[0].set(xlabel=None, ylabel='Volume $(log_{10}(cm^{3}))$')

    normal_axes[1].set(xlabel='Days From Diagnosis', ylabel=None)
    normal_axes[1].set_xlim([plot_start_time - 30, x_limit])
    normal_axes[1].set_ylim([0, max_rows])
    normal_axes[1].get_yaxis().set_visible(False)

    log_axes[1].set(xlabel='Days From Diagnosis', ylabel=None)
    log_axes[1].set_xlim([plot_start_time - 30, x_limit])
    log_axes[1].set_ylim([0, max_rows])
    log_axes[1].get_yaxis().set_visible(False)

    progress.emit(90)
    time.sleep(0.05)

    # --- Plot GDRS ---
    detected_args = detected_lesion_offset, detected_lesion_marker_size, detected_lesion_marker_width
    lesion_args = lesion_marker_size, lesion_text_offset_ticks, lesion_color_list
    misc_args = text_size, text_offset, label_percent_OS, up_down_OS, plot_up_lesion_list

    normal_axes[0] = plot_normal_points(
        normal_y_min,
        lesion_dict,
        general_data["clean_lesions"],
        lesion_volumes,
        les_scan_removal,
        plot_start_time,
        nonsystemic_treatments,
        normal_axes[0],
        detected_args=detected_args,
        lesion_args=lesion_args,
        misc_args=misc_args
    )

    # --- Plot Lesion Sim ---
    for lesion_index in range(lesion_dict["num_lesions"]):
        if lesion_dict["simulate"][lesion_index] and simulation_dates[lesion_index] is not None:
            normal_axes[0].plot(simulation_dates[lesion_index], simulation_data[lesion_index], color=lesion_color_list[lesion_index, :], linestyle='-',
                        linewidth=simulation_line_width)

    # --- Create Log variables ---
    log_line_collect = []
    log_lesion_volumes = lesion_volumes
    log_simulation_data = simulation_data
    min_lower_buffer_log_y = 1

    for lesion_index in range(lesion_dict["num_lesions"]):
        if lesion_dict["simulate"][lesion_index] and simulation_data[lesion_index] is not None:
            with np.errstate(invalid='ignore'): # Some values are calculated to be neg and have log10 applied
                    log_simulation_data[lesion_index] = np.where(simulation_data[lesion_index] != 0, np.log10(simulation_data[lesion_index]), 0)
            for column_index in range(len(lesion_volumes[lesion_index])):
                log_volume = np.log10(lesion_volumes[lesion_index][column_index])
                log_lesion_volumes[lesion_index][column_index] = log_volume
        # log_detect_size = np.log10(get_detect_size())
        log_detect_size = np.log10(DETECT_SIZE)
        log_y_min = log_detect_size - min_lower_buffer_log_y
        log_y_min = max(log_y_min, -9.5)
        log_y_max = np.log10(max(y_max_holder, get_sim_max())) * upper_buffer_mult_y_max
        log_y_max = min(log_y_max, 4)
        log_y_max = log_y_max + (log_y_max - log_y_min) * legend_buffer_y_max
        log_text_offset = -(log_y_max - log_y_min) * text_offset_mult
        log_detected_lesion_offset = log_text_offset * detected_lesion_offset_mult
    lesion_text_offset_ticks = np.zeros(lesion_dict["num_scans"]) - text_offset

    # --- Plot Log Scans ---
    detected_args = log_detect_size, log_detected_lesion_offset, detected_lesion_marker_size, detected_lesion_marker_width
    lesion_args = lesion_marker_size, lesion_text_offset_ticks, lesion_color_list
    misc_args = text_size, text_offset, label_percent_OS, up_down_OS, plot_up_lesion_list

    log_axes[0] = plot_log_points(
        log_y_min,
        lesion_dict,
        general_data["clean_lesions"],
        log_lesion_volumes, les_scan_removal,
        plot_start_time,
        nonsystemic_treatments,
        log_axes[0],
        detected_args=detected_args,
        lesion_args=lesion_args,
        misc_args=misc_args
    )

    cone_color_list = {
        'A': 'lightblue',
        'B': 'lightgreen',
        'C': 'pink'
    }

    # --- Plot Log Simulation ---
    for lesion_index in range(lesion_dict["num_lesions"]):
        if lesion_dict["simulate"][lesion_index] and simulation_dates[lesion_index] is not None:
            log_axes[0].plot(simulation_dates[lesion_index], log_simulation_data[lesion_index], color=lesion_color_list[lesion_index, :], linestyle='-',
                        linewidth=simulation_line_width)
            if cone_settings["method"] == COMPARISON_CONE and lesion_index == cone_lesion_index and lesion_dict['simulate'][lesion_index]:
                for regimen, bounds_data in regimen_data_store.items():
                    dates = bounds_data['days']
                    log_min_data = bounds_data['log_min_data']
                    log_avg_data = bounds_data['log_avg_data']
                    log_max_data = bounds_data['log_max_data']
                    log_axes[0].plot(dates, log_min_data, color=cone_color_list[regimen], linestyle="-", linewidth=simulation_line_width, alpha=0.3)
                    log_axes[0].plot(dates, log_avg_data, color=cone_color_list[regimen], linestyle="--", linewidth=simulation_line_width, alpha=0.3)
                    log_axes[0].plot(dates, log_max_data, color=cone_color_list[regimen], linestyle="-", linewidth=simulation_line_width, alpha=0.3)
                    log_axes[0].fill_between(dates, log_min_data, log_max_data, color=cone_color_list[regimen], alpha=0.2)

    # Final configurations for setting x and y limits for volume plot
    # if override_y_max > 1e-9:
    #     y_max = override_y_max
    normal_axes[0].set_ylim([normal_y_min, normal_y_max])
    normal_axes[0].set_xlim([plot_start_time - 30, x_limit])
    log_axes[0].set_ylim([log_y_min, log_y_max])
    log_axes[0].set_xlim([plot_start_time - 30, x_limit])

    # TODO: Create detect line variable (is there already a detect size?)
    # --- Add Vertical Date Lines ---
    normal_detect_line = normal_axes[0].axhline(0.003, color='black', linewidth=1, linestyle='--', alpha=0.65,
                                label='Detect Limit')
    normal_line_collect.append(normal_detect_line)
    log_detect_line = log_axes[0].axhline(np.log10(0.003), color="black", linewidth=1, linestyle="--", alpha=0.65, label="Detect Limit")
    log_line_collect.append(log_detect_line)

    if notable_dates_dict["ETBdates"] is not None:
        for date in notable_dates_dict["ETBdates"]:
            normal_etb_line = normal_axes[0].axvline((date - lesion_dict["dos"]).days, color='red', linestyle='dashed', linewidth=1,
                                    alpha=1, label='ETB')
            normal_line_collect.append(normal_etb_line)
            log_etb_line = log_axes[0].axvline((date - lesion_dict["dos"]).days, color='red', linestyle='dashed', linewidth=1,
                                    alpha=1, label='ETB')
            log_line_collect.append(log_etb_line)
            # normal_axes[1].axvline((date - lesion_dict["dos"]).days, color='red', linestyle='dashed', linewidth=1,
            #                 alpha=1, zorder=1)
    if notable_dates_dict["NextScans"] is not None:
        for date in notable_dates_dict["NextScans"]:
            normal_scan_line = normal_axes[0].axvline((date-lesion_dict["dos"]).days, color='green', linestyle='solid', linewidth=1,
                                        alpha=1, label='Next')
            normal_line_collect.append(normal_scan_line)
            log_scan_line = log_axes[0].axvline((date-lesion_dict["dos"]).days, color='green', linestyle='solid', linewidth=1,
                                        alpha=1, label='Next')
            log_line_collect.append(log_scan_line)
            # normal_axes[1].axvline((date - lesion_dict["dos"]).days, color='green', linestyle='solid', linewidth=1,
            #                 alpha=1, zorder=1)
    if notable_dates_dict["Expired"] is not None:
        for date in notable_dates_dict["Expired"]:
            normal_expired_line = normal_axes[0].axvline((date-lesion_dict["dos"]).days, color='orange', linestyle='dashdot',
                                            linewidth=1, alpha=1, label='Expired')
            normal_line_collect.append(normal_expired_line)
            log_expired_line = log_axes[0].axvline((date-lesion_dict["dos"]).days, color='orange', linestyle='dashdot',
                                            linewidth=1, alpha=1, label='Expired')
            log_line_collect.append(log_expired_line)
            # normal_axes[1].axvline((date - lesion_dict["dos"]).days, color='orange', linestyle='dashdot', linewidth=1,
            #                 alpha=1, zorder=1)

    normal_axes[0].legend(handles=normal_line_collect, loc='upper center', ncol=len(normal_line_collect))
    log_axes[0].legend(handles=log_line_collect, loc='upper center', ncol=len(log_line_collect))

    progress.emit(95)
    time.sleep(0.05)

    # --- Create Treatment plot ---
    merged_treatments = []
    current_start = tx_dict['days_to_start'][0]
    current_end = tx_dict['days_to_end'][0]

    for start, end in zip(tx_dict['days_to_start'][1:], tx_dict['days_to_end'][1:]):
        if start <= current_end:  # There is an overlap
            current_end = max(current_end, end)  # Merge the treatments
        else:
            merged_treatments.append((current_start, current_end))
            current_start = start
            current_end = end

    merged_treatments.append((current_start, current_end))

    if cone_settings["method"] == NO_CONE:
        normal_axes[1], log_axes[1] = format_treatment_plot(
            tx_dict,
            assigned_tx_rows,
            x_limit,
            lesion_marker_size,
            normal_axes[1],
            log_axes[1],
            nonsystemic_treatments
        )
    else:
        normal_axes[1], log_axes[1] = format_treatment_plot(
            tx_dict,
            assigned_tx_rows,
            x_limit,
            lesion_marker_size,
            normal_axes[1],
            log_axes[1],
            nonsystemic_treatments,
            extra_treatment=cone_settings,
            cone_colors=cone_color_list,
            dos=lesion_dict["dos"]
        )

    normal_figure.tight_layout(pad=2.5)
    log_figure.tight_layout(pad=2.5)

    modeling_dict = {
        'normal_plot': [normal_figure, normal_axes],
        'log_plot':  [log_figure, log_axes],
        'bar_data': merged_treatments
    }

    progress.emit(100)

    return modeling_dict
