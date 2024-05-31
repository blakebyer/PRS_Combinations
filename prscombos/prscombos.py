""" Import Libraries """
from config import tsv_path, tsv_cols, adni_path, adni_cols, dx_path, dx_cols, demographics, default
import pandas as pd
import numpy as np
from scipy.stats import gmean, hmean, ranksums, chisquare
import matplotlib.pyplot as plt

""" Initialize DataFrames and Variables """
tsv_df = pd.read_csv(tsv_path, header=0, usecols=tsv_cols, sep='\t')
adni_df = pd.read_csv(adni_path, header=0, usecols=adni_cols)
dx_df = pd.read_csv(dx_path, header=0, usecols=dx_cols)

def filter_df(df, traits):
    """
    Filters the DataFrame to only include rows where 'Reported Trait' contains the specified traits.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    traits (str): The trait(s) to filter by.
    
    Returns:
    pd.DataFrame: The filtered DataFrame.
    """
    df = df[df['Reported Trait'].str.contains(f'{traits}', case=False)].reset_index(drop=True)
    return df

def find_diagnosis(df, options):
    """
    Determines whether to keep the earliest or latest diagnosis.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    options (str): Either 'Earliest' or 'Latest' to specify which diagnosis to keep.
    
    Returns:
    pd.DataFrame: The DataFrame with diagnoses filtered by the specified option.
    """
    if options == 'Earliest':
        keep = 'first'
        fill = 'bfill'
    elif options == 'Latest':
        keep = 'last'
        fill = 'ffill'
    else: 
        raise ValueError("Enter 'Earliest' or 'Latest'")

    # Fill empty values and keep the specified diagnosis
    df['EXAMDATE'] = df['EXAMDATE'].fillna(method=fill)
    df['DIAGNOSIS'] = df['DIAGNOSIS'].fillna(method=fill)
    df = df.drop_duplicates(subset='RID', keep=keep).reset_index(drop=True)

    return df

def create_merged_df(df1, df2, df3, demographics):
    """
    Merges three DataFrames on relevant columns and creates a pivot table for percentiles.
    
    Args:
    df1 (pd.DataFrame): ADNI DataFrame.
    df2 (pd.DataFrame): Diagnoses DataFrame, generated from find_diagnosis function.
    df3 (pd.DataFrame): Filtered DataFrame.
    demographics (list): List of demographic columns from adni_df.
    
    Returns:
    pd.DataFrame: The merged and pivoted DataFrame.
    """
    # Drop duplicates in adni_df to eliminate duplicate patients
    df1 = df1.drop_duplicates(subset='RID', keep='first').reset_index(drop=True)
    
    # Merge DataFrames on 'RID'
    adni_diagnoses = pd.merge(df1, df2, left_on='RID', right_on='RID', how='inner').reset_index(drop=True)
    
    # Ensure case consistency for merging
    adni_diagnoses['PTID'] = adni_diagnoses['PTID'].str.upper()
    df3['Sample'] = df3['Sample'].str.upper()
    
    # Merge DataFrames on 'Sample'
    diagnoses_tsv = pd.merge(adni_diagnoses, df3, left_on='PTID', right_on='Sample', how='inner').reset_index(drop=True)
    
    # Create pivot table
    merged_df = diagnoses_tsv.pivot_table(index=demographics, columns='Study ID', values='Percentile', aggfunc='first')
    
    return merged_df

def range_to_numeric(df):
    """
    Converts UK Biobank percentile ranges, like 50-72, to numeric values (mean of the range).
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    pd.DataFrame: The DataFrame with numeric percentile values.
    """
    def convert_value(x):
        if pd.isna(x):
            return None
        elif '-' in x:
            lower, upper = map(float, x.split('-'))
            return (lower + upper) / 2
        else:
            return float(x)

    return df.applymap(convert_value)

