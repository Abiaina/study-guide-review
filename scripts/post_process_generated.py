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
    
    # Fix 1: Remove language markers from closing fences
    # Pattern: ```language at end of line (closing fence)
    # We need to be careful - only fix closing fences, not opening ones
    lines = content.split('\n')
    fixed_lines = []
    in_code_block = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        if stripped.startswith('```'):
            if not in_code_block:
                # Opening fence - keep as is (may have language)
                in_code_block = True
                fixed_lines.append(line)
            else:
                # Closing fence - strip any language markers
                in_code_block = False
                # Always output just ```
                fixed_lines.append('```')
        else:
            fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Fix 2: Fix any broken code blocks (like "for x in nums:\n```python")
    # This shouldn't happen, but just in case
    content = re.sub(r'(for x in nums:\n)```python', r'\1    print(x)', content)
    
    # Fix 3: Ensure code fence balance
    # Count opening and closing fences
    opening_count = len(re.findall(r'^```[a-z]+\s*$', content, re.MULTILINE))
    closing_count = len(re.findall(r'^```\s*$', content, re.MULTILINE))
    
    # If we have more opening than closing, we might have an issue
    # But this is just a check, not a fix (fixing would be complex)
    
    if content != original_content:
        file_path.write_text(content, encoding='utf-8')
        print(f"  ✅ Fixed {file_path.name}")
        print(f"     Opening fences: {opening_count}, Closing fences: {closing_count}")
    else:
        print(f"  ✅ {file_path.name} already clean")
        print(f"     Opening fences: {opening_count}, Closing fences: {closing_count}")

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

