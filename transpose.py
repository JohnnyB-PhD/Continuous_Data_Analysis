#!/usr/bin/env python3

import numpy as np
import pyreadline 
import pandas as pd
import os

os.mkdir("C:\Users\jbroussard5\Desktop\combined_values")

for i in os.listdir():
    if os.path.isdir(i):
        continue
    with open(i) as f:
        first_col = f.pyreadline()
    first_col = first_col.strip().split("\t")
    del first_col[0]
    data = np.loadtxt(i, skiprows=1)
    data = data.transpose();
    df = pd.DataFrame(data=data[1:,0:], columns=data[0], index=first_col)
    df.insert(0, 0, df.index)
    df.index = np.repeat(i, df.shape[0])
    df.to_csv("C:\Users\jbroussard5\Desktop\combined_values\combined_transpose.txt", mode="a", sep="\t")
    output = open("C:\Users\jbroussard5\Desktop\combined_values\combined_transpose.txt", "a")
    output.write("\n")
    output.close()
