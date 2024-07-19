
import csv
# Paths to your input and output files
input_file_path = 'heart_transactionsfinal2023.csv'
output_file_path = 'converted_heart_transactions.txt'

# Read the dataset
with open(input_file_path, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    headers = reader.fieldnames

    # Mapping headers to integers
    feature_map = {name: idx + 1 for idx, name in enumerate(headers)}

    # Open the output file
    with open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
        # For each row in the input file
        for row in reader:
            # Create a transaction list containing the integers for features that are '1' or 'True'
            transaction = [str(feature_map[key]) for key, value in row.items() if value == '1' or value.strip().lower() == 'true']
            # Write the transaction to the output file, separating items with spaces
            outfile.write(' '.join(transaction) + '\n')

# Print out the feature map to understand what each integer represents
print("Feature to integer mapping:")
for key, value in feature_map.items():
    print(f"{key}: {value}")
    
# asymptomatic: 1
# atypical_angina: 2
# cholhigh: 3
# chollow: 4
# cholnormal: 5
# downsloping: 6
# elderly: 7
# exercise_angina0: 8
# exercise_angina1: 9
# fasting_blood_sugar0: 10
# fasting_blood_sugar1: 11
# female: 12
# flat: 13
# heart_disease: 14
# heart_rate_high: 15
# heart_rate_low: 16
# heart_rate_normal: 17
# man: 18
# middle-aged: 19
# no_heart_disease: 20
# non_anginal_pain: 21
# oldpeakhigh: 22
# oldpeaklow: 23
# oldpeakmoderate: 24
# typical_angina: 25
# upsloping: 26
# young: 27

# Optionally, print the first few lines of the output file to check
print("\nFirst few transactions from the output file:")
with open(output_file_path, 'r') as file:
    for _ in range(5):
        print(file.readline().strip())


# # Open the input file in read mode and the output file in write mode
# with open(input_file_path, 'r') as infile, open(output_file_path, 'w', newline='') as outfile:
#     reader = csv.reader(infile)
#     writer = csv.writer(outfile)

#     # Read the header (column names) and write it as is
#     headers = next(reader)
#     writer.writerow(headers)

#     # Iterate over each row in the CSV
#     for row in reader:
#         # Convert 'True' to '1' and 'False' to '0', and convert each cell to string
#         converted_row = ['1' if cell == 'True' else '2' if cell == 'False' else str(cell) for cell in row]
#         # Join the converted row with spaces and write to the output file
#         outfile.write(' '.join(converted_row) +' ' + '\n')

# print("Conversion complete. The file has been saved to", output_file_path)
