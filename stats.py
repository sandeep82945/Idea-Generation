from transformers import GPT2Tokenizer
import os

def count_tokens_in_folder(folder_path):
    # Load the GPT-2 tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
    
    total_tokens = 0
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                # Tokenize the text and count the number of tokens
                tokens = tokenizer.tokenize(text)
                file_tokens = len(tokens)
                total_tokens += file_tokens
                print(f"{filename}: {file_tokens} tokens")
    return total_tokens

folder_path = 'path/to/your/folder'  # Replace with your folder path
total_tokens = count_tokens_in_folder(folder_path)
print(f"Total GPT-2 tokens in folder (similar to GPT-4): {total_tokens}")
