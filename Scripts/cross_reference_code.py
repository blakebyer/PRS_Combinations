import pandas as pd

# Load the Excel spreadsheet with the correct column names
spreadsheet_file_path = "C:\\Users\\hadys\\Desktop\\PRS Combinations\\ADNIMERGE_21Nov2023.xlsx"
df_spreadsheet = pd.read_excel(spreadsheet_file_path, usecols=['PTID', 'DX_bl'])

# Load the TSV file
tsv_file_path = "C:\\Users\\hadys\\Desktop\\PRS Combinations\\hady_ADNI_trial2.tsv"
df_tsv = pd.read_csv(tsv_file_path, sep='\t', header=None, skiprows=1)

# Transpose the TSV DataFrame to have IDs as rows
df_tsv = df_tsv.T

# Extract the IDs from the first row of the TSV DataFrame
tsv_ids = df_tsv.iloc[0]

# Create a new DataFrame to store the results
df_results = pd.DataFrame(columns=['ID', 'Count'])

# Iterate through the IDs in the spreadsheet and count occurrences in the TSV file
for index, row in df_spreadsheet.iterrows():
    id_in_spreadsheet = row['PTID']
    count_in_tsv = tsv_ids[tsv_ids == id_in_spreadsheet].count()
    df_results = pd.concat([df_results, pd.DataFrame({'ID': [id_in_spreadsheet], 'Count': [count_in_tsv + 1]})])

# Group by ID and aggregate the count
df_results = df_results.groupby('ID')['Count'].sum().reset_index()

# Display the detailed count results
print(df_results)

# Save detailed count results to an Excel file
excel_detailed_output_path = "C:\\Users\\hadys\\Desktop\\PRS Combinations\\detailed_results.xlsx"
df_results.to_excel(excel_detailed_output_path, index=False)
