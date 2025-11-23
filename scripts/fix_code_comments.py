#!/usr/bin/env python3
"""
Fix code comments in markdown files:
- Convert # comments to docstrings in Python code blocks
- Ensure consistent code block markers
- Use // style comments for languages that support it
"""

import re
from pathlib import Path
from typing import List, Tuple

def convert_python_comments_to_docstrings(content: str) -> str:
    """Convert standalone # comments in Python code blocks to docstrings."""
    lines = content.split('\n')
    result = []
    in_python_block = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for code block markers
        stripped = line.strip()
        if stripped.startswith('```'):
            # Check if it's Python
            if 'python' in stripped.lower():
                in_python_block = True
            elif stripped == '```':
                in_python_block = False
            result.append(line)
            i += 1
            continue
        
        if in_python_block:
            # Inside Python code block - convert standalone # comments to docstrings
            # Only convert lines that are ONLY comments (not inline comments)
            if re.match(r'^\s+#\s+[A-Z]', line):  # Comment starting with capital (likely documentation)
                # Check if it's a standalone comment (not inline)
                if not re.search(r'[=+\-*/]\s*#', line):  # Not inline comment
                    indent = len(line) - len(line.lstrip())
                    comment_text = line.strip()[1:].strip()
                    
                    # Check if next line is also a comment - collect consecutive comments
                    comments = [comment_text]
                    j = i + 1
                    while j < len(lines) and j < i + 5:  # Limit to 5 consecutive comment lines
                        next_line = lines[j]
                        if next_line.strip() == '':
                            break
                        if re.match(r'^\s+#\s+', next_line) and not re.search(r'[=+\-*/]\s*#', next_line):
                            comments.append(next_line.strip()[1:].strip())
                            j += 1
                        else:
                            break
                    
                    # Convert to docstring only if it's documentation-style
                    if len(comments) <= 3:  # Only convert short comment blocks
                        if len(comments) == 1:
                            result.append(' ' * indent + f'""" {comments[0]} """')
                        else:
                            result.append(' ' * indent + '"""')
                            for comment in comments:
                                result.append(' ' * indent + comment)
                            result.append(' ' * indent + '"""')
                        i = j
                        continue
            
            result.append(line)
            i += 1
        else:
            result.append(line)
            i += 1
    
    return '\n'.join(result)

def detect_language_from_content(code_lines: List[str]) -> str:
    """Detect programming language from code content."""
    code_text = '\n'.join(code_lines[:10])  # Check first 10 lines
    
    # Python indicators
    if any(indicator in code_text for indicator in ['def ', 'import ', 'from ', 'print(', 'if __name__', 'class ', '->']):
        return 'python'
    
    # JavaScript/TypeScript
    if any(indicator in code_text for indicator in ['function ', 'const ', 'let ', 'var ', '=>', 'console.log']):
        return 'javascript'
    
    # Bash/Shell
    if any(indicator in code_text for indicator in ['#!/bin/', 'echo ', 'export ', '$', 'if [']):
        return 'bash'
    
    # YAML
    if ':' in code_text and ('---' in code_text or code_text.strip().startswith('apiVersion:')):
        return 'yaml'
    
    # HCL/Terraform
    if any(indicator in code_text for indicator in ['resource "', 'variable "', 'provider "', 'terraform {']):
        return 'hcl'
    
    # Groovy
    if 'pipeline {' in code_text or 'stage(' in code_text:
        return 'groovy'
    
    # Markdown
    if code_text.strip().startswith('#') or '**' in code_text:
        return 'markdown'
    
    return 'text'

def ensure_consistent_code_blocks(content: str) -> str:
    """Ensure all code blocks have consistent start/stop markers with language."""
    lines = content.split('\n')
    result = []
    in_code_block = False
    current_language = None
    code_block_start = None
    code_block_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        if stripped.startswith('```'):
            if not in_code_block:
                # Opening fence
                in_code_block = True
                code_block_start = len(result)  # Track position in result list
                code_block_lines = []
                
                # Extract language if present (handle both ```python and ```python {data-source-line="..."})
                if len(stripped) > 3:
                    # Remove any trailing attributes like {data-source-line="..."}
                    lang_part = stripped[3:].strip().split()[0].split('{')[0].strip()
                    current_language = lang_part if lang_part else None
                    result.append(f'```{current_language}')
                else:
                    # No language specified - we'll detect it from content
                    result.append('```')  # Placeholder, will update after reading content
                    current_language = None
            else:
                # Closing fence - ALWAYS strip any language/attributes, always just ```
                # The closing fence should NEVER have a language marker
                # If we didn't have a language, detect it now and update opening
                if current_language is None and code_block_lines:
                    detected = detect_language_from_content(code_block_lines)
                    # Update the opening fence in result
                    if code_block_start < len(result):
                        opening_line = result[code_block_start]
                        if opening_line.strip() == '```':
                            result[code_block_start] = f'```{detected}'
                    current_language = detected
                
                in_code_block = False
                # Closing fence is ALWAYS just ``` (strip any language/attributes that might be present)
                # Even if the source has ```markdown or ```text, we output just ```
                result.append('```')
                current_language = None
                code_block_lines = []
        else:
            if in_code_block:
                code_block_lines.append(line)
            result.append(line)
        
        i += 1
    
    return '\n'.join(result)

def fix_file(file_path: Path) -> None:
    """Fix comments and code blocks in a single file."""
    print(f"Processing {file_path.name}...")
    content = file_path.read_text(encoding='utf-8')
    
    # First ensure consistent code blocks
    content = ensure_consistent_code_blocks(content)
    
    # Then convert Python comments
    content = convert_python_comments_to_docstrings(content)
    
    file_path.write_text(content, encoding='utf-8')
    print(f"  ✅ Fixed {file_path.name}")

def main():
    """Main function to fix all markdown files."""
    project_root = Path(__file__).parent.parent
    docs_dir = project_root / "docs"
    
    if not docs_dir.exists():
        print(f"Error: Docs directory not found at {docs_dir}")
        return
    
    print("Fixing code comments and ensuring consistent code blocks...")
    print("=" * 60)
    
    # Process all markdown files
    for md_file in docs_dir.glob("*.md"):
        fix_file(md_file)
    
    print("=" * 60)
    print("✅ All files processed!")
    print("\nNote: This converts # comments to docstrings in Python code blocks.")
    print("You may want to review the changes before committing.")

if __name__ == "__main__":
    main()

