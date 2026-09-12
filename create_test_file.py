import pandas as pd

# Create a DataFrame with some example numbers
data = {'Numbers': [10, 20, 30, 40, 50]}
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
df.to_excel('test_numbers.xlsx', index=False)