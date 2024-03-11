# import os

# def generate_and_save_prompts(original_folder_path, new_folder_name=None):
#     if not new_folder_name:
#         new_folder_name = f"{original_folder_path}_prompts"
    
#     print(f"Creating directory: {new_folder_name}")
#     os.makedirs(new_folder_name, exist_ok=True)
    
#     files_processed = 0
    
#     for filename in os.listdir(original_folder_path):
#         if filename.endswith('.txt'):  # Process only .txt files
#             original_file_path = os.path.join(original_folder_path, filename)
            
#             print(f"Processing file: {filename}")
            
#             try:
#                 with open(original_file_path, 'r', encoding='utf-8') as file:
#                     paper_text = file.read()
#             except UnicodeDecodeError:
#                 try:
#                     with open(original_file_path, 'r', encoding='ISO-8859-1') as file:
#                         paper_text = file.read()
#                 except UnicodeDecodeError:
#                     print(f"Skipping file due to encoding issues: {filename}")
#                     continue
            
#             prompt = f"""Imagine you are a research scientist, read the following paper and generate 5 possible future research ideas after brainstorming:  
# ``` {paper_text}```
# 5 possible future research ideas from the paper are: """
            
#             prompt_file_path = os.path.join(new_folder_name, filename)
            
#             with open(prompt_file_path, 'w', encoding='utf-8') as prompt_file:
#                 prompt_file.write(prompt)
            
#             files_processed += 1
    
#     if files_processed > 0:
#         print(f"Prompts generated and saved successfully in {new_folder_name}. Total files processed: {files_processed}")
#     else:
#         print("No text files found or processed.")

# # Example usage
# original_folder_path = 'data/final'  # Update this path
# generate_and_save_prompts(original_folder_path)

import os

def generate_and_save_prompts(base_folder_path, new_base_folder_name=None):
    # Create the base directory for all prompts if it does not exist
    if not new_base_folder_name:
        new_base_folder_name = f"{base_folder_path}_prompts"
    os.makedirs(new_base_folder_name, exist_ok=True)
    
    # Function to process each file
    def process_file(original_file_path, relative_path):
        try:
            with open(original_file_path, 'r', encoding='utf-8') as file:
                paper_text = file.read()
        except UnicodeDecodeError:
            try:
                with open(original_file_path, 'r', encoding='ISO-8859-1') as file:
                    paper_text = file.read()
            except UnicodeDecodeError:
                print(f"Skipping file due to encoding issues: {original_file_path}")
                return
        
        prompt = f"""Imagine you are a research scientist, read the following paper and generate top 5 possible future research ideas after brainstorming:  
``` {paper_text}```
5 possible future research ideas from the paper are: """
        
        # Create subdirectory in new base folder if it doesn't exist
        new_dir_path = os.path.join(new_base_folder_name, os.path.dirname(relative_path))
        os.makedirs(new_dir_path, exist_ok=True)
        
        prompt_file_path = os.path.join(new_base_folder_name, relative_path)
        
        with open(prompt_file_path, 'w', encoding='utf-8') as prompt_file:
            prompt_file.write(prompt)
    
    # Function to recursively process each directory
    def process_directory(directory, relative_path=""):
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isdir(full_path):
                process_directory(full_path, os.path.join(relative_path, entry))
            elif entry.endswith('.txt'):
                process_file(full_path, os.path.join(relative_path, entry))
    
    # Start processing from the base folder
    process_directory(base_folder_path)
    
    print(f"Prompts generated and saved successfully in {new_base_folder_name}.")

# Example usage
base_folder_path = 'data/final'  # Update this path
generate_and_save_prompts(base_folder_path)

