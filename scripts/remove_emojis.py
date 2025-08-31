#!/usr/bin/env python3
"""
Script to remove all emojis from markdown files in the study guide project.
"""

import os
import re
import glob

def remove_emojis_from_file(file_path):
    """Remove emojis from a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern to match common emojis used in the project
        emoji_pattern = re.compile(r'[⚡🌳🎒🎯💰📊🔄🔍🔢🕸️🪟🖨️]')
        
        # Remove emojis
        cleaned_content = emoji_pattern.sub('', content)
        
        # Write back to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        print(f"Cleaned: {file_path}")
        return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def main():
    """Remove emojis from all markdown files in the project."""
    # Get all markdown files
    md_files = []
    
    # Main docs directory
    md_files.extend(glob.glob('docs/*.md'))
    
    # Generated directory
    md_files.extend(glob.glob('generated/*.md'))
    md_files.extend(glob.glob('generated/flashcards/*.md'))
    
    # Root directory
    md_files.extend(glob.glob('*.md'))
    
    print(f"Found {len(md_files)} markdown files to process")
    
    success_count = 0
    for file_path in md_files:
        if remove_emojis_from_file(file_path):
            success_count += 1
    
    print(f"\nCompleted! Processed {success_count}/{len(md_files)} files successfully.")

if __name__ == "__main__":
    main()
