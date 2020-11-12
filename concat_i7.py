#!/usr/bin/env python

import os
import sys
import pandas as pd
import subprocess
import fire

def concat(input_dir="output/clone-filter/", output_dir="output/concat-i7/",
        plate_indexes_file="config/barcodes-i7.csv"):
    df = pd.read_csv(plate_indexes_file)
    os.mkdir(output_dir)
    for name, group in df.groupby(by="plate_id"):
        for read in [1,2]:
            files = ["{i}.{read}.{read}.fq.gz".format(
                    i=i, read=read) for i in group["barcode_id"]]
            paths = " ".join([os.path.join(input_dir, i) for i in files])
            outpath = os.path.join(output_dir, "{name}.{read}.fq.gz".format(
                    name=name, read=read))
            cmd = "cat {} > {}".format(paths, outpath)
            subprocess.call(cmd, shell=True)
    print("Finished concatenating")

if __name__ == "__main__":
    fire.Fire(concat)
