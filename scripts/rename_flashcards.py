#!/usr/bin/env python3
"""
Script to rename flashcard files to remove emojis from filenames.
"""

import os
import re
import glob

def rename_flashcard_files():
    """Rename flashcard files to remove emojis from filenames."""
    flashcard_dir = 'generated/flashcards'
    
    # Mapping of emoji prefixes to clean names
    emoji_mapping = {
        '⚡': 'common-interview-patterns',
        '🌳': 'tree-traversal-pattern',
        '🎯': 'problem-type-algorithm-pattern',
        '📊': 'heap-pattern',
        '🔄': 'backtracking-pattern',
        '🔢': 'binary-search-pattern',
        '🕸️': 'graph-traversal-pattern',
        '🪟': 'sliding-window-pattern',
        '🎒': 'knapsack-pattern',
        '💰': 'classic-dp-pattern',
        '🔍': 'two-pointers-pattern'
    }
    
    # Get all flashcard files
    flashcard_files = glob.glob(f'{flashcard_dir}/*.md')
    
    renamed_count = 0
    for file_path in flashcard_files:
        filename = os.path.basename(file_path)
        
        # Check if filename starts with an emoji
        for emoji, clean_name in emoji_mapping.items():
            if filename.startswith(f'{emoji}-'):
                # Create new filename
                new_filename = f'{clean_name}-flashcards.md'
                new_file_path = os.path.join(flashcard_dir, new_filename)
                
                # Rename the file
                try:
                    os.rename(file_path, new_file_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                    renamed_count += 1
                    break
                except Exception as e:
                    print(f"Error renaming {filename}: {e}")
    
    print(f"\nRenamed {renamed_count} flashcard files.")

if __name__ == "__main__":
    rename_flashcard_files()
