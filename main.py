from agent import *

import utils

# Placeholder for Read_Data_FIle
def Read_Data_FIle(file_name):
    # Open the file in read mode, assuming each line is a number separated by newline.
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

        # Strip whitespace and convert to numbers (int or float depending on your needs)
        Numbers = [float(line.strip()) for line in lines if line.strip()]

        return Numbers

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Main function to test the median calculation
def main():
    file_name = 'somefile.txt'
    Numbers = Read_Data_FIle(file_name)
    if Numbers:
        Median = utils.calculate_median(Numbers)
        print(f"The Median is: {Median}")

        Average = utils.calculate_average(Numbers)
        print(f"The Average is: {Average}")
    else:
        print("No numbers found in the file.")

if __name__ == '__main__':
    main()