#!/usr/bin/env python3

import math
import os
import re
import sys
import numpy as np
import pandas as pd
from io import StringIO

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: info_revision.py position spikes')
    position = str(sys.argv[1])
    spikes = str(sys.argv[2])
    bin_time = np.loadtxt(position, delimiter='\t', skiprows=1)
    bin_prob = bin_time/np.sum(bin_time)
    spikect = np.loadtxt(spikes, delimiter='\t', skiprows=1)
    with open(spikes) as f:
        header = f.readline()
    header = header.strip().split("\t")
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
    channel_names = "\n".join(channel_names)
    channel_names = "channel name\n" + channel_names
    df = pd.read_csv(StringIO(channel_names))
    df['mean firing rate'] = mean_firing_rate
    df['peak firing rate'] = peak_firing_rate
    df['std dev of firing rate'] = standard_deviation
    df['spatial information'] = spacial_info
    base = os.path.splitext(position)[0]
    output = base + "_spike_analysis.txt"
    df.to_csv(output, index=False, sep="\t")
