#!/usr/bin/env python3

import re
import peaks as r
import sys
import numpy as np
from scipy.signal import butter, sosfilt, sosfreqz

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = butter(order, [low, high], analog=False, btype='band', output='sos')
    return sos

def butter_bandpass_filter(data, lowcut, highcut, fs, order):
    sos = butter_bandpass(lowcut, highcut, fs, order=order)
    y = sosfilt(sos, data)
    return y

def extrema(x, i):
    diff = np.diff(x)
    if (diff[i] > 0 and diff [i - 1] < 0):
        return True
    elif (diff[i] < 0 and diff [i - 1] > 0):
        return True
    else:
        return False

def col_extract(header):
    cols_index = []
    for i in range(0, len(header)):
        cols_index.append(int(re.findall("\d+", header[i])[0]))
    return cols_index

def reg_search(header):
    cols = []
    for i in range(0, len(header)):
        if re.search("[0-9]_values", header[i]):
        #if re.search("value_[0-9]", header[i]):
            cols.append(i)
    return cols

def ripple_event(t, fs, peaks_pos):
    ripple = []
    for i in range(0, len(peaks_pos)):
        dur = 0.4*fs
        y_index = peaks_pos[i][0]
        peak_dur = peaks_pos[i][2] - peaks_pos[i][1]
        half = int((dur - peak_dur)/2)
        begin = peaks_pos[i][1] - half
        end = peaks_pos[i][2] + half
        if begin < 0:
            begin = 0
            end = int(dur)
        if end > t.size - 1:
            end = t.size - 1
        ripple.append((y_index, begin, end))
    return ripple

def ripple_spikes(y, sd):
    peaks = []
    for i in range(0, y.shape[1]):
        peaks.append(y[:,i][(abs(y[:,i]) > 6*sd[i]).nonzero()])
    return peaks

def ripple_peaks(spike_pos, channels):
    peaks_pos = []
    dur = 0.4*fs
    for i in range(0, len(spike_pos)):
        for j in range(0, len(spike_pos[i])):
            pos = spike_pos[i][j]
            if j == 0:
                init_pos = spike_pos[i][j]
                continue
            if j == len(spike_pos[i]) - 1:
                peaks_pos.append((channels[i], init_pos, pos))
                break
            if pos - init_pos < dur:
                continue
            else:
                prev_pos = spike_pos[i][j - 1]
                peaks_pos.append((channels[i], init_pos, prev_pos))
                init_pos = pos
                continue
    return peaks_pos

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: ripple.py input output')
    filepath = str(sys.argv[1])
    output = str(sys.argv[2])
    with open(filepath) as f:
        header = f.readline()
    header = header.strip().split("\t")
    cols = reg_search(header)
    col_channels = col_extract([ header [i] for i in cols ])
    x = np.loadtxt(filepath, delimiter='\t', skiprows=1, usecols=cols)
    fs = 2000
    lowcut = 100
    highcut = 250
    interval = 1/fs
    end = 1/fs * x.shape[0]
    t = np.arange(0, end, 1/fs)
    y = np.empty((x.shape[0], x.shape[1]))
    for i in range(0, (x.shape[1])):
        y[:,i] = butter_bandpass_filter(x[:,i], lowcut, highcut, fs, order=4)
    sd = np.empty(x.shape[1])
    for i in range(0, (x.shape[1])):
        sd[i] = np.std(y[:,i])
    spikes = ripple_spikes(y, sd)
    spike_pos = []
    for i in range(0, len(spikes)):
        spike_pos.append(r.peaks(y[:,i].tolist(), spikes[i].tolist()))
    peaks = ripple_peaks(spike_pos, col_channels)
    ripple_loc = ripple_event(t, fs, peaks)
    rip = []
    for i in range(0, len(ripple_loc)):
        index = np.where(ripple_loc[i][0] == np.array(col_channels))[0][0]
        ripple = np.zeros((ripple_loc[i][2] - ripple_loc[i][1], 2))
        ripple[:,0] = t[ripple_loc[i][1]:ripple_loc[i][2]]
        ripple[:,1] = y[:,index][ripple_loc[i][1]:ripple_loc[i][2]]
        rip.append(ripple)
    maxes = []
    for i in range(0, len(rip)):
        amp = max(rip[i][:,1].max(), rip[i][:,1].min(), key=abs)
        maxes.append(amp)
    max_col = 0
    col_length = 0
    for i in range(0, len(ripple_loc)):
        if i == 0:
            prev = ripple_loc[i][0]
            continue
        if prev == ripple_loc[i][0]:
            col_length = col_length + 1
            continue
        else:
            if col_length > max_col:
                max_col = col_length
                col_length = 0
            prev = ripple_loc[i][0]
    z = np.zeros((max_col, max(col_channels)*2))
    for i in range(0, len(ripple_loc)):
        if i == 0:
            col = ripple_loc[i][0] - 1
            row = 0
            z[row][2*col] = t[ripple_loc[i][1]]
            z[row][2*col+1] = t[ripple_loc[i][2]]
        if col == ripple_loc[i][0] - 1:
            z[row][2*col] = t[ripple_loc[i][1]]
            z[row][2*col+1] = t[ripple_loc[i][2]]
            row = row + 1
        else:
            col = ripple_loc[i][0] - 1
            row = 0
            z[row][2*col] = t[ripple_loc[i][1]]
            z[row][2*col+1] = t[ripple_loc[i][2]]
    channel_names = []
    for i in range(0, max(col_channels)):
        channel_names.append("Chan"+str(i+1)+"Start")
        channel_names.append("Chan"+str(i+1)+"End")
    channel_names = "\t".join(channel_names)
    out = open(output, 'w')
    out.write(channel_names)
    out.write("\n")
    for i in range(0, z.shape[0]):
        for j in range(0, z.shape[1]):
            if z[i][j] == 0:
                if j == z.shape[1] - 1:
                    out.write("\n")
                else:
                    out.write("\t")
            else:
                out.write(str(z[i][j]))
                if j != z.shape[1] - 1:
                    out.write("\t")
            if j == z.shape[1] - 1:
                out.write("\n")
    out.close()
