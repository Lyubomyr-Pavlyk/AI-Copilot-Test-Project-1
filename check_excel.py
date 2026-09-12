import pandas as pd

# Placeholder for Read_Data_FIle
def Read_Data_File(file_name):
    try:
        df = pd.read_excel(file_name)

        # Ensure we're extracting numbers from a single column.
        Numbers = df.iloc[:, 0].dropna().astype(float).values

        return Numbers

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Function to calculate the average
def calculate_average(numbers):
    if not numbers.size:
        return None
    return float(sum(numbers) / len(numbers))

# Function to calculate the median
def calculate_median(numbers):
    if not numbers.size:
        return None
    return statistics.median(numbers)

# Main function to test the median and average calculations
file_name = 'somefile.xlsx'  # Change this to your Excel file name.
Numbers = Read_Data_File(file_name)

if Numbers:
    Average = calculate_average(Numbers)
    Median = calculate_median(Numbers)

    print(f"The Average is: {Average}")
    print(f"The Median is: {Median}")