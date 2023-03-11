#!/usr/bin/env python3

import math
import os
import re
import sys
import numpy as np
import pandas as pd
from io import StringIO

def reg_trim(header):
    for i in range(0, len(header)):
        header[i] = re.sub(" bin.*", "", header[i])
    return header

def firing_rate(position, spikes):
    bin_time = np.loadtxt(position, delimiter='\t', skiprows=1)
    bin_prob = bin_time/np.sum(bin_time)
    spikect = np.loadtxt(spikes, delimiter='\t', skiprows=1)
    channel_num = int(spikect.shape[1]/spikect.shape[0])
    mean_firing_rate = np.zeros(channel_num)
    standard_deviation = np.zeros(channel_num)
    peak_firing_rate = np.zeros(channel_num)
    spacial_info = np.zeros(channel_num)
    channel_names = []
    for i in range(0, channel_num):
        start = i * 20;
        spikesub = spikect[:,start:start+20]
        firing_rate = np.nan_to_num(spikesub/bin_time)
        channel_names.append(re.sub("bin[0-9]", "", header[start]))
        mean_firing_rate[i] = np.nan_to_num(np.sum(spikesub)/np.sum(bin_time))
        standard_deviation[i] = np.std(firing_rate.flatten())
        peak_firing_rate[i] = np.max(firing_rate.flatten())
        for j in range(0, spikesub.shape[0]):
            for k in range(0, spikesub.shape[1]):
                if (firing_rate[:,j][k] == 0):
                    continue
                else:
                    spacial_info[i] += bin_prob[:,j][k]*(firing_rate[:,j][k]/mean_firing_rate[i])*math.log((firing_rate[:,j][k]/mean_firing_rate[i]), 2)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        sys.exit('Usage: correlation.py basename')
    basename = str(sys.argv[1])
    familiar = basename+"_F"
    nlocation = basename+"_NL"
    position1 = "TrackingInfo/"+familiar+"_timespent.txt"
    position2 = "TrackingInfo/"+nlocation+"_timespent.txt"
    spikes1 = "TrackingInfo/"+familiar+"_spikecount.txt"
    spikes2 = "TrackingInfo/"+nlocation+"_spikecount.txt"
    with open(spikes1) as f:
        header1 = f.readline()
    header1 = header1.strip().split("\t")
    header1 = reg_trim(header1)
    with open(spikes2) as g:
        header2 = g.readline()
    header2 = header2.strip().split("\t")
    header2 = reg_trim(header2)
    bin_time1 = np.loadtxt(position1, delimiter='\t', skiprows=1)
    bin_prob1 = bin_time1/np.sum(bin_time1)
    spikect1 = np.loadtxt(spikes1, delimiter='\t', skiprows=1)
    bin_time2 = np.loadtxt(position2, delimiter='\t', skiprows=1)
    bin_prob2 = bin_time2/np.sum(bin_time2)
    spikect2 = np.loadtxt(spikes2, delimiter='\t', skiprows=1)
    channel_num1 = int(spikect1.shape[1]/spikect1.shape[0])
    channel_num2 = int(spikect2.shape[1]/spikect2.shape[0])
    channel_names1 = []
    channel_names2 = []
    f_rate = []
    nl_rate = []
    for i in range(0, channel_num1):
        start = i * 20;
        spikesub = spikect1[:,start:start+20]
        f_rate.append(np.nan_to_num(spikesub/bin_time1))
        channel_names1.append(re.sub("bin[0-9]", "", header1[i]))
    for i in range(0, channel_num2):
        start = i * 20;
        spikesub = spikect2[:,start:start+20]
        nl_rate.append(np.nan_to_num(spikesub/bin_time2))
        channel_names2.append(re.sub("bin[0-9]", "", header2[i]))
    corr = []
    for i in range(0, len(channel_names1)):
        for j in range(0, len(channel_names2)):
            if channel_names1[i] == channel_names2[j]:
                corr.append(np.corrcoef(f_rate[i].flatten(), nl_rate[j].flatten())[0][1])
                break
    z = np.zeros((len(f_rate), len(f_pos)*2))
    for i in range(0, len(f_rate)):
        for j in range(0, len(f_pos)):
            z[i][2*j] = f_rate[i][f_pos[j]]
            z[i][2*j+1] = nl_rate[i][nl_pos[j]]
    output = basename+"_correlations.txt"
    out = open(output, "w")
    out.write(channel_names)
    out.write("\n")
    np.savetxt(out, z, delimiter="\t")
    out.close()
