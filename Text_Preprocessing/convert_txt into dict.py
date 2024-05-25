# Read the contents of the file
file_path = 'E:\Project Commit\Data Accquisition\web scraping\slang.txt'
with open(file_path, 'r') as file:
    lines = file.readlines()

# Initialize an empty dictionary
slang_dict = {}

# Iterate through each line to populate the dictionary
for line in lines:
    line = line.strip()  # Remove leading/trailing whitespace
    if '=' in line:
        # Split the line into key and value
        key, value = line.split('=', 1)
    elif ' – ' in line:
        key, value = line.split(' – ', 1)
    elif ': ' in line:
        key, value = line.split(': ', 1)
    else:
        continue

    # Add the key-value pair to the dictionary
    slang_dict[key] = value

# Print the resulting dictionary
print(slang_dict)
