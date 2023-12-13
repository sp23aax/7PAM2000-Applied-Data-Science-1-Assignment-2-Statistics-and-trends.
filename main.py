# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 10:54:32 2023

@author: Saikiran (sp23aax)
"""
# Bringing in the necessary libraries.
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#  A function to retrieve data.
def transpose_world_bank_data(filename):
    """
    Retrieve and reorganize World Bank data from the given CSV file by reading and transposing it.
    
    Parameters:
    - filename (str): The Path to the World Bank data CSV file.
    
    Returns:
    - original_df (pd.DataFrame): Original DataFrame.
    - transposed_df (pd.DataFrame): Transposed DataFrame.
    """
    # Importing the CSV file and creating a Pandas DataFrame with its contents.
    df = pd.read_csv(filename)

    # Transpose the DataFrame to have countries as columns and years as one column
    transposed_df = df.set_index(['Country Name', 'Indicator Name']).stack().unstack(0).reset_index()

    # Altering the column names.
    transposed_df.columns.name = None

    return df, transposed_df


# Substituting 'my_file.csv' with the actual filepath to my World Bank data CSV file.
file_path = 'Indicators.csv'

# Call the function to get the original and transposed DataFrames
original_df, transposed_df = transpose_world_bank_data(file_path)

# Display the first few rows of the transposed DataFrame
print(transposed_df.head())

transposed_df.to_csv('transposed.csv')

original_df.to_csv('original.csv')

# Descriptive Statistics with Few Countries.
# Select a few countries and indicators of interest
selected_countries = ['Pakistan', 'Nepal']
selected_indicators = ['Arable land (% of land area)', 'Access to electricity (% of population)']

# Applying a filter to the DataFrame based on selected countries and indicators
selected_data = original_df[original_df['Country Name'].isin(selected_countries) & original_df['Indicator Name'].isin(selected_indicators)]

# Droping the non-numeric columns for statical analysis
selected_data_numeric = selected_data.drop(['Country Name','Indicator Name'], axis=1)

# Explore statistical properties using .describe()
summary_stats = selected_data_numeric.describe()

# Calculate mean, median, and standard deviation
mean_values = selected_data_numeric.mean()
median_values = selected_data_numeric.median()
std_dev_values = selected_data_numeric.std()

# Display the results
print("Summary Statistics:")
print(summary_stats)

print("\nMean Values:")
print(mean_values)

print("\nMedian Values:")
print(median_values)

print("\nStandard Deviation:")
print(std_dev_values)

# Loading the transposed DataFrame from the CSV file. 
transposed=pd.read_csv('transposed.csv')

#line chart for Access to Electricity
selected_data = transposed[(transposed['Indicator Name'] == 'Access to electricity (% of population)') &
                   (transposed['Year'].notna())]  # Ensure there's a valid year

# Select only the relevant columns
selected_data = selected_data[['Year', 'Pakistan', 'Afghanistan', 'Australia']]
grouped_data = selected_data.groupby('Year').sum()

# Plot the line chart
plt.figure(figsize=(10, 6))
plt.plot(grouped_data.index, grouped_data['Pakistan'], label='Pakistan')
plt.plot(grouped_data.index, grouped_data['Afghanistan'], label='Afghanistan')
plt.plot(grouped_data.index, grouped_data['Australia'], label='Australia')

plt.title('Access to electricity (% of population) - Pakistan, Afghanistan, Australia')
plt.xlabel('Year')
plt.ylabel('Access to electricity (% of population)')
plt.legend()
plt.grid(True)
plt.show()

# Bar Chart Comparison
selected_data = transposed_df[transposed_df['Indicator Name'] == 'Arable land (% of land area)'][
    ['Australia', 'India', 'Afghanistan', 'Nepal']]

# Aggregate the values for Nepal, India, and Pakistan
aggregated_data = selected_data.sum()

# Create a bar chart
aggregated_data.plot(kind='bar', color=['blue', 'orange', 'green', 'red'], figsize=(10, 6))
plt.title('Arable Land - Nepal, India, Pakistan')
plt.xlabel('Country')
plt.ylabel('Arable Land Values')
plt.show()

# Pie Chart
perception = original_df[original_df['Indicator Name'] == 'Average precipitation in depth (mm per year)'].copy()
years_columns = original_df.columns[2:]
perception['Total'] = perception[years_columns].sum(axis=1)
top5_countries = perception.nlargest(5, 'Total')

plt.figure(figsize=(10, 8))
plt.pie(top5_countries['Total'], labels=top5_countries['Country Name'], autopct='%1.1f%%', startangle=90)
plt.legend(bbox_to_anchor=(1, 0.5), loc="center left", title="Country Name", bbox_transform=plt.gcf().transFigure)
plt.title('Top 5 Countries With Perception')
plt.show()
