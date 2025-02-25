import pandas as pd
import numpy as np
import shutil
import matplotlib.pyplot as plt

# First, make a copy of the filtered data
shutil.copy2('HPU Master Data Filtered.csv', 'Simulation Outcomes.csv')

# Load the data
proportions_df = pd.read_csv('Language Proportions.csv')
simulation_df = pd.read_csv('Simulation Outcomes.csv')

# Create a dictionary to store probabilities for each gear type + color combination
prob_dict = {}
for _, row in proportions_df.iterrows():
    key = (row['Gear Type'], row['Color'])
    if key not in prob_dict:
        prob_dict[key] = []
    prob_dict[key].append({'language': row['Language'], 'probability': row['Proportion']})


# Function to assign language based on probabilities
def assign_language(gear_type, color):
    key = (gear_type, color)
    if key in prob_dict:
        options = prob_dict[key]
        languages = [opt['language'] for opt in options]
        probabilities = [opt['probability'] for opt in options]
        chosen_language = np.random.choice(languages, p=probabilities)
        # Find the probability for the chosen language
        chosen_prob = next(opt['probability'] for opt in options if opt['language'] == chosen_language)
        return chosen_language, round(chosen_prob, 4)
    return None, None


# Add new columns
simulation_df['Assigned?'] = False
simulation_df['Probability'] = 'N/A'

# Assign languages where they're missing
assignments = []
for index, row in simulation_df.iterrows():
    if pd.isna(row['Language']):
        assigned_language, probability = assign_language(row['Gear Type'], row['Color'])
        if assigned_language:
            simulation_df.at[index, 'Language'] = assigned_language
            simulation_df.at[index, 'Assigned?'] = True
            simulation_df.at[index, 'Probability'] = probability
            assignments.append({
                'ID Name': row['ID Name'],
                'Gear Type': row['Gear Type'],
                'Color': row['Color'],
                'Assigned Language': assigned_language,
                'Probability': probability
            })

# Save the results
simulation_df.to_csv('Simulation Outcomes.csv', index=False)

# Print statistics and sample assignments
print("\nSimulation complete!")
print(f"Total rows processed: {len(simulation_df)}")
print(f"Number of new language assignments: {len(assignments)}")

print("\nSample of new language assignments:")
for assignment in assignments[:5]:  # Show first 5 assignments
    print(f"\nID Name: {assignment['ID Name']}")
    print(f"Gear Type: {assignment['Gear Type']}")
    print(f"Color: {assignment['Color']}")
    print(f"Assigned Language: {assignment['Assigned Language']}")
    print(f"Probability: {assignment['Probability']}")

# After line 77 (after saving to CSV and printing initial statistics)...
# 1. Create a stacked bar chart of languages (Existing vs Assigned)
plt.figure(figsize=(12, 6))
language_counts = pd.DataFrame({
    'Existing': simulation_df[~simulation_df['Assigned?']]['Language'].value_counts(),
    'Assigned': simulation_df[simulation_df['Assigned?']]['Language'].value_counts()
}).fillna(0)

language_counts.plot(kind='bar', stacked=True)
plt.title('Distribution of Languages (Existing vs Assigned)')
plt.xlabel('Language')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Status')
plt.tight_layout()
plt.savefig('language_distribution.png')
plt.close()

# 2. Create a heatmap of Gear Type and Color combinations
plt.figure(figsize=(12, 8))
heatmap_data = pd.crosstab(simulation_df['Gear Type'], simulation_df['Color'])
plt.imshow(heatmap_data, cmap='YlOrRd')
plt.colorbar(label='Count')
plt.title('Distribution of Gear Type and Color Combinations')
plt.xlabel('Color')
plt.ylabel('Gear Type')
plt.xticks(range(len(heatmap_data.columns)), heatmap_data.columns, rotation=45, ha='right')
plt.yticks(range(len(heatmap_data.index)), heatmap_data.index)
plt.tight_layout()
plt.savefig('gear_color_heatmap.png')
plt.close()

# 3. Create a bar chart of assignment probabilities
plt.figure(figsize=(12, 6))
assigned_probs = simulation_df[simulation_df['Assigned?']].groupby('Language')['Probability'].mean()
plt.bar(assigned_probs.index, assigned_probs.values)
plt.title('Average Assignment Probabilities by Language')
plt.xlabel('Language')
plt.ylabel('Average Probability')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('assignment_probabilities.png')
plt.close()

print("\nVisualizations have been created:")
print("1. language_distribution.png - Shows distribution of existing vs assigned languages")
print("2. gear_color_heatmap.png - Shows distribution of gear type and color combinations")
print("3. assignment_probabilities.png - Shows average probabilities for assigned languages")

# Optional: Display some numerical summaries
print("\nNumerical Summaries:")
print("\nTotal counts by language:")
print(simulation_df['Language'].value_counts())

print("\nAverage probabilities for assigned languages:")
print(assigned_probs.round(4))

print("\nMost common gear type and color combinations:")
print(pd.crosstab(simulation_df['Gear Type'], simulation_df['Color']).stack().sort_values(ascending=False).head())
