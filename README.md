# Polygenic Risk Scores Combinations

## Introduction
We started the Polygenic Risk Scores Combinations Project in August 2023. In this repository, you will find the code we used to clean our data and perform our analyses. The primary aim of this project is to show that combining polygenic risk scores across multiple genome-wide association studies (GWAS) is adequate at predicting risk for Alzheimer's disease.
We calculated polygenic risk scores for 808 individuals from the Alzheimer's Disease Neuroimaging Initiative (ADNI) using the Polygenic Risk Scores Knowledge Base (PRSKB) commmand-line interface (CLI). Then, using statistical techniques, we showed that PRS from different GWAS had variable accuracy at predicting disease risk, empashizing the need for standardized PRS calculation methods before PRS can be used in the clinic.

## Requirements
| Tool  | Version | Installation |
| --- | --- | --- | 
| Python  | 3.11+ | [Python](https://www.python.org/downloads/) |
| R | 4.3+ | [R](https://cran.rstudio.com/index.html) |
| Jupyter | 1.0.0 | `pip install jupyter` |

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
There is a Jupyter notebook tutorial for how to use the software.

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

### Data Processing
Each step is its own callable function within the Jupyter Notebook.
1. Setup config.py file
2. Import Packages
3. Initialize DataFrames
4. Create Filtered DataFrame for Reported Trait
5. Find Earliest or Latest Diagnosis for Patient in ADNI
6. Merge Three DataFrames to Clean the Data
7. Convert Range PRS to Mean of Lower and Upper Bounds
8. Drop Genome-Wide Association Studies
9. Calculate Means
10. Simple Diagnosis for Cases and Controls
11. Mann-Whitney U Test
12. Chi-Squared Test
13. Make Plots
14. Save Output

## Acknowlegements
Thank you to authors Hady Sabra, Blake Byer, Leah Moylan, and Justin Miller.

## License
This work is freely available for academic and not-for-profit use. However, commercial use is regulated by © 2024 University of Kentucky. All rights reserved. For more information about commercial use of this product, please contact Justin Miller, Ph.D. (justin.miller@uky.edu)
