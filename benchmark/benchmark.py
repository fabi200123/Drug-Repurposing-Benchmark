import json
import os

# List of all ATC codes
ALL_ATC_CODES = [
    "V", "M", "D", "B", "S", "N", "L", "G", "J", "P", "A", "R", "C", "H"
]

# Algorithm output path and true data path
algorithm_output_path = "algorithm_outputs"
true_data_path = "test_data/true_data.json"

# The function to read the algorithm outputs and the true data and return them
def read_algorithm_outputs(algorithm_output_path, true_data_path):
    algorithm_outputs = {}
    # Iterate through all files in the folder
    for filename in os.listdir(algorithm_output_path):
        # Check if the file has a .json extension
        if filename.endswith(".json"):
            file_path = os.path.join(algorithm_output_path, filename)

            # Extract the algorithm name (filename without extension)
            algorithm_name = os.path.splitext(filename)[0]

            # Open and load the JSON file
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    algorithm_outputs[algorithm_name] = data
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {filename}: {e}")
    
    with open(true_data_path, 'r') as f:
        try:
            true_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {true_data_path}: {e}")

    return algorithm_outputs, true_data


# Function to compare the output of the algorithm with the expected output
def benchmark_atc_comparison(reference, output):
    score = 0
    
    for code in ALL_ATC_CODES:
        reference_set = set(reference.get(code, []))
        output_set = set(output.get(code, []))
        
        # Add +1 for correctly matched drugs
        correct_matches = reference_set & output_set
        score += len(correct_matches)
        
        # Subtract -1 for incorrect drugs in the output
        incorrect_matches = output_set - reference_set
        score -= len(incorrect_matches)
        
        # # Subtract -1 for missing drugs in the output
        # missing_matches = reference_set - output_set
        # score -= len(missing_matches)
    
    return score

# Main function to run the benchmark
def main():
    # Read the algorithm outputs and the true data
    algorithms_output, true_data = read_algorithm_outputs(algorithm_output_path, true_data_path)

    # Calculate the benchmark score for each algorithm
    scores = {}
    for algorithm_name, algorithm_output in algorithms_output.items():
        score = benchmark_atc_comparison(true_data, algorithm_output)
        scores[algorithm_name] = score

    # Print the result
    print(scores)

if __name__ == "__main__":
    main()