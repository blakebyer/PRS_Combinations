import pandas as pd
import numpy as np
from scipy import stats as spy

#Load Files
adni_path = r"" #ADNIMERGE is a CSV with Demographic Information About Cases
tsv_path = r"" #TSV is the raw output file from the PRSKB CLI Tool

#Create Dataframes
demographics = ['PTID','DX','DX_bl','PTGENDER','PTRACCAT','AGE','APOE4','EXAMDATE']
tsv_df = pd.read_csv(tsv_path, header=0, usecols=['Sample','Study ID','Reported Trait','Percentile'],sep='\t')
adni_df = pd.read_csv(adni_path, header=0,usecols=demographics)
merged_df = pd.DataFrame()
final_df = pd.DataFrame()
