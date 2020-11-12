#!/usr/bin/env python

import os
import fire
import io
import pandas as pd
import numpy as np

barcode_map = """
read,enzyme,position,barcode_id,barcode_seq
read1,xbaI,A,NheI_A,CCGAATG
read1,xbaI,B,NheI_B,TTAGGCAG
read1,xbaI,C,NheI_C,AACTCGTCG
read1,xbaI,D,NheI_D,GGTCTACGTG
read1,xbaI,E,NheI_E,GATACCG
read1,xbaI,F,NheI_F,AGCGTTGG
read1,xbaI,G,NheI_G,CTGCAACTG
read1,xbaI,H,NheI_H,TCATGGTCAG
read1,nheI,A,NheI_A,CCGAATG
read1,nheI,B,NheI_B,TTAGGCAG
read1,nheI,C,NheI_C,AACTCGTCG
read1,nheI,D,NheI_D,GGTCTACGTG
read1,nheI,E,NheI_E,GATACCG
read1,nheI,F,NheI_F,AGCGTTGG
read1,nheI,G,NheI_G,CTGCAACTG
read1,nheI,H,NheI_H,TCATGGTCAG
read1,claI,A,ClaI_A,CCGAATAT
read1,claI,B,ClaI_B,TTAGGCAAT
read1,claI,C,ClaI_C,AACTCGTCAT
read1,claI,D,ClaI_D,GGTCTACGTAT
read1,claI,E,ClaI_E,GATACCAT
read1,claI,F,ClaI_F,AGCGTTGAT
read1,claI,G,ClaI_G,CTGCAACTAT
read1,claI,H,ClaI_H,TCATGGTCAAT
read2,ecoRI,1,EcoRI_1,CTAACGT
read2,ecoRI,2,EcoRI_2,TCGGTACT
read2,ecoRI,3,EcoRI_3,GATCGTTGT
read2,ecoRI,4,EcoRI_4,AGCTACACTT
read2,ecoRI,5,EcoRI_5,ACGCATT
read2,ecoRI,6,EcoRI_6,GTATGCAT
read2,ecoRI,7,EcoRI_7,CACATGTCT
read2,ecoRI,8,EcoRI_8,TGTGCACGAT
read2,ecoRI,9,EcoRI_9,GCATCAT
read2,ecoRI,10,EcoRI_10,ATGCTGTT
read2,ecoRI,11,EcoRI_11,CATGACCTT
read2,ecoRI,12,EcoRI_12,TGCAGTGAGT
read2,bamHI,1,BamHI_1,CTAACGC
read2,bamHI,2,BamHI_2,TCGGTACC
read2,bamHI,3,BamHI_3,GATCGTTGC
read2,bamHI,4,BamHI_4,AGCTACACTC
read2,bamHI,5,BamHI_5,ACGCATC
read2,bamHI,6,BamHI_6,GTATGCAC
read2,bamHI,7,BamHI_7,CACATGTCC
read2,bamHI,8,BamHI_8,TGTGCACGAC
read2,bamHI,9,BamHI_9,GCATCAC
read2,bamHI,10,BamHI_10,ATGCTGTC
read2,bamHI,11,BamHI_11,CATGACCTC
read2,bamHI,12,BamHI_12,TGCAGTGAGC
read2,hindIII,1,HindIII_1,CTAACGT
read2,hindIII,2,HindIII_2,TCGGTACT
read2,hindIII,3,HindIII_3,GATCGTTGT
read2,hindIII,4,HindIII_4,AGCTACACTT
read2,hindIII,5,HindIII_5,ACGCATT
read2,hindIII,6,HindIII_6,GTATGCAT
read2,hindIII,7,HindIII_7,CACATGTCT
read2,hindIII,8,HindIII_8,TGTGCACGAT
read2,hindIII,9,HindIII_9,GCATCAT
read2,hindIII,10,HindIII_10,ATGCTGTT
read2,hindIII,11,HindIII_11,CATGACCTT
read2,hindIII,12,HindIII_12,TGCAGTGAGT
"""

def gen(plate_barcodes, sample_map, out_dir="config/"):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    # Generate i7 barcodes file
    plate_df = pd.read_csv(plate_barcodes)
    plate_df[["barcode_seq", "barcode_id"]].to_csv(os.path.join(out_dir,
            "barcodes-i7.tsv"), sep="\t", index=False, header=False)

    # Read sample barcode map csv
    sample_df = pd.read_csv(sample_map, dtype=str)

    # Check if sample ids contain '.', period will be used to merge duplicated
    # samples later so cannot be used in sample id
    contain_stop = sample_df[sample_df["sample_id"].str.contains('\.')]["sample_id"]
    if len(contain_stop) > 0:
        rec_str = "\n  ".join(contain_stop)
        quit("\nError: The following sample ids contain a \'.\' which will interfere with later steps\n  {}".format(rec_str))

    # Read barcode map csv string
    barcode_map_df = pd.read_csv(io.StringIO(barcode_map), dtype=str)

    # Separate read 1 barcodes into dataframe
    r1_df = barcode_map_df[barcode_map_df["read"] == "read1"].drop(
            "read", axis=1).rename(columns=dict(enzyme="read1_enzyme",
            position="row", barcode_id="read1_barcode_id",
            barcode_seq="read1_barcode_seq"))

    # Separate read 2 barcodes into dataframe
    r2_df = barcode_map_df[barcode_map_df["read"] == "read2"].drop(
            "read", axis=1).rename(columns=dict(enzyme="read2_enzyme",
            position="column", barcode_id="read2_barcode_id",
            barcode_seq="read2_barcode_seq"))


    for proj, proj_data in sample_df.groupby("proj_id"):
        # Make popmap file for each project before renaming duplicates so they
        # can be merged later
        # Replace pop_id with sample_id if pop_id is None
        unique_proj_data = proj_data.drop_duplicates("sample_id")
        proj_data["pop_id"] = np.where(proj_data["pop_id"] == "None",
                proj_data["sample_id"], proj_data["pop_id"])
        # Output popmap file
        path = os.path.join(out_dir, "popmap-{}.tsv".format(proj))
        cols = ["sample_id", "pop_id"]
        proj_data.to_csv(path, columns=cols, sep="\t", index=False, header=None)

        # Check for duplicate sample ids and rename them so they can later be merged
        dups = proj_data[proj_data[["proj_id", "sample_id"]].duplicated(keep=False)]
        for name, group in dups.groupby(by="sample_id"):
            cnt = 1
            for ix, row in group.iterrows():
                proj_data.iloc[ix]["sample_id"] = "{}.{}".format(name, cnt)
                cnt += 1

        # Merge read 1 and read2 barcode data with sample map dataframe
        proj_data = proj_data.merge(r1_df, how="left", on=["row", "read1_enzyme"]
                ).merge(r2_df, how="left", on=["column", "read2_enzyme"])

        # Output tab separated barcode file for each plate
        cols = ["read1_barcode_seq", "read2_barcode_seq", "sample_id"]
        plate_ids = plate_df["plate_id"].unique()
        for plate, plate_data in proj_data.groupby("plate_id"):
            group_df = plate_data[cols]
            path = os.path.join(out_dir, "barcodes-samples-{}.tsv".format(plate))
            group_df.to_csv(path, sep="\t", index=False, header=None)

if __name__ == "__main__":
    fire.Fire(gen)
