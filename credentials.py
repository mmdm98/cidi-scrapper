import os

# Function to read CUIL and password from text file
def read_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 2:
                cuil = lines[0].strip()
                password = lines[1].strip()
                return cuil, password
            else:
                print(f"Error: File '{file_path}' does not contain enough lines.")
                return None, None
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None, None
    except Exception as e:
        print(f"Error reading credentials from {file_path}: {e}")
        return None, None
 
def read_paths_from_file(file_path):
    paths = []
    try:
        with open(file_path, 'r') as file:
            paths = [line.strip() for line in file.readlines()]
    except Exception as e:
        print(f"Error reading paths from {file_path}: {e}")
    return paths
