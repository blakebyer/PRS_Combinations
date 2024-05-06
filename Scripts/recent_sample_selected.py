import pandas as pd
from datetime import datetime

# Load the Excel spreadsheet with the correct column names
spreadsheet_file_path = "C:\\Users\\hadys\\Desktop\\PRS Combinations\\ADNIMERGE_21Nov2023.xlsx"
df = pd.read_excel(spreadsheet_file_path)

# Convert the 'EXAMDATE' column to datetime format
df['EXAMDATE'] = pd.to_datetime(df['EXAMDATE'], errors='coerce')

# Group by 'PTID' and find the index of the row with the most recent 'EXAMDATE'
recent_sample_indices = df.groupby('PTID')['EXAMDATE'].idxmax()

# Select rows with the most recent 'EXAMDATE'
selected_samples = df.loc[recent_sample_indices]

# Save the selected samples to a separate Excel file
output_file_path = "selected_samples.xlsx"
selected_samples.to_excel(output_file_path, index=False)

print("Selected samples saved to:", output_file_path)
