import numpy as np
import pandas as pd


class ExperimentParameters:
    def __init__(self, p_exp, temp_flow, sigma_methane, sigma_water):
        self.p_exp = p_exp
        self.T_f = temp_flow
        self.sigma_methane = sigma_methane
        self.sigma_water = sigma_water


class MassSpecAnalysis(ExperimentParameters):
    def import_raw_file(self, file):
        reader = open(self.file)
        row_offset = 2
        data = []
        with open(file, 'r') as txt_in:
            for i in np.xrange(row_offset):
                txt_in.next()
            for line in txt_in:
                data.append(line.split())
        data = np.array(data, dtype=np.float64)
        return data

    def smooth(self, y, box_pts):
        box = np.ones(box_pts) / box_pts
        y_smooth = np.convolve(y, box, mode='same')
        return y_smooth

    def exp_fit(self, x, a, b, c):
        return a * np.exp(-b * x) + c

    def gaussian(self, x, amp, cen, wid):  #
        return (amp) * np.exp(-(x - cen) ** 2 / (2 * wid ** 2))

    def clean_tof_spectra(self, data):
        col_names = ['time', 'signal)']
        ms_baseline_corr = pd.DataFrame(data=data, columns=col_names)
        ms_baseline_corr = ms_baseline_corr.loc[ms_baseline_corr['Time(s)'] > 0]
        ms_baseline_corr = ms_baseline_corr.assign(
            bl_corr_signal=lambda a: a.signal - a.signal.tail(1000).mean()).reset_index(drop=True, inplace=False)
        return ms_baseline_corr

    def pick_peaks_for_calibration(self):
        pass

    def calibrate_tof_spectra(self):
        pass

    def determine_peak_shape(self):
        pass

    def determine_number_concentration(self):
        pass
