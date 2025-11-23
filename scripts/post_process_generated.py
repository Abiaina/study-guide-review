#!/usr/bin/env python3
"""
Post-process the generated study guide to fix any remaining formatting issues.
This is a safety net to clean up any issues that the generation script might have missed.
"""

import re
from pathlib import Path

def post_process_generated_file(file_path: Path) -> None:
    """Post-process the generated file to fix remaining issues."""
    print(f"Post-processing {file_path.name}...")
    
    content = file_path.read_text(encoding='utf-8')
    original_content = content
    
    # Fix: Remove language markers from ALL closing fences
    # Process line by line, tracking code block state
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    
    for line in lines:
        stripped = line.strip()
        
        if stripped.startswith('```'):
            if not in_code_block:
                # Opening fence - keep as is (may have language)
                in_code_block = True
                fixed_lines.append(line)
            else:
                # Closing fence - ALWAYS strip any language markers
                # Check if it has more than just ```
                if len(stripped) > 3:
                    # Has language marker - strip it
                    fixed_lines.append('```')
                else:
                    # Already clean
                    fixed_lines.append('```')
                in_code_block = False
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Additional safety: Use regex to catch any remaining closing fences with language
    # This handles edge cases where state tracking might have been off
    # Replace any standalone ```language that should be just ```
    # We need to be careful - only replace closing fences, not opening ones
    
    # More aggressive approach: track state again and fix
    lines_final = content.split('\n')
    fixed_final = []
    in_code_final = False
    
    for i, line in enumerate(lines_final):
        stripped = line.strip()
        
        if stripped.startswith('```'):
            if not in_code_final:
                # Opening fence
                in_code_final = True
                fixed_final.append(line)
            else:
                # Closing fence - strip ALL language markers
                in_code_final = False
                # If stripped has more than 3 characters, it has a language marker
                if len(stripped) > 3:
                    fixed_final.append('```')
                else:
                    fixed_final.append('```')
        else:
            fixed_final.append(line)
    
    content = '\n'.join(fixed_final)
    
    # Fix broken code blocks (shouldn't happen, but safety net)
    content = re.sub(r'(for x in nums:\n)```python', r'\1    print(x)', content)
    
    # Verify and report
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        
        # Count for reporting
        in_code = False
        opening = 0
        closing = 0
        closing_with_lang = 0
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('```'):
                if not in_code:
                    opening += 1
                    in_code = True
                else:
                    closing += 1
                    if len(stripped) > 3:
                        closing_with_lang += 1
                    in_code = False
        
        print(f"  ✅ Fixed {file_path.name}")
        print(f"     Opening fences: {opening}, Closing fences: {closing}")
        print(f"     Closing fences with language: {closing_with_lang}")
    else:
        # Count for reporting even if no changes
        in_code = False
        opening = 0
        closing = 0
        closing_with_lang = 0
        for line in content.split('\n'):
            stripped = line.strip()
            if stripped.startswith('```'):
                if not in_code:
                    opening += 1
                    in_code = True
                else:
                    closing += 1
                    if len(stripped) > 3:
                        closing_with_lang += 1
                    in_code = False
        
        print(f"  ✅ {file_path.name} processed")
        print(f"     Opening fences: {opening}, Closing fences: {closing}")
        print(f"     Closing fences with language: {closing_with_lang}")

def main():
    """Main function to post-process generated files."""
    project_root = Path(__file__).parent.parent
    generated_file = project_root / "generated" / "study-guide-complete-printable.md"
    
    if not generated_file.exists():
        print(f"Error: Generated file not found at {generated_file}")
        return
    
    print("=" * 60)
    print("Post-processing generated study guide...")
    print("=" * 60)
    
    post_process_generated_file(generated_file)
    
    print("=" * 60)
    print("✅ Post-processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()
