#!/usr/bin/env python3

import re
import sys
import numpy as np

filepath = str(sys.argv[1])
output = str(sys.argv[2])
with open(filepath) as f:
    header = f.readline()
header = header.strip().split("\t")
x = np.genfromtxt(filepath, delimiter="\t", skip_header=1)
digits = []
for i in range(0, len(header)):
    digits.append(int(re.findall('\d+', header[i])[0]))
digits = np.unique(digits)
count = []
for i in range(0, x.shape[1], 2):
    count.append(x[:,i][~np.isnan(x[:,i])].size)
outmat = np.zeros((len(count), 2))
for i in range(0, outmat.shape[0]):
    outmat[i][0] = digits[i]
    outmat[i][1] = count[i]
out = open(output, 'w')
out.write("Channel\t#Ripples\n")
out.close()
out = open(output, 'ab')
np.savetxt(out, outmat, delimiter="\t")
out.close()
