#!/usr/bin/env python

import os
import sys
import pandas as pd
import subprocess
import fire
import glob


def concat(sample_barcodes):
    df = pd.read_csv(sample_barcodes)
    print(df["sample_id"].map(lambda x: x.split("_")))
#     for name, group in df.groupby(by="sample_id"):
#         if len(group) > 1:
#             print(group)



    # df = pd.read_csv(plate_indexes_file)
    # for name, group in df.groupby(by=plate_id):
    #     for read in [1,2]:
    #         files = ["{}.{}.fq.gz".format(i, read) for i in group["barcode_id"]]
    #         paths = " ".join([os.path.join(input_dir, i) for i in files])
    #         outpath = os.path.join(output_dir, "{}.{}.fq.gz".format(name, read))
    #         cmd = "cat {} > {}".format(paths, outpath)
    #         subprocess.call(cmd, shell=True)

if __name__ == "__main__":
    fire.Fire(concat)