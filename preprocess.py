import pandas as pd

# Path to your input and output files
filepath = 'C:/IMSE7143-IoT2024-CW1/TestingResults.txt'
output_path = 'C:/Users/85817/PycharmProjects/WEI/abnormal_guide_price.xlsx'

# Read the data and filter rows where the last element is '1'
data_lines = []
with open(filepath, 'r') as file:
    for line in file:
        line_data = line.strip().split(',')
        if line_data and line_data[-1] == '1':  # Check if the last element is '1', abnormal
            data_lines.append(line_data[:24])  # Take only the first 24 elements

# Convert to DataFrame
data_df = pd.DataFrame(data_lines)

# Save to Excel file
data_df.to_excel(output_path, index=False, header=False)