def drop_gwas(df, methods, threshold=0, gwas=None, unique=0):
    """
    Drops GWAS columns based on the specified method.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    methods (str): The method to use for dropping columns.
    threshold (int, optional): Threshold for the number of NaNs in 'dropnaX' method.
    gwas (list, optional): List of GWAS IDs to drop for 'select' method.
    unique (int, optional): Cutoff for unique proportion in 'repeated' method.
    
    Returns:
    pd.DataFrame: The DataFrame with GWAS columns dropped based on the method.
    """
    if gwas is None:
        gwas = []  # Initialize gwas as an empty list

    if methods == 'dropna':
        df = df.dropna(axis='columns', how='any')
    elif methods == 'dropnaX':
        df = df.dropna(axis='columns', thresh=threshold)
    elif methods == 'repeated':
        unique_proportion = df.apply(lambda col: col.nunique() / col.count(), axis='rows')
        del_cols = unique_proportion[unique_proportion < (unique / len(df))].index
        df = df.drop(del_cols, axis='columns')
    elif methods == 'select':
        df = df.drop(gwas, axis='columns')
    else:
        raise ValueError("Enter specified method")

    return df

def simpledx(df):
    """
    Simplifies diagnosis categories.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    pd.DataFrame: The DataFrame with simplified diagnosis categories.
    """
    df.reset_index(inplace=True)
    df['DIAGNOSIS'] = df['DIAGNOSIS'].replace(["Dementia", "MCI"], "CI")
    df = df.reset_index(drop=True)
    return df

def means_calculations(df):
    """
    Calculates arithmetic, geometric, and harmonic means for each row.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    
    Returns:
    pd.DataFrame: The DataFrame with new columns for each mean type.
    """
    df.dropna(axis='columns', how='any', inplace=True)
    df.replace(0.0, 1, inplace=True)
    df['Arithmetic Mean'] = df.apply(np.mean, axis=1)
    df['Geometric Mean'] = df.apply(gmean, axis=1)
    df['Harmonic Mean'] = df.apply(hmean, axis=1)

    return df

def mannwhitneyu(df, gwas_cols=default):
    """
    Performs Mann-Whitney U test between 'CN' and 'CI' diagnosis groups for each column.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    gwas_cols (list, optional): List of columns to test.
    
    Returns:
    pd.DataFrame: DataFrame with results of the Mann-Whitney U tests.
    """
    results_df = pd.DataFrame(columns=['Columns', 'Statistic', 'P-value'])
  
    for column in gwas_cols:
        try:
            group1 = df[df['DIAGNOSIS'] == 'CN'][column].dropna()
            group2 = df[df['DIAGNOSIS'] == 'CI'][column].dropna()
            statistic, p_value = ranksums(group1, group2)
        except ValueError:
            statistic, p_value = np.nan, np.nan  # Use np.nan for missing values

        results_df = pd.concat([results_df, pd.DataFrame({'Columns': [column], 'Statistic': [statistic], 'P-value': [p_value]})], ignore_index=True)

    return results_df

demographics = ['PTID','AGE','PTGENDER','PTRACCAT','APOE4','DIAGNOSIS','EXAMDATE'] # Demographics used in some functions
default = [col for col in df if col not in demographics] # Default gwas, which is all of them

def chi_squared(df, quantile, gwas_cols=default):
    """
    Performs Chi-squared test for top percentile of PRS.
    
    Args:
    df (pd.DataFrame): The input DataFrame.
    quantile (float): The lower cutoff for risk.
    gwas_cols (list, optional): List of columns to test.
    
    Returns:
    pd.DataFrame: DataFrame with results of the Chi-squared tests.
    """
    results_df = pd.DataFrame(columns=['Columns', 'Statistic', 'P-value'])
    for column in gwas_cols:
        df_sorted = df.sort_values(by=column, ascending=False)
    
        cn_count = sum(df["DIAGNOSIS"] == 'CN')
        ci_count = sum(df["DIAGNOSIS"] == 'CI')

        threshold = int((1 - quantile) * len(df_sorted))
        observed_cn = sum(df_sorted["DIAGNOSIS"].iloc[:threshold] == 'CN')
        observed_ci = sum(df_sorted["DIAGNOSIS"].iloc[:threshold] == 'CI')
        observed = np.array([observed_cn, observed_ci])

        expected = np.array([(cn_count / len(df_sorted)), (ci_count / len(df_sorted))]) * np.sum(observed)
        chisq_result, p_value = chisquare(observed, expected)
        
        temp_df = pd.DataFrame({'Columns': [column], 'Statistic': [chisq_result], 'P-value': [p_value]})

        results_df = pd.concat([results_df, temp_df], ignore_index=True)

    return results_df

