# Polygenic Risk Scores Combinations

## Introduction
We started the Polygenic Risk Scores Combinations Project in August 2023. In this repository, you will find the code we used to clean our data and perform our analyses. The primary aim of this project is to show that combining polygenic risk scores across multiple genome-wide association studies (GWAS) is adequate at predicting risk for Alzheimer's disease.
We calculated polygenic risk scores for 808 individuals from the Alzheimer's Disease Neuroimaging Initiative (ADNI) using the Polygenic Risk Scores Knowledge Base (PRSKB) commmand-line interface (CLI). Then, using statistical techniques, we showed that PRS from different GWAS had variable accuracy at predicting disease risk, empashizing the need for standardized PRS calculation methods before PRS can be used in the clinic.

## Requirements
You will need the most recent version of Python: [Download Python](https://www.python.org/downloads/)

You must have the following packages:
- pandas
- numpy
- scipy

These packages can be installed with the following commands:
```
python -m pip install pandas
python -m pip install numpy
python -m pip install scipy
```
## Usage
The Polygenic Risk Scores Knowledge Base is an online or CLI polygenic risk scores calculator, which contains GWAS summary statistics from the NHGRI-EBI GWAS Catalog.
Visit the Polygenic Risk Scores Knowledge Base at: [PRSKB](https://prs.byu.edu/)

Or clone the GitHub PRSKB repository:

``` git clone https://github.com/kauwelab/PolyRiskScore.git ```

To use the PRS Combinations Software:

``` git clone https://github.com/jmillerlab/PRS_Combinations.git ```

### Input
Your input must contain two separate files:
1. Tab-separated values (.tsv) file which is an output of the PRSKB. See [an example](Examples/PRSKB).
2. Comma-separated values (.csv) file which contains demographics information from patient data. See [an example](Examples/).

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
