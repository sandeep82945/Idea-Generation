import os
import shutil

# Define the paths to your folders
source_folder = 'data/WF_paper_text/physics'
exclude_folder = 'verification_data/physics'
destination_folder = 'data/WF_paper_text/physics_annotated'

# Ensure destination folder exists
os.makedirs(destination_folder, exist_ok=True)

# List all .txt files in both folders
source_files = {file for file in os.listdir(source_folder) if file.endswith('.txt')}
exclude_files = {file for file in os.listdir(exclude_folder) if file.endswith('.txt')}

# Determine which .txt files are in both source_folder and exclude_folder
files_to_move = source_files & exclude_files

# Move these files to destination_folder
for file in files_to_move:
    shutil.move(os.path.join(source_folder, file), os.path.join(destination_folder, file))

print(f'Moved {len(files_to_move)} files to {destination_folder}')
