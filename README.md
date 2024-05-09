# Polygenic Risk Scores Combinations

## Introduction
We started the Polygenic Risk Scores Combinations Project in August 2023. In this repository, you will find the code we used to clean our data and perform our analyses. The primary aim of this project is to show that combining polygenic risk scores across multiple genome-wide association studies (GWAS) is adequate at predicting risk for Alzheimer's disease.
We calculated polygenic risk scores for 808 individuals from the Alzheimer's Disease Neuroimaging Initiative (ADNI) using the Polygenic Risk Scores Knowledge Base (PRSKB) commmand-line interface (CLI). Then, using statistical techniques, we showed that PRS from different GWAS had variable accuracy at predicting disease risk, empashizing the need for standardized PRS calculation methods before PRS can be used in the clinic.

## Requirements
| Tool  | Version | Installation |
| --- | --- | --- | 
| Python  | 3.11+ | [Python](https://www.python.org/downloads/) |
| R | 4.3+ | [R](https://cran.rstudio.com/index.html) |

| Package | Version | Installation |
| --- | --- | --- |
| pandas | 2.0.2+ | `pip install pandas` |
| numpy | 1.26.2+ | `pip install numpy` |
| scipy | 1.11.4+ | `pip install scipy` |
| matplotlib | 3.7.1+ | `pip install matplotlib` |

## Usage
This software is an accompaniment to the Polygenic Risk Scores Knowledge Base, an online or CLI polygenic risk scores calculator, which contains GWAS summary statistics from the NHGRI-EBI GWAS Catalog. Visit the Polygenic Risk Scores Knowledge Base at: [PRSKB](https://prs.byu.edu/)

Or clone the GitHub PRSKB repository:

``` git clone https://github.com/kauwelab/PolyRiskScore.git ```

To use the PRS Combinations Software:

``` git clone https://github.com/jmillerlab/PRS_Combinations.git ```

### Jupyter Notebooks
There are three Jupyter notebooks tutorials for how to use the software.

### Input
Your input must contain two separate files:
1. Tab-separated values (.tsv) file which is an output of the PRSKB. See [an example](Examples/PRSKB/samplePRSKBoutput.tsv).
2. Adnimerge. Comma-separated values (.csv) file, which is a compilation of patient demographics and biomarkers information in ADNI. See [an example](Examples/ADNI/fakeADNI.csv).
3. Dxsum. Comma-separated values (.csv) file, which has the final diagnoses for patients in ADNI. 

#### Downloadable ADNI Files Needed
| Data  | Disk Space (Megabytes) | Download Time (seconds) |
| ------------- | ------------- | ------------- |
| adnimerge  | 8.17  | 3.0 |
| dxsum | 1.54 | 1.0 | 

[Access ADNI Data](https://adni.loni.usc.edu/data-samples/access-data/)

[Instructions for downloading ADNIMERGE Package in R](https://adni.bitbucket.io/)

### Output
The standard output is a single comma-separated values (.csv) file, but you may choose from the following outputs:
1. CSV
2. TSV
3. XLSX (Excel)

### Functions

The main prs_combinations.py file has the following functions to clean, sort, and analyze your data:
- Sort PRSKB Output by Reported Trait
- Sort by Diagnosis
- Sort by Demographics
- Merge DataFrames
- Drop inaccurate GWAS from DataFrame
- Calculate mean PRS
- Kolmogorov-Smirnov Test
- Mann-Whitney U Test
- Chi-Squared Test
- Plot the Results

### Data Processing
The data from the PRSKB goes through several processing steps until it is useful. These can be summarized with the following steps:
1. Sorting
    - By Trait
    - By PRS Score Type (Odds Ratio, Beta, Percentiles)
    - By Study ID
    - By Sample
    - By Demographics
        - Exam Date
        - Sex
        - Age
        - Ethnicity 
    - Etc.
2. Cleaning
    - Deleting GWAS that cannot compute PRS for all individuals
    - Deleting GWAS that are inaccurate and imprecise. Low variation PRS.
    - Standardize diagnoses.
4. Merging
   - Merging of PRSKB output and demographics information
5. Analysis
   - Calculate mean PRS
   - Kolmogorov-Smirnov Test
   - Mann-Whitney U Test
   - Chi-squared Test
   - Plotting

#### Examples

```
def filter_df(tsv_df,trait1,trait2):
    #Create Filtered Dataframe for Reported Trait
    tsv_df = tsv_df[tsv_df['Reported Trait'].str.contains(trait1|trait2, case=False, regex=True)].reset_index(drop=True)
    return tsv_df

filter_df(tsv_df, 'Alzheimer','Dementia')
```

## Acknowlegements
Thank you to authors Hady Sabra, Blake Byer, Leah Moylan, and Justin Miller.

## License
This work is freely available for academic and not-for-profit use. However, commercial use is regulated by © 2024 University of Kentucky. All rights reserved. For more information about commercial use of this product, please contact Justin Miller, Ph.D. (justin.miller@uky.edu)
