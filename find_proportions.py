import pandas as pd

# Step 1: Load filtered clean data
input_file = 'HPU Subset Data Filtered.csv'
df = pd.read_csv(input_file)

# Step 2: Group by Gear Type and Color
grouped = df.groupby(['Gear Type', 'Color'])

# Step 3: Calculate proportions and collect into list
rows = []

for (gear, color), group in grouped:
    language_counts = group['Language'].value_counts()
    total = language_counts.sum()
    proportions = (language_counts / total).to_dict()
    for language, prop in proportions.items():
        rows.append({
            "Gear Type": gear,
            "Color": color,
            "Language": language,
            "Proportion": round(prop, 4)
        })

# Step 4: Create a DataFrame
proportions_df = pd.DataFrame(rows)

# Step 5: Save to CSV
output_file = 'language_proportions.csv'
proportions_df.to_csv(output_file, index=False)
print(f"Saved language proportions to '{output_file}'.")
