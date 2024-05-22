import pandas as pd

# Read the CSV file
input_file = 'D:/ATOMPROJECTS/tatras/NarrativeReseach/TWEETS/New_RajeshAgrawal.csv'  # Replace with your actual file path
df = pd.read_csv(input_file)

# Select the first 134 rows
df_subset = df.head(134)

# Write the selected rows to a new CSV file
output_file = 'D:/ATOMPROJECTS/tatras/NarrativeReseach/TWEETS/final_rajesh.csv'  # Replace with your desired output file path
df_subset.to_csv(output_file, index=False)

print(f"Saved the first 134 rows to {output_file}")