def make_plots(df, options):
    """
    Plots bar graph of -log10(p-value) for sorted p-values.
    
    Args:
    df (pd.DataFrame): DataFrame with test results.
    options (str): Title for the plot.
    
    Returns:
    None: Displays the plot.
    """
    df_sorted = df.sort_values('P-value', ascending=False)

    gwas_studies = df_sorted['Columns'].tolist()
    p_values = df_sorted['P-value'].tolist()

    neg_log_p_values = [-np.log10(p) if p > 0 else np.nan for p in p_values]  # Using nan for p-value of 0 (log(0) is undefined)

    plt.figure(figsize=(10, 5))
    colors = ['skyblue' for study in gwas_studies]
    bars = plt.bar(gwas_studies, neg_log_p_values, color=colors)

    significance_threshold = -np.log10(0.05)
    plt.axhline(y=significance_threshold, color='red', linestyle='--', label='Significance threshold (p=0.05)')

    for bar, p_value in zip(bars, p_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'p={p_value:.3g}', 
                 ha='center', va='bottom', fontsize=6, rotation='horizontal')

    plt.xlabel('GWAS Study', fontsize=12, fontweight='bold')
    plt.ylabel('-log10(p-value)', fontsize=12, fontweight='bold')
    plt.title(f'{options} Results', fontsize=14, fontweight='bold')
    plt.legend()

    plt.xticks(rotation=90, fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.show()

def save_output(df, option, path):
    # Options are 'CSV','TSV', or 'XLSX'
    if option == 'CSV':
        df.to_csv(path,index=True)
        print("CSV File Saved")
    elif option == 'TSV':
        df.to_csv(path,index=True,sep='\t')
        print("TSV File Saved")
    elif option == 'XLSX':
        df.to_excel(path,index=True)
        print("XLSX (Excel) File Saved")
    else: 
        print("Pick filetype option: 'CSV','TSV', or 'XLSX' ")

"""
Usage for the PRS Combinations Project

This section demonstrates how to apply the defined functions to process polygenic risk scores (PRS) data 
and perform statistical analysis on the resulting DataFrame.

Steps:
1. Filter the TSV DataFrame for Alzheimer's and Dementia traits.
2. Find and keep the latest diagnosis for each individual.
3. Merge the ADNI DataFrame, diagnoses DataFrame, and filtered TSV DataFrame.
4. Convert PRS percentile ranges to numeric values.
5. Clean the DataFrame by removing columns with NaN values and GWAS with unsufficient unique values.
6. Calculate arithmetic, geometric, and harmonic means for each individual.
7. Simplify the diagnosis labels for easier analysis.
8. Perform the Mann-Whitney U test to compare groups.
9. Perform the Chi-Squared test to assess the distribution of PRS.
10. Generate and display plots for the statistical tests.

Each step is performed by calling the appropriate function defined earlier in the script.
"""

# Step 1: Filter the TSV DataFrame for Alzheimer's and Dementia traits
filtered_df = filter_df(tsv_df, 'Alzheimer|Dementia')

# Step 2: Find and keep the latest diagnosis for each individual
diagnoses = find_diagnosis(dx_df, 'Latest')

# Step 3: Merge the ADNI DataFrame, diagnoses DataFrame, and filtered TSV DataFrame
merged = create_merged_df(adni_df, diagnoses, filtered_df, demographics=demographics)

# Step 4: Convert percentile ranges to numeric values
numeric_prs = range_to_numeric(merged)

# Step 5: Clean the DataFrame by removing columns with NaN values and GWAS with unsufficient unique values.
cleaned_df = drop_gwas(numeric_prs, 'dropna')
unique_gwas = drop_gwas(cleaned_df, 'repeated', unique=50)

# Step 6: Calculate arithmetic, geometric, and harmonic means for each individual
means_df = means_calculations(unique_gwas)

# Step 7: Simplify the diagnosis labels for easier analysis
final_df = simpledx(means_df)

# Step 8: Perform the Mann-Whitney U test to compare groups
mannwhitney = mannwhitneyu(final_df)

# Step 9: Perform the Chi-Squared test to assess the distribution of PRS
chisq = chi_squared(final_df, 0.8)

# Step 10: Generate and display plots for the statistical tests
chisq_plot = make_plots(chisq, "Chi-Squared Test")
print(chisq_plot)
mannwhitney_plot = make_plots(mannwhitney, "Mann-Whitney U Test")
print(mannwhitney_plot)

# Uncomment the following line to save the final DataFrame to a CSV file
# final_csv = save_output(final_df, 'CSV', path) # Example usage
