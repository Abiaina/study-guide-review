#!/usr/bin/env python3
"""
Script to remove all emojis from programming_languages.md
"""

import re
import sys

def remove_emojis(text):
    """Remove emojis from text using regex patterns"""
    # Pattern to match most emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002702-\U000027B0"  # dingbats
        "\U000024C2-\U0001F251"  # enclosed characters
        "]+", flags=re.UNICODE
    )
    
    # Remove emojis
    text = emoji_pattern.sub('', text)
    
    # Also remove common emoji characters that might not be caught by the above pattern
    text = re.sub(r'[🀄-🿕]', '', text)
    
    return text

def main():
    file_path = "docs/programming_languages.md"
    
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove emojis
        cleaned_content = remove_emojis(content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Successfully removed emojis from {file_path}")
        
    except FileNotFoundError:
        print(f"Error: File {file_path} not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
