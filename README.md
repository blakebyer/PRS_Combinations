# Polygenic Risk Scores Combinations

## Introduction
We started the Polygenic Risk Scores Combinations Project in August 2023. In this repository, you will find the code we used to clean our data and perform our analyses. The primary aim of this project is to show that combining polygenic risk scores across multiple genome-wide association studies (GWAS) is adequate at predicting risk for Alzheimer's disease.
We calculated polygenic risk scores for 808 individuals from the Alzheimer's Disease Neuroimaging Initiative (ADNI) using the Polygenic Risk Scores Knowledge Base commmand-line interface (CLI). Then, using statistical techniques, we showed that PRS from different GWAS had variable accuracy at predicting disease risk, empashizing the need for standardized PRS calculation methods before PRS can be used in the clinic.

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
The Polygenic Risk Scores Knowledge Base is an online or CLI polygenic risk scores calculator, which contains GWAs summary statistics from the NHGRI-EBI GWAs Catalog.
Visit the Polygenic Risk Scores Knowledge Base at: [PRSKB](https://prs.byu.edu/) or [PRSKB Github](https://github.com/kauwelab/PolyRiskScore.git)

``` git clone https://github.com/kauwelab/PolyRiskScore.git ```

To use the PRS Combinations Software:
``` git clone https://github.com/jmillerlab/PRS_Combinations.git ```

### Functions
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

### Examples

## Tests


## 



