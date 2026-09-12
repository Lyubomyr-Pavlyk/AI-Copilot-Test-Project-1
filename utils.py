import statistics

def calculate_average(numbers):
    return sum(numbers) / len(numbers)

def calculate_median(numbers):
    return statistics.median(numbers)