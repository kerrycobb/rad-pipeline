#!/usr/bin/env python

import fire
import glob
import os
import subprocess

def qsub(cmd, name, log_dir):
    subprocess.call(
        "myqsub -N {} -t 48:00:00 -m 10gb -o {} \"{}\"".format(name, log_dir, cmd),
        shell=True)

def declone(input_dir="output/process-radtags-i7", output_dir="output/clone-filter/"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    else:
        quit("{} directory already exists".format(output_dir))
    log_dir = os.path.join(output_dir, "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    files = glob.glob("{}/*.fq.gz".format(input_dir))
    # basenames = set([os.path.basename(i).split('.')[0] for i in files])
    path_basename = set([file.split('.')[0] for file in files])
    for sample in path_basename:
        sample_name = sample.split("/")[-1]
        cmd = (
            "module load stacks; "
            "clone_filter "
                "-1 {sample}.1.fq.gz "
                "-2 {sample}.2.fq.gz "
                "-o {output_dir} "
                "-i gzfastq "
                "--null_index "
                "--oligo_len_2 8").format(sample=sample, output_dir=output_dir)
        qsub(cmd, sample_name, log_dir)

if __name__ == "__main__":
    fire.Fire(declone)
