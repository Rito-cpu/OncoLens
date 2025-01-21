import sys
import math
import os
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib
import warnings
warnings.filterwarnings( "ignore")#, module = "matplotlib\..*" )

from PyQt6.QtCore import pyqtSignal, QObject
from matplotlib.patches import Rectangle
from dataclasses import dataclass, field
from scipy.integrate import odeint
from datetime import datetime

# matplotlib.use("agg")


def isTreatmentSegment(date_segment, treatment_dates):
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


def gdrs_modeling(init_state, time_range, *params):
    """GDRS equation method to be used with odeint"""
    current_dates, tx_dates, tx_IDS, is_active_tx, gamma, delta, res_array, sens_array = params

    init_size = init_state[0]
    tx_efficacies = init_state[1:]
    modeled_efficacies = np.zeros(len(tx_efficacies))
    treatment_killsum = 0
    rs_switch = np.zeros(len(tx_efficacies))

    for index in range(len(tx_IDS)):
        if is_active_tx[index]:
            formatted_ID = tx_IDS[index] - 1
            drug_stat = isTreatmentSegment(current_dates, tx_dates[index, :])
            if drug_stat:
                rs_switch[formatted_ID] = 1
            treatment_killsum = treatment_killsum + delta[index] * gamma * tx_efficacies[formatted_ID] * drug_stat

    for index in range(len(tx_efficacies)):
        if rs_switch[index]:
            modeled_efficacies[index] = -tx_efficacies[index] * res_array[index]
        else:
            modeled_efficacies[index] = tx_efficacies[index] * sens_array[index] * (1 - tx_efficacies[index])

    modeled_size = init_size * (gamma - treatment_killsum)
    modeled_state = np.append(modeled_size, modeled_efficacies)

    return modeled_state   # Returning [dT dE dE ... dE]


@dataclass
class ModelETB:
    # --- File error attributes ---
    _file_error: bool = False
    _file_error_message: str = ''

    # --- File check attributes ---
    _has_data: bool = False     # Boolean to let us know if there is old data and we need to reset data
    excel_file_path: str = None
    excel_file: pd.ExcelFile = None
    _num_sheets = 4
    _sheet_names = {0: 'notable_dates',
                    1: 'historical_treatment',
                    2: 'available_treatment',
                    3: 'clinician_data'}

    # --- Data that will help set up GUI page ---
    _lesion_data: dict = field(default_factory=lambda: {})   # list = field(default_factory=lambda: [])
    _historical_treatment_data: dict = field(default_factory=lambda: {})   # list = field(default_factory=lambda: [])
    _available_treatment_data: dict = field(default_factory=lambda: {})   # list = field(default_factory=lambda: [])

    # --- Modeling Process Variables ---
    general_options: list = field(default_factory=lambda: [])
    lesion_dict: dict = field(default_factory=lambda: {})
    tx_dict: dict = field(default_factory=lambda: {})
    matrix_dict: dict = field(default_factory=lambda: {})
    _detect_size: float = 3e6/1e9
    _death_threshold = 1e-11
    _detect_line = 0.003

    def initiate_excel_check(self, file_path: str) -> None:
        # Not included in __init__ so we can call this whenever we have a new excel sheet
        # No need to create more objects when we can reuse this one
        self._valid_file_check(file_path)

    def _valid_file_check(self, file_path) -> None:
        if os.path.exists(file_path):
            excel_file = pd.ExcelFile(file_path)
            current_sheet_names = excel_file.sheet_names

            # --- Uneven sheet number ---
            if len(current_sheet_names) < self._num_sheets:
                self._file_error_message = 'Excel file quick check failed: Length issue!'
                self._file_error = True
            # --- Sheet names are not the same ---
            elif not set(self._sheet_names.values()).issubset(set(current_sheet_names)):
                # TODO: if sheet names are not the same but the sheet number is correct - check if the sheets are
                #  actually what we want (name may be misspelled)
                self._file_error_message = 'Excel file quick check failed: Sheet name issue!'
                self._file_error = True
            # --- Correct file passed ---
            else:
                # self.excel_file = excel_file
                self._file_data_check(file_path, excel_file)
        # --- File does not exist ---
        else:
            self._file_error_message = 'Excel file quick check failed: File does not exist!'
            self._file_error = True

    def _file_data_check(self, file_path, excel_file) -> None:
        historical_treatment_headers = ['Name', 'Abbr', 'DateOn', 'DateOff', 'TxID', 'Active']
        available_treatment_headers = ['Name', 'Abbr']
        clinician_data_headers = ['Name', 'Abbr', 'RECIST']

        # --- Notable_dates check ---
        notable_dates_sheet = excel_file.parse(self._sheet_names[0])

        # --- Historical treatment check ---
        historical_treatment_test = excel_file.parse(self._sheet_names[1], header=0)
        for header in historical_treatment_headers:
            if header in historical_treatment_test.columns:
                if len(historical_treatment_test[header]) == 0:
                    self._file_error_message = f'Required column name \'{header}\' is empty in sheet ' \
                                                f'\'{self._sheet_names[1]}\'!'
                    self._file_error = True
                elif historical_treatment_test[header].isnull().values.any():
                    self._file_error_message = f'Column \'{header}\' in sheet \'{self._sheet_names[1]}\' contains an ' \
                                                f'empty value - uneven column size!'
                    self._file_error = True
            else:
                self._file_error_message = f'Required column name \'{header}\' does not exist in sheet ' \
                                            f'\'{self._sheet_names[1]}\'!'
                self._file_error = True

        # --- Available treatment check ---
        available_treatment_test = excel_file.parse(self._sheet_names[2], header=0)
        for header in available_treatment_headers:
            if header not in available_treatment_test.columns:
                self._file_error_message = f'Missing required column \'{header}\' in sheet \'{self._sheet_names[2]}\''
                self._file_error = True
            elif available_treatment_test[header].isnull().values.any():
                self._file_error_message = f'Column \'{header}\' in sheet \'{self._sheet_names[2]}\' contains an empty ' \
                                            f'value - uneven column size!'
                self._file_error = True

        # --- Clinician data check ---
        clinician_volume_data = excel_file.parse(self._sheet_names[3], header=0)
        clinician_lesion_data = excel_file.parse(self._sheet_names[3], header=1, usecols=lambda x: 'Volume' not in x)
        for header in clinician_data_headers:
            if header in clinician_lesion_data.columns:
                if len(clinician_lesion_data[header]) == 0:
                    self._file_error_message = f'Error'
                    self._file_error = True
                elif clinician_lesion_data[header].isnull().values.any():
                    self._file_error_message = f'Error'
                    self._file_error = True
            else:
                self._file_error_message = 'Error'
                self._file_error = True

        if not self._file_error:
            # TODO: Can we create a dictionary for storing model options?
            if self._has_data:
                self.reset_data()
            self._has_data = True
            self.excel_file_path = file_path
            self.excel_file = excel_file
            self._lesion_data = {'Name': clinician_lesion_data['Name'],
                                'Abbr': clinician_lesion_data['Abbr']}

            self._historical_treatment_data = {'Name': historical_treatment_test['Name'],
                                                'Abbr': historical_treatment_test['Abbr'],
                                                'On': historical_treatment_test['DateOn'],
                                                'Off': historical_treatment_test['DateOff']}

            self._available_treatment_data = {'Name': available_treatment_test['Name'],
                                                'Abbr': available_treatment_test['Abbr']}

    def initiate_data_import(self, model_options: list[dict], progress: pyqtSignal):
        self.general_options, self.lesion_dict, self.tx_dict, self.matrix_dict = model_options

        self.tx_dict["num_tx"] = len(self.tx_dict["abbr"])
        self.tx_dict["plot"] = np.ones(self.tx_dict["num_tx"])

        progress.emit(1)
        time.sleep(0.05)

        # --- Retrieve more lesion data from Excel sheets ---
        lesion_scan_df = pd.read_excel(self.excel_file_path, sheet_name="clinician_data", header=0)
        lesion_info_df = pd.read_excel(self.excel_file_path, sheet_name="clinician_data", header=1)
        lesion_data = lesion_info_df.to_numpy()

        if lesion_data.shape[0] == 0 or lesion_data.shape[1] <= 3:
            sys.exit(f"Clinician data does not meet minimum requirements. Missing values and/or columns.")

        lesion_vol_headers = 1
        self.lesion_dict["num_lesions"] = len(self.lesion_dict["abbr"])
        # self.lesion_dict["scan_dates"] = pd.to_datetime(lesion_scan_df.columns[lesion_scan_df.iloc[0] == "Volume"])
        temp_date_list = []
        for date in lesion_scan_df.columns[lesion_scan_df.iloc[0] == "Volume"]:
            temp_date_list.append(date)
        self.lesion_dict["scan_dates"] = pd.to_datetime(temp_date_list)
        self.lesion_dict["num_scans"] = len(self.lesion_dict["scan_dates"])
        self.lesion_dict["dos"] = min(self.lesion_dict["scan_dates"][0], self.tx_dict["date_on"][0])

        # --- Format Matrix ---
        tx_switch_array = []
        counter = 0
        for name in self.tx_dict["abbr"]:
            switch_values = []
            if name.lower() == "rad" or name.lower() == "surg":
                if counter <= len(self.matrix_dict["array"]):
                    switch_values = self.matrix_dict["array"][counter]
                    counter += 1
                else:
                    print("Out of bounds for nonsystemic treatments - redo matrix!")
                    break
            else:
                switch_values = np.ones(self.lesion_dict["num_lesions"])
            tx_switch_array.append(switch_values)
        self.matrix_dict["array"] = np.array(tx_switch_array)

        # --- Gather scan date volumes ---
        self.lesion_dict["recist"] = []
        lesion_volumes = []
        for index in range(self.lesion_dict["num_lesions"]):
            self.lesion_dict["recist"].append(lesion_data[index, 2])
            volume_instance = []
            for current_date in self.lesion_dict["scan_dates"]:
                column_index = lesion_scan_df.columns.get_loc(current_date)
                scan_vol = lesion_scan_df.iloc[index+1, column_index]
                if isinstance(scan_vol, str):
                    scan_vol = np.nan
                elif scan_vol == 0 or scan_vol < 0:
                    scan_vol = 0.99 * self._detect_size
                volume_instance.append(scan_vol)
            lesion_volumes.append(volume_instance)
        lesion_volumes = np.asarray(lesion_volumes)

        # --- Gather notable dates from Excel sheet ---
        notable_dates_df = pd.read_excel(self.excel_file_path, sheet_name="notable_dates", header=0)
        header_names = ["ETBdates", "NextScans", "Expired"]
        notable_dates_dict = {
            "ETBdates": pd.to_datetime(notable_dates_df[header_names[0]]).dropna() if notable_dates_df[header_names[0]].count() != 0 else None,
            "NextScans": pd.to_datetime(notable_dates_df[header_names[1]]).dropna() if notable_dates_df[header_names[1]].count() != 0 else None,
            "Expired": pd.to_datetime(notable_dates_df[header_names[2]]).dropna() if notable_dates_df[header_names[2]].count() != 0 else None
        }

        # --- Find maximum volume for plot ---
        normal_y_max = 0

        for index in range(self.lesion_dict["num_lesions"]):
            if self.lesion_dict["plot"][index]:
                temp_max = np.nanmax(lesion_volumes[index])
                if temp_max is not np.nan and temp_max > normal_y_max:
                    normal_y_max = temp_max
        y_max_holder = normal_y_max

        progress.emit(15)
        time.sleep(0.05)

        # --- Calculate days between treatment start and end dates ---
        self.tx_dict["days_to_start"] = []
        self.tx_dict["days_to_end"] = []
        for start_date, end_date in zip(self.tx_dict["date_on"], self.tx_dict["date_off"]):
            day_delta = (start_date - self.lesion_dict["dos"]).days
            self.tx_dict["days_to_start"].append(day_delta)
            day_delta = (end_date - self.lesion_dict["dos"]).days
            self.tx_dict["days_to_end"].append(day_delta)

        # --- Calculate duration of each treatment ---
        self.tx_dict["duration"] = [end-start for start, end in zip(self.tx_dict["days_to_start"], self.tx_dict["days_to_end"])]

        progress.emit(25)
        time.sleep(0.03)

        # --- Sort day delta in arrays while keeping original indexes ---

        # --- Create treatment plot settings ---
        assigned_tx_rows, max_rows = self.create_tx_plot_settings()

        progress.emit(45)
        time.sleep(0.05)

        # --- GDRS Model variable prep ---
        active_tx = np.ones(self.tx_dict["num_tx"])
        self.tx_dict["joined_dates"] = np.array([self.tx_dict["date_on"], self.tx_dict["date_off"]]).T
        unique_tx_dates = np.unique(self.tx_dict["joined_dates"], axis=0)
        holder = np.unique(unique_tx_dates.flatten())
        unique_all_dates = np.concatenate((holder, self.lesion_dict["scan_dates"]), axis=0)
        unique_all_dates = np.unique(unique_all_dates)
        holder = unique_all_dates[len(unique_all_dates)-1] + np.timedelta64(1, "D")
        t_breaks = np.append(unique_all_dates, holder)
        t_end = max(unique_all_dates) + np.timedelta64(80, "D")
        t_end_index = np.argwhere(t_end <= t_breaks).flatten()
        if len(t_end_index) == 0:
            t_breaks = np.append(t_breaks, t_end)
        else:
            t_end_index = t_end_index[0]
            t_breaks = np.append(t_breaks[0:t_end_index], t_end)
        simulation_dates, simulation_data = [None] * self.lesion_dict["num_lesions"], [None] * self.lesion_dict["num_lesions"]
        sim_max = 1e-11

        progress.emit(55)
        time.sleep(0.05)

        # --- Targeting lesions with radiation and surgery ---
        # matrix_tx_rows = self.matrix_dict["dataframe"].index
        matrix_tx_rows = self.tx_dict["abbr"]
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

        for lesion in range(self.lesion_dict["num_lesions"]):
            if nonsystemic_treatments["surgery"]:
                for s in nonsystemic_treatments["surgery"]:
                    if self.matrix_dict["array"][s, lesion] == 1:
                        nonsystemic_treatments["surgery_index"].append(lesion) if lesion not in nonsystemic_treatments["surgery_index"] else None
            if nonsystemic_treatments["radiation"]:
                for r in nonsystemic_treatments["radiation"]:
                    if self.matrix_dict["array"][r, lesion] == 1:
                        nonsystemic_treatments["radiation_index"].append(lesion) if lesion not in nonsystemic_treatments["radiation_index"] else None

        les_scan_removal = {}
        if self.general_options["clean_lesions"]:
            if len(nonsystemic_treatments["radiation_index"]) != 0:
                for target in nonsystemic_treatments["radiation_index"]:
                    for tx in nonsystemic_treatments["radiation"]:
                        if self.matrix_dict["array"][tx, target] == 1:
                            les_scan_removal[target] = []
                            for index, date in enumerate(self.lesion_dict["scan_dates"]):
                                if date > self.tx_dict["joined_dates"][tx][1]:
                                    les_scan_removal[target].append(index)
                            break
            if len(nonsystemic_treatments["surgery_index"]) != 0:
                for lesion_index in nonsystemic_treatments["surgery_index"]:
                    for tx in nonsystemic_treatments["surgery"]:
                        if self.matrix_dict["array"][tx, lesion_index] == 1:
                            les_scan_removal[lesion_index] = []
                            for index, date in enumerate(self.lesion_dict["scan_dates"]):
                                if date > self.tx_dict["joined_dates"][tx][1] and index not in les_scan_removal[lesion_index]:
                                    les_scan_removal[lesion_index].append(index)
                            break

        progress.emit(70)
        time.sleep(0.05)

        # --- Model GDRS ---
        # self.model_GDRS(all_volumes)
        for lesion_index in range(self.lesion_dict["num_lesions"]):
            if self.lesion_dict["simulate"][lesion_index]:
                existing_lesion_index = np.argwhere(~pd.isna(lesion_volumes[lesion_index])).flatten()
                model_gamma = self.lesion_dict["growth"][lesion_index] * self.lesion_dict["growth_mults"][lesion_index]
                model_delta = (self.tx_dict["efficacy"] * self.lesion_dict["efficacy_mults"][lesion_index]) * self.matrix_dict["array"][:, lesion_index].T
                model_res = self.tx_dict["resistance"] * self.lesion_dict["resistance_mults"][lesion_index]
                model_sens = self.tx_dict["sensitivity"] * self.lesion_dict["sensitivity_mults"][lesion_index]

                initial_state = np.ones(self.tx_dict["num_tx"]+1)
                initial_state[0] = 0
                ys, xs = [], [0]

                volume_start_index = existing_lesion_index[0]
                lesion_exist = np.argwhere(t_breaks == self.lesion_dict["scan_dates"][volume_start_index]).flatten()

                for index, date in enumerate(t_breaks[:-1]):
                    if date == unique_all_dates[lesion_exist]:
                        initial_state[0] = lesion_volumes[lesion_index][volume_start_index] * (10**self.lesion_dict["offset"][lesion_index])
                        ys.append(initial_state[0])
                    first_date = (t_breaks[index] - self.lesion_dict["dos"]).days
                    second_date = (t_breaks[index+1] - self.lesion_dict["dos"]).days
                    step_size = (second_date-first_date) # * 2    # Half-a-day
                    time_range = np.linspace(first_date, second_date, step_size+1)
                    current_dates = np.array([t_breaks[index], t_breaks[index+1]])
                    params = (current_dates, self.tx_dict["joined_dates"], self.tx_dict["id_list"], active_tx, model_gamma, model_delta, model_res, model_sens)
                    ode_result = odeint(gdrs_modeling, initial_state, time_range, args=params)
                    initial_state = ode_result[-1, :]
                    ys.append(ode_result[1:, 0])
                    xs.append(time_range[1:])
                    if initial_state[0] < self._death_threshold:
                        initial_state[0] = 0
                ys, xs = np.hstack(ys), np.hstack(xs)
                first_time = (np.argwhere(xs == (self.lesion_dict["scan_dates"][volume_start_index] - self.lesion_dict["dos"]).days)).flatten()
                first_time = first_time[0]
                simulation_dates[lesion_index] = xs[first_time:]
                ys = np.where(ys == 0, 10**-10, ys)
                simulation_data[lesion_index] = ys[first_time:]
                sim_max = max(sim_max, max(ys))

        progress.emit(85)
        time.sleep(0.05)

        # --- defining matplotlib parameters  ---
        tx_color_list = plt.cm.turbo(np.linspace(0, 1, self.tx_dict["num_tx"] + 1))
        tx_color_list[:, 1] = tx_color_list[:, 1] * 0.85
        lesion_color_list = plt.cm.turbo(np.linspace(0, 1, self.lesion_dict["num_lesions"] + 1))
        lesion_color_list[:, 1] = lesion_color_list[:, 1] * 0.85
        x_limit = (t_end - self.lesion_dict["dos"]).days
        plot_start_time = 0 - x_limit * 0.05
        detected_lesion_offset_ticks = np.zeros(self.lesion_dict["num_scans"])
        text_offset_mult = 0.028
        xAxisDateTextOffsetMult = 0.2
        detected_lesion_offset_mult = 0.3
        upper_buffer_mult_y_max = 1.05  # 0.447
        legend_buffer_y_max = 0.15
        text_size = 10
        lesion_marker_size = 11
        detected_lesion_marker_size = 12
        detected_lesion_marker_width = 2
        endDateTextOffset = math.ceil(self.lesion_dict["num_lesions"] / 2)  # 3.1
        up_down_OS = 0.2
        maxSchedPlot = 0.2
        simulation_line_width = 1.75
        label_percent_OS = 3
        plot_up_lesion_list = np.zeros(self.lesion_dict["num_lesions"])
        normal_line_collect = []

        # --- Prepare Log parameters ---
        normal_y_min = 0
        normal_y_max *= upper_buffer_mult_y_max
        normal_y_max = normal_y_max + (normal_y_max - normal_y_min) * legend_buffer_y_max
        text_offset = (normal_y_max - normal_y_min) * text_offset_mult
        detected_lesion_offset = 0
        """
        if self.general_options["apply_log"]:
            for lesion_index in range(self.lesion_dict["num_lesions"]):
                if self.lesion_dict["simulate"][lesion_index] and simulation_data[lesion_index] is not None:
                    with np.errstate(invalid='ignore'): # Some values are calculated to be neg and have log10 applied
                        simulation_data[lesion_index] = np.where(simulation_data[lesion_index] != 0, np.log10(simulation_data[lesion_index]), 0)
                for column_index in range(len(lesion_volumes[lesion_index])):
                    log_volume = np.log10(lesion_volumes[lesion_index][column_index])
                    lesion_volumes[lesion_index][column_index] = log_volume
            modifiable_detect_size = np.log10(self._detect_size)
            normal_y_min = modifiable_detect_size - min_lower_buffer_log_y
            normal_y_min = max(normal_y_min, -9.5)
            normal_y_max = np.log10(max(y_max_holder, sim_max)) * upper_buffer_mult_y_max
            normal_y_max = min(normal_y_max, 4)
            normal_y_max = normal_y_max + (normal_y_max - normal_y_min) * legend_buffer_y_max
            text_offset = -(normal_y_max - normal_y_min) * text_offset_mult
            detected_lesion_offset = text_offset * detected_lesion_offset_mult
        """
        lesion_text_offset_ticks = np.zeros(self.lesion_dict["num_scans"]) - text_offset

        # --- Setup Plot ---
        normal_fig, normal_axes = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [4, 1]})
        log_fig, log_axes = plt.subplots(2, 1, figsize=(8, 8), gridspec_kw={'height_ratios': [4, 1]})

        plot_title = os.path.split(self.excel_file_path)[1]
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
        yPlotValMin = normal_y_min
        for lesion_index in range(self.lesion_dict["num_lesions"]):
            lesion_label_needed = True
            if self.lesion_dict["plot"][lesion_index]:
                if self.general_options["clean_lesions"]:
                    firstInstance = np.argwhere(~pd.isna(lesion_volumes[lesion_index])).flatten()
                    firstInstance = firstInstance[0]
                    plotCondition = lesion_index in les_scan_removal.keys()#  and len(lesScanRemoval[li]) != 0
                for scan_index in range(self.lesion_dict["num_scans"]):
                    if (self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days >= plot_start_time:
                        if self.general_options["clean_lesions"]:
                            if plotCondition and scan_index == firstInstance:
                                if lesion_index in nonsystemic_treatments["surgery_index"]:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index], color='gold',
                                                marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                                elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index], color='black',
                                                marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                            elif plotCondition and scan_index in les_scan_removal[lesion_index]:
                                continue
                            # Plot everything else normally
                            if lesion_volumes[lesion_index][scan_index] <= self._detect_size:
                                normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days,
                                            lesion_volumes[lesion_index][scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                            color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                            linewidth=detected_lesion_marker_width)
                                detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                            # Plot normal points
                            else:
                                if self.lesion_dict["recist"][lesion_index]:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index],
                                                color=lesion_color_list[lesion_index],
                                                marker='^', markersize=lesion_marker_size / 2)
                                else:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index],
                                                color=lesion_color_list[lesion_index],
                                                marker='.', markersize=lesion_marker_size)
                            if lesion_label_needed and ~np.isnan(lesion_volumes[lesion_index][scan_index]):
                                if lesion_volumes[lesion_index][scan_index] <= self._detect_size:
                                    yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                    if yPlotVal + text_offset < yPlotValMin:
                                        yPlotValMin = yPlotVal + text_offset
                                        normal_y_min = yPlotValMin
                                    normal_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS, yPlotVal,
                                                self.lesion_dict["abbr"][lesion_index],
                                                fontsize=text_size, color=lesion_color_list[lesion_index],
                                                horizontalalignment='right')
                                    lesion_label_needed = False
                                    lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                                else:
                                    yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset
                                    normal_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS,
                                                yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                                self.lesion_dict["abbr"][lesion_index], fontsize=text_size,
                                                color=lesion_color_list[lesion_index],
                                                horizontalalignment='right')
                                    lesion_label_needed = False
                        else:
                            # X'ing out small points
                            if lesion_volumes[lesion_index][scan_index] <= self._detect_size:
                                normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days,
                                            lesion_volumes[lesion_index][scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                            color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                            linewidth=detected_lesion_marker_width)
                                detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                            # Plot normal points
                            else:
                                if lesion_index in nonsystemic_treatments["surgery_index"]:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index], color='gold',
                                                marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                                elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index], color='black',
                                                marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                                if self.lesion_dict["recist"][lesion_index]:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                                marker='^', markersize=lesion_marker_size / 2)
                                else:
                                    normal_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                                marker='.', markersize=lesion_marker_size)
                            if lesion_label_needed and ~np.isnan(lesion_volumes[lesion_index][scan_index]):
                                if lesion_volumes[lesion_index][scan_index] <= self._detect_size:
                                    yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                    if yPlotVal + text_offset < yPlotValMin:
                                        yPlotValMin = yPlotVal + text_offset
                                        normal_y_min = yPlotValMin
                                    normal_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS, yPlotVal, self.lesion_dict["abbr"][lesion_index],
                                                fontsize=text_size, color=lesion_color_list[lesion_index], horizontalalignment='right')
                                    lesion_label_needed = False
                                    lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                                else:
                                    yPlotVal = lesion_volumes[lesion_index][scan_index] + text_offset
                                    normal_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS,
                                                yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                                self.lesion_dict["abbr"][lesion_index], fontsize=text_size, color=lesion_color_list[lesion_index],
                                                horizontalalignment='right')
                                    lesion_label_needed = False

        # --- Plot Lesion Sim ---
        for lesion_index in range(self.lesion_dict["num_lesions"]):
            if self.lesion_dict["simulate"][lesion_index] and simulation_dates[lesion_index] is not None:
                normal_axes[0].plot(simulation_dates[lesion_index], simulation_data[lesion_index], color=lesion_color_list[lesion_index, :], linestyle='-',
                            linewidth=simulation_line_width)

        # --- Create Log variables ---
        # /Users/4474613/Documents/ETB-Excel-Module/etb10_updated.xlsx
        log_line_collect = []
        log_lesion_volumes = lesion_volumes
        log_simulation_data = simulation_data
        min_lower_buffer_log_y = 1
        detected_lesion_offset_ticks = np.zeros(self.lesion_dict["num_scans"])
        for lesion_index in range(self.lesion_dict["num_lesions"]):
            if self.lesion_dict["simulate"][lesion_index] and simulation_data[lesion_index] is not None:
                with np.errstate(invalid='ignore'): # Some values are calculated to be neg and have log10 applied
                        log_simulation_data[lesion_index] = np.where(simulation_data[lesion_index] != 0, np.log10(simulation_data[lesion_index]), 0)
                for column_index in range(len(lesion_volumes[lesion_index])):
                    log_volume = np.log10(lesion_volumes[lesion_index][column_index])
                    log_lesion_volumes[lesion_index][column_index] = log_volume
            log_detect_size = np.log10(self._detect_size)
            log_y_min = log_detect_size - min_lower_buffer_log_y
            log_y_min = max(log_y_min, -9.5)
            log_y_max = np.log10(max(y_max_holder, sim_max)) * upper_buffer_mult_y_max
            log_y_max = min(log_y_max, 4)
            log_y_max = log_y_max + (log_y_max - log_y_min) * legend_buffer_y_max
            log_text_offset = -(log_y_max - log_y_min) * text_offset_mult
            log_detected_lesion_offset = log_text_offset * detected_lesion_offset_mult
        lesion_text_offset_ticks = np.zeros(self.lesion_dict["num_scans"]) - text_offset

        # --- Plot Log Scans ---
        yPlotValMin = log_y_min
        for lesion_index in range(self.lesion_dict["num_lesions"]):
            lesion_label_needed = True
            if self.lesion_dict["plot"][lesion_index]:
                if self.general_options["clean_lesions"]:
                    firstInstance = np.argwhere(~pd.isna(log_lesion_volumes[lesion_index])).flatten()
                    firstInstance = firstInstance[0]
                    plotCondition = lesion_index in les_scan_removal.keys()#  and len(lesScanRemoval[li]) != 0
                for scan_index in range(self.lesion_dict["num_scans"]):
                    if (self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days >= plot_start_time:
                        if self.general_options["clean_lesions"]:
                            if plotCondition and scan_index == firstInstance:
                                if lesion_index in nonsystemic_treatments["surgery_index"]:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='gold',
                                                marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                                elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='black',
                                                marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                            elif plotCondition and scan_index in les_scan_removal[lesion_index]:
                                continue
                            # Plot everything else normally
                            if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                                log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days,
                                            log_lesion_volumes[lesion_index][scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                            color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                            linewidth=detected_lesion_marker_width)
                                detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                            # Plot normal points
                            else:
                                if self.lesion_dict["recist"][lesion_index]:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index],
                                                color=lesion_color_list[lesion_index],
                                                marker='^', markersize=lesion_marker_size / 2)
                                else:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index],
                                                color=lesion_color_list[lesion_index],
                                                marker='.', markersize=lesion_marker_size)
                            if lesion_label_needed and ~np.isnan(log_lesion_volumes[lesion_index][scan_index]):
                                if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                                    yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                    if yPlotVal + text_offset < yPlotValMin:
                                        yPlotValMin = yPlotVal + text_offset
                                        log_y_min = yPlotValMin
                                    log_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS, yPlotVal,
                                                self.lesion_dict["abbr"][lesion_index],
                                                fontsize=text_size, color=lesion_color_list[lesion_index],
                                                horizontalalignment='right')
                                    lesion_label_needed = False
                                    lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                                else:
                                    yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset
                                    log_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS,
                                                yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                                self.lesion_dict["abbr"][lesion_index], fontsize=text_size,
                                                color=lesion_color_list[lesion_index],
                                                horizontalalignment='right')
                                    lesion_label_needed = False
                        else:
                            # X'ing out small points
                            if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                                log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days,
                                            log_lesion_volumes[lesion_index][scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index],
                                            color=lesion_color_list[lesion_index, :], marker='x', markersize=detected_lesion_marker_size,
                                            linewidth=detected_lesion_marker_width)
                                detected_lesion_offset_ticks[scan_index] = detected_lesion_offset_ticks[scan_index] + 1
                            # Plot normal points
                            else:
                                if lesion_index in nonsystemic_treatments["surgery_index"]:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='gold',
                                                marker='*', markersize=lesion_marker_size * 2, alpha=0.3)
                                elif lesion_index in nonsystemic_treatments["radiation_index"]:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color='black',
                                                marker='D', markersize=lesion_marker_size*0.75, alpha=0.3)
                                if self.lesion_dict["recist"][lesion_index]:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                                marker='^', markersize=lesion_marker_size / 2)
                                else:
                                    log_axes[0].plot((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days, log_lesion_volumes[lesion_index][scan_index], color=lesion_color_list[lesion_index],
                                                marker='.', markersize=lesion_marker_size)
                            if lesion_label_needed and ~np.isnan(log_lesion_volumes[lesion_index][scan_index]):
                                if log_lesion_volumes[lesion_index][scan_index] <= log_detect_size:
                                    yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset * lesion_text_offset_ticks[scan_index] + log_detected_lesion_offset * detected_lesion_offset_ticks[scan_index]
                                    if yPlotVal + text_offset < yPlotValMin:
                                        yPlotValMin = yPlotVal + text_offset
                                        log_y_min = yPlotValMin
                                    log_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS, yPlotVal, self.lesion_dict["abbr"][lesion_index],
                                                fontsize=text_size, color=lesion_color_list[lesion_index], horizontalalignment='right')
                                    lesion_label_needed = False
                                    lesion_text_offset_ticks[scan_index] = lesion_text_offset_ticks[scan_index] + 1
                                else:
                                    yPlotVal = log_lesion_volumes[lesion_index][scan_index] + text_offset
                                    log_axes[0].text((self.lesion_dict["scan_dates"][scan_index] - self.lesion_dict["dos"]).days - label_percent_OS,
                                                yPlotVal + up_down_OS * plot_up_lesion_list[lesion_index],
                                                self.lesion_dict["abbr"][lesion_index], fontsize=text_size, color=lesion_color_list[lesion_index],
                                                horizontalalignment='right')
                                    lesion_label_needed = False

        # --- Plot Log Simulation ---
        for lesion_index in range(self.lesion_dict["num_lesions"]):
            if self.lesion_dict["simulate"][lesion_index] and simulation_dates[lesion_index] is not None:
                log_axes[0].plot(simulation_dates[lesion_index], log_simulation_data[lesion_index], color=lesion_color_list[lesion_index, :], linestyle='-',
                            linewidth=simulation_line_width)

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
                normal_etb_line = normal_axes[0].axvline((date - self.lesion_dict["dos"]).days, color='red', linestyle='dashed', linewidth=1,
                                        alpha=1, label='ETB')
                normal_line_collect.append(normal_etb_line)
                log_etb_line = log_axes[0].axvline((date - self.lesion_dict["dos"]).days, color='red', linestyle='dashed', linewidth=1,
                                        alpha=1, label='ETB')
                log_line_collect.append(log_etb_line)
                # normal_axes[1].axvline((date - self.lesion_dict["dos"]).days, color='red', linestyle='dashed', linewidth=1,
                #                 alpha=1, zorder=1)
        if notable_dates_dict["NextScans"] is not None:
            for date in notable_dates_dict["NextScans"]:
                normal_scan_line = normal_axes[0].axvline((date-self.lesion_dict["dos"]).days, color='green', linestyle='solid', linewidth=1,
                                            alpha=1, label='Next')
                normal_line_collect.append(normal_scan_line)
                log_scan_line = log_axes[0].axvline((date-self.lesion_dict["dos"]).days, color='green', linestyle='solid', linewidth=1,
                                            alpha=1, label='Next')
                log_line_collect.append(log_scan_line)
                # normal_axes[1].axvline((date - self.lesion_dict["dos"]).days, color='green', linestyle='solid', linewidth=1,
                #                 alpha=1, zorder=1)
        if notable_dates_dict["Expired"] is not None:
            for date in notable_dates_dict["Expired"]:
                normal_expired_line = normal_axes[0].axvline((date-self.lesion_dict["dos"]).days, color='orange', linestyle='dashdot',
                                                linewidth=1, alpha=1, label='Expired')
                normal_line_collect.append(normal_expired_line)
                log_expired_line = log_axes[0].axvline((date-self.lesion_dict["dos"]).days, color='orange', linestyle='dashdot',
                                                linewidth=1, alpha=1, label='Expired')
                log_line_collect.append(log_expired_line)
                # normal_axes[1].axvline((date - self.lesion_dict["dos"]).days, color='orange', linestyle='dashdot', linewidth=1,
                #                 alpha=1, zorder=1)
        normal_axes[0].legend(handles=normal_line_collect, loc='upper center', ncol=len(normal_line_collect))
        log_axes[0].legend(handles=log_line_collect, loc='upper center', ncol=len(log_line_collect))

        progress.emit(95)
        time.sleep(0.05)

        # --- Create Treatment plot ---
        for index in range(self.tx_dict["num_tx"]):
            if self.tx_dict["plot"][index] == 1:
                start = self.tx_dict["days_to_start"][index]
                row_num = assigned_tx_rows[index] - 1
                length = self.tx_dict["duration"][index]
                name = self.tx_dict["abbr"][index]
                if start+length > x_limit:
                    new_length = x_limit - start
                    rectangle = Rectangle((start, row_num), new_length + 10, 1.0, color=tx_color_list[index], alpha=0.5,
                                        linewidth=0.5)
                    rectangle_dup = Rectangle((start, row_num), new_length + 10, 1.0, color=tx_color_list[index], alpha=0.5,
                                        linewidth=0.5)
                else:
                    rectangle = Rectangle((start, row_num), length, 1.0, color=tx_color_list[index], alpha=0.8, linewidth=0.5, zorder=2)
                    rectangle_dup = Rectangle((start, row_num), length, 1.0, color=tx_color_list[index], alpha=0.8, linewidth=0.5, zorder=2)
                normal_axes[1].add_patch(rectangle)
                log_axes[1].add_patch(rectangle_dup)
                rectangle_x, rectangle_y = rectangle.get_xy()
                center_x = rectangle_x + rectangle.get_width()/2
                center_y = rectangle_y + rectangle.get_height()/2
                normal_axes[1].annotate(name, (center_x, center_y), color='black', weight='bold', fontsize=7, ha='center', va='center', zorder=2)
                log_axes[1].annotate(name, (center_x, center_y), color='black', weight='bold', fontsize=7, ha='center', va='center', zorder=2)
                if index in nonsystemic_treatments["radiation"]:
                    normal_axes[1].plot(center_x, center_y+0.025, color='black', marker='D', alpha=0.3, markersize=lesion_marker_size*1.3, zorder=2)
                    log_axes[1].plot(center_x, center_y+0.025, color='black', marker='D', alpha=0.3, markersize=lesion_marker_size*1.3, zorder=2)
                elif index in nonsystemic_treatments["surgery"]:
                    normal_axes[1].plot(center_x, center_y+0.025, color='gold', marker='*', alpha=0.3, markersize=lesion_marker_size*2, zorder=2)
                    log_axes[1].plot(center_x, center_y+0.025, color='gold', marker='*', alpha=0.3, markersize=lesion_marker_size*2, zorder=2)

        normal_fig.tight_layout(pad=2.5)
        log_fig.tight_layout(pad=2.5)

        progress.emit(100)

        return normal_fig, normal_axes, log_fig, log_axes

    def create_tx_plot_settings(self):
        tx_order = np.arange(0, self.tx_dict["num_tx"], 1)
        assigned_tx_rows = np.zeros(self.tx_dict["num_tx"])
        min_tx_index = min(tx_order)
        assigned_tx_rows[min_tx_index] = 1
        max_row_assign = 1
        max_rows = 1

        for index in range(min_tx_index, self.tx_dict["num_tx"]):
            if self.tx_dict["plot"][index] == 1:
                need_assign = True
                row_assign = 1
                while need_assign:
                    more_than_all = True
                    chi = 0
                    for y in range(chi, index):
                        if assigned_tx_rows[y] == row_assign:
                            if self.tx_dict["days_to_start"][index] < self.tx_dict["days_to_end"][y]:
                                more_than_all = False
                    if more_than_all:
                        assigned_tx_rows[index] = row_assign
                        need_assign = False
                    else:
                        row_assign += 1
                        if row_assign > max_row_assign:
                            assigned_tx_rows[index] = row_assign
                            need_assign = False
                            max_row_assign += 1

        for row in assigned_tx_rows:
            if row > max_rows:
                max_rows = row

        return assigned_tx_rows, max_rows

    def has_file_error(self):
        return self._file_error

    def get_error_message(self):
        return self._file_error_message

    def get_file_path(self) -> str:
        return self.excel_file_path

    def get_file_name(self) -> str:
        tail = os.path.split(self.excel_file_path)
        return tail[1]

    def get_settings_data(self) -> list:
        return self._lesion_data, self._historical_treatment_data, self._available_treatment_data

    def set_detect_size(self, new_size: float) -> None:
        self._detect_size = new_size

    def reset_data(self):
        self._file_error = None
        self._file_error_message = None

        self.excel_file_path = None
        self.excel_file = None

        self._lesion_data = {}
        self._historical_treatment_data = {}
        self._available_treatment_data = {}

        print('Cleared data!')
