#!/usr/bin/env python3
"""
Generate a complete study guide that consolidates:
1. All documentation from docs/ directory
2. All flashcards from generated/flashcards/ directory
3. Creates a single printable file for book printing

This ensures no important study guide information is lost.
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Define the order and structure for the combined document
DOCUMENT_STRUCTURE = [
    {
        "title": "Core Fundamentals",
        "sections": [
            ("Core_Data_Structures.md", "Data Structures Overview"),
            ("algo.md", "Algorithms & Data Structures"),
            ("graphs_linked_lists.md", "Complex Data Structures (Trees, Graphs)"),
            ("search.md", "Searching & Sorting Algorithms"),
            ("sliding_window.md", "Sliding Window Algorithms"),
            ("frontend.md", "Frontend Development"),
            ("programming_languages.md", "Programming Languages & Tools"),
        ]
    },
    {
        "title": "System Design & Architecture",
        "sections": [
            ("system_design.md", "System Design Problems"),
            ("data_layer.md", "Data Layer & Databases"),
            ("design_patterns.md", "Design Patterns"),
        ]
    },
    {
        "title": "DevOps & Cloud",
        "sections": [
            ("cicd.md", "CI/CD & Infrastructure"),
            ("reliability.md", "Reliability Engineering (Internet Fundamentals, Observability, Chaos Engineering, Load Testing)"),
        ]
    },
    {
        "title": "Security & Compliance",
        "sections": [
            ("security_compliance.md", "Security & Compliance"),
        ]
    },
    {
        "title": "Quick Reference & Cheat Sheets",
        "sections": [
            ("cheat_sheet.md", "Comprehensive Cheat Sheet"),
        ]
    }
]

# Flashcard files to include (in order of importance)
FLASHCARD_FILES = [
    "FLASHCARD_DECK_SUMMARY.md",
    "common-interview-patterns-flashcards.md",
    "sliding-window-pattern-flashcards.md",
    "two-pointers-pattern-flashcards.md",
    "fast-slow-pointers-pattern-flashcards.md",
    "prefix-suffix-pattern-flashcards.md",
    "greedy-pattern-flashcards.md",
    "binary-search-pattern-flashcards.md",
    "backtracking-pattern-flashcards.md",
    "classic-dp-pattern-flashcards.md",
    "knapsack-pattern-flashcards.md",
    "monotonic-stack-pattern-flashcards.md",
    "graph-traversal-pattern-flashcards.md",
    "tree-traversal-pattern-flashcards.md",
    "heap-pattern-flashcards.md",
    "greedy-threshold-tracking-pattern-flashcards.md",
    "hash-map-frequency-tracking-pattern-flashcards.md",
    "intervals-pattern-flashcards.md",
    "problem-type-algorithm-pattern-flashcards.md",
    "back-side-(solution-pattern)-flashcards.md",
]

def read_markdown_file(file_path: Path) -> str:
    """Read a markdown file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Warning: File {file_path} not found")
        return ""
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def clean_markdown_file(file_path: Path, is_printable: bool = True) -> str:
    """Clean and format a single markdown file - processes file individually before combining."""
    if not file_path.exists():
        return ""
    
    # Read the file
    content = read_markdown_file(file_path)
    if not content:
        return ""
    
    # Clean the content
    return clean_markdown_content(content, is_printable=is_printable)

def clean_markdown_content(content: str, is_printable: bool = True) -> str:
    """Clean and format markdown content for the target format.
    
    This function processes individual files before they are combined.
    It handles:
    - Removing front matter
    - Removing emojis (for printable version)
    - Preserving code blocks correctly
    """
    if not content:
        return ""
    
    # Remove front matter (YAML headers)
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Remove title from content if it's the first line (we'll add our own)
    # Only remove if it's a standalone # title at the start
    lines = content.split('\n')
    if lines and lines[0].startswith('# '):
        # Check if it's just a title with nothing else on that line
        if len(lines[0].strip()) == len(lines[0]) and (len(lines) == 1 or lines[1].strip() == ''):
            content = '\n'.join(lines[1:]).lstrip('\n')
    
    if is_printable:
        # For printable version, remove emojis
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        content = emoji_pattern.sub('', content)
        
        # Fix indented code blocks: Markdown treats lines starting with 4 spaces as code blocks
        # We need to detect indented code and wrap it in proper code fences
        # IMPORTANT: We must NOT process lines that are inside existing code fences
        lines = content.split('\n')
        fixed_lines = []
        in_code_fence = False
        code_fence_language = None  # Track the language of the code fence
        
        i = 0
        while i < len(lines):
            line = lines[i]
            original_line = line  # Keep original for debugging
            
            # Track code fence state - be very strict about this
            # Check if line contains a code fence marker (```)
            stripped_line = line.strip()
            
            # Check for code fence - must be at start of line (after optional whitespace) or standalone
            # This handles both ```python and ``` on their own lines, and ```python after text like "**Back:** ```python"
            code_fence_match = None
            if stripped_line.startswith('```'):
                # Code fence at start of line
                code_fence_match = (0, stripped_line)
            elif '```' in line:
                # Code fence somewhere in line (like "**Back:** ```python")
                match = re.search(r'```', line)
                if match:
                    fence_pos = match.start()
                    fence_text = line[fence_pos:].strip()
                    code_fence_match = (fence_pos, fence_text)
            
            if code_fence_match:
                # This line contains a code fence marker
                fence_pos, fence_text = code_fence_match
                
                if not in_code_fence:
                    # Opening fence
                    in_code_fence = True
                    # Extract language if present (e.g., ```python)
                    if len(fence_text) > 3:
                        code_fence_language = fence_text[3:].strip().split()[0] if ' ' in fence_text[3:] else fence_text[3:].strip() or None
                    else:
                        code_fence_language = None
                else:
                    # Closing fence - ALWAYS strip language markers, output just ```
                    # Even if source has ```markdown or ```text, output just ```
                    # This handles cases where closing fence has language like ```markdown or ```text
                    in_code_fence = False
                    code_fence_language = None
                    # Always output just ``` regardless of what the source had
                    fixed_lines.append('```')
                    i += 1
                    continue
            
            # CRITICAL: If we're in a code fence, keep EVERYTHING as-is (including indented lines)
            # Do NOT process indented lines inside code fences - they're part of the code!
            # This includes ALL lines, regardless of indentation, until we see the closing fence
            if in_code_fence:
                # We're inside a code fence - preserve everything exactly as-is
                fixed_lines.append(line)
                i += 1
                continue
                
            # Process both indented code AND non-indented code that starts with # comments
            # # comments followed by code need to be in code blocks to prevent markdown interpretation
            is_indented_code = line.startswith('    ') and len(line.strip()) > 0
            is_code_comment = (not line.startswith('    ') and line.strip().startswith('# ') and 
                              len(line.strip()) > 2 and not line.strip().startswith('##'))
            
            if is_indented_code or is_code_comment:
                # Safety check: look backwards for the most recent code fence
                # If we find an opening fence without a closing one, we're inside a code block
                recent_fence_state = False
                fence_count_backward = 0
                for j in range(i-1, max(-1, i-100), -1):  # Look back up to 100 lines
                    if j < 0:
                        break
                    check_line = lines[j].strip()
                    if check_line.startswith('```'):
                        fence_count_backward += 1
                        # If we've seen an odd number of fences, we're inside a code block
                        # (opening fence without matching closing fence)
                        if fence_count_backward % 2 == 1:
                            recent_fence_state = True
                        else:
                            recent_fence_state = False
                        break
                
                # If we detected we might be in a code fence, don't process this line
                if recent_fence_state:
                    # We're likely inside a code fence - preserve as-is
                    fixed_lines.append(line)
                    i += 1
                    continue
                
                # Handle both indented code and non-indented # comments
                if is_indented_code:
                    stripped = line[4:]  # Remove 4-space indent
                else:
                    # Non-indented # comment - check if it's followed by code
                    stripped = line.strip()
                    # Look ahead to see if next line is code
                    if i + 1 < len(lines):
                        next_line = lines[i + 1].strip()
                        # If next line is code (def, class, import, etc.), this comment is part of code
                        if not any(x in next_line for x in ['def ', 'class ', 'import ', 'from ', 'if ', 'for ', 'while ', 'return ', 'print(']):
                            # Not followed by code - might be markdown, skip
                            fixed_lines.append(line)
                            i += 1
                            continue
                
                # Check if it looks like code
                # IMPORTANT: # comments and """ docstrings MUST be in code blocks to avoid markdown interpretation
                code_indicators = ['def ', 'class ', 'import ', 'from ', 'return ', 'if ', 'for ', 'while ', 
                                 'print(', '->', 'async def', 'with ', 'try:', 'except', 'finally:', '"""', "'''",
                                 '=', '(', ')', '[', ']', '{', '}', ':', ';']
                looks_like_code = any(indicator in stripped for indicator in code_indicators)
                
                # CRITICAL: # comments MUST be wrapped in code blocks to prevent markdown header interpretation
                # If we see a # comment, it's likely code (unless it's clearly markdown like ##)
                if stripped.strip().startswith('#') and not stripped.strip().startswith('##'):
                    # This is likely a code comment - treat it as code
                    # Check if it's part of a code block by looking at context
                    has_nearby_code = False
                    # Look at previous lines for code context (check up to 5 lines back)
                    for check_idx in range(max(0, i-5), i):
                        if check_idx < len(lines):
                            check_line = lines[check_idx]
                            # Check if previous line has code indicators or is also a comment
                            if (any(ind in check_line for ind in ['def ', 'class ', 'import ', 'from ', 'return ', '=', '(', ')', '[', ']', '    #', 'if ', 'for ', 'while ']) or
                                (check_line.strip().startswith('#') and not check_line.strip().startswith('##') and len(check_line.strip()) > 2)):
                                has_nearby_code = True
                                break
                    # Also check next few lines
                    if not has_nearby_code:
                        for check_idx in range(i+1, min(len(lines), i+4)):
                            check_line = lines[check_idx]
                            if any(ind in check_line for ind in ['def ', 'class ', 'import ', 'from ', 'return ', '=', '(', ')', '[', ']', '    #', 'if ', 'for ', 'while ']):
                                has_nearby_code = True
                                break
                    
                    # If it's a # comment, treat it as code (needs to be in code block)
                    # This prevents markdown from interpreting # as a header
                    # Be more aggressive - if it looks like a code comment (has text after #), wrap it
                    if has_nearby_code or (stripped.strip().startswith('# ') and len(stripped.strip()) > 2):
                        looks_like_code = True
                
                # Don't treat Terraform/HCL as Python code - it has different syntax
                # Terraform uses resource blocks, variables, etc. which shouldn't be wrapped in ```python
                is_terraform = any(keyword in stripped for keyword in ['resource "', 'variable "', 'output "', 
                                                                       'data "', 'provider "', 'module "',
                                                                       'terraform {', 'backend "'])
                
                if looks_like_code and not is_terraform:
                    # Collect consecutive indented code lines
                    # IMPORTANT: Include # comments and """ docstrings - they need to be in code blocks
                    code_lines = [stripped]
                    j = i + 1
                    
                    while j < len(lines):
                        # Check if we hit a code fence - if so, stop collecting
                        if '```' in lines[j]:
                            break
                        if lines[j].strip() == '':
                            # Empty line - include if followed by more code
                            if j + 1 < len(lines) and lines[j + 1].startswith('    '):
                                code_lines.append('')
                                j += 1
                            else:
                                break
                        elif lines[j].startswith('    '):
                            # More indented code - include it
                            next_stripped = lines[j][4:]
                            # Check if it's also code (not Terraform)
                            next_is_terraform = any(keyword in next_stripped for keyword in ['resource "', 'variable "', 'output "'])
                            if next_is_terraform:
                                break
                            code_lines.append(next_stripped)
                            j += 1
                        elif lines[j].strip().startswith('#') and not lines[j].strip().startswith('##'):
                            # # comment that's not indented but is part of code block
                            # Include it in the code block
                            code_lines.append(lines[j].strip())
                            j += 1
                        else:
                            # Not code - stop collecting
                            break
                    
                    # Wrap in code fence if we have code
                    if len(code_lines) > 0:
                        fixed_lines.append('```python')
                        fixed_lines.extend(code_lines)
                        fixed_lines.append('```')
                        i = j - 1  # Skip processed lines
                    else:
                        fixed_lines.append(stripped)
                else:
                    # Not code, just remove indentation
                    fixed_lines.append(stripped)
            else:
                fixed_lines.append(line)
            
            i += 1
        
        content = '\n'.join(fixed_lines)
    
    return content.strip()

def get_all_flashcard_files(flashcards_dir: Path) -> List[Path]:
    """Get all flashcard files, prioritizing the ordered list."""
    if not flashcards_dir.exists():
        print(f"Warning: Flashcards directory {flashcards_dir} not found")
        return []
    
    # Get files from the ordered list first
    ordered_files = []
    remaining_files = []
    
    for file_name in FLASHCARD_FILES:
        file_path = flashcards_dir / file_name
        if file_path.exists():
            ordered_files.append(file_path)
    
    # Get any remaining .md files not in the ordered list
    for file_path in flashcards_dir.glob("*.md"):
        if file_path not in ordered_files and file_path.name not in ["algorithm-flashcards-anki.md"]:
            remaining_files.append(file_path)
    
    return ordered_files + sorted(remaining_files)

def generate_complete_study_guide(docs_dir: Path, flashcards_dir: Path, output_file: Path) -> None:
    """Generate a complete study guide with all docs and flashcards."""
    print("Generating complete study guide...")
    print("=" * 60)
    
    content_parts = []
    
    # Add main title
    content_parts.append("# DevOps & Backend Study Guide - Complete Edition")
    content_parts.append("")
    content_parts.append("*A comprehensive study guide covering DevOps, Chaos Engineering, and Backend Development fundamentals*")
    content_parts.append("")
    content_parts.append("*Complete edition including all documentation and algorithm flashcards*")
    content_parts.append("")
    content_parts.append("*Generated for printing and offline study*")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")
    
    # Add table of contents
    content_parts.append("## Table of Contents")
    content_parts.append("")
    
    section_num = 1
    for section in DOCUMENT_STRUCTURE:
        content_parts.append(f"### {section_num}. {section['title']}")
        subsection_num = 1
        for file_name, section_title in section['sections']:
            content_parts.append(f"   {section_num}.{subsection_num} {section_title}")
            subsection_num += 1
        content_parts.append("")
        section_num += 1
    
    # Add flashcards section to TOC
    content_parts.append(f"### {section_num}. Algorithm Flashcards & Pattern Recognition")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")
    
    # Add content sections
    section_num = 1
    for section in DOCUMENT_STRUCTURE:
        content_parts.append(f"# {section_num}. {section['title']}")
        content_parts.append("")
        
        subsection_num = 1
        for file_name, section_title in section['sections']:
            file_path = docs_dir / file_name
            if file_path.exists():
                print(f"  Processing {file_name}...")
                # Clean each file individually first
                cleaned_content = clean_markdown_file(file_path, is_printable=True)
                
                if cleaned_content:
                    content_parts.append(f"## {section_num}.{subsection_num} {section_title}")
                    content_parts.append("")
                    content_parts.append(cleaned_content)
                    content_parts.append("")
                    content_parts.append("---")
                    content_parts.append("")
                    subsection_num += 1
            else:
                print(f"  Warning: {file_name} not found")
        
        section_num += 1
    
    # Add flashcards section
    content_parts.append(f"# {section_num}. Algorithm Flashcards & Pattern Recognition")
    content_parts.append("")
    content_parts.append("*This section contains algorithm pattern flashcards for quick reference and pattern recognition practice.*")
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")
    
    flashcard_files = get_all_flashcard_files(flashcards_dir)
    
    if flashcard_files:
        print(f"  Processing {len(flashcard_files)} flashcard files...")
        
        for i, flashcard_file in enumerate(flashcard_files, 1):
            print(f"    Processing {flashcard_file.name}...")
            # Clean each flashcard file individually first
            cleaned_content = clean_markdown_file(flashcard_file, is_printable=True)
            
            if cleaned_content:
                # Extract title from content or filename
                title_match = re.search(r'^#\s+(.+?)$', cleaned_content, re.MULTILINE)
                if title_match:
                    title = title_match.group(1).strip()
                else:
                    # Generate title from filename
                    title = flashcard_file.stem.replace('-', ' ').replace('_', ' ').title()
                
                content_parts.append(f"## {section_num}.{i} {title}")
                content_parts.append("")
                
                # Remove the title from content if it exists
                cleaned_content = re.sub(r'^#\s+.+?\n', '', cleaned_content, count=1, flags=re.MULTILINE)
                
                content_parts.append(cleaned_content)
                content_parts.append("")
                content_parts.append("---")
                content_parts.append("")
    else:
        print("  Warning: No flashcard files found")
        content_parts.append("*No flashcard files found in the flashcards directory.*")
        content_parts.append("")
    
    # Add footer
    content_parts.append("")
    content_parts.append("---")
    content_parts.append("")
    content_parts.append("# End of Study Guide")
    content_parts.append("")
    content_parts.append("*This complete study guide includes all documentation and algorithm flashcards.*")
    content_parts.append("*Generated for comprehensive offline study and interview preparation.*")
    content_parts.append("")
    
    # Write the combined file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_parts))
    
    # Get file stats
    file_size = output_file.stat().st_size
    line_count = len(content_parts)
    
    print("")
    print("=" * 60)
    print(f"✅ Complete study guide generated: {output_file}")
    print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")
    print(f"   Total sections: {section_num}")
    print(f"   Flashcard files included: {len(flashcard_files)}")
    print("")
    print("📖 This file is ready for printing or PDF conversion")

def main():
    """Main function to generate the complete study guide."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"
    flashcards_dir = project_root / "generated" / "flashcards"
    
    if not docs_dir.exists():
        print(f"Error: Docs directory not found at {docs_dir}")
        sys.exit(1)
    
    # Create output directory
    output_dir = project_root / "generated"
    output_dir.mkdir(exist_ok=True)
    
    # Generate complete study guide
    output_file = output_dir / "study-guide-complete-printable.md"
    
    generate_complete_study_guide(docs_dir, flashcards_dir, output_file)
    
    print("")
    print("Next steps:")
    print("1. Review the generated file: generated/study-guide-complete-printable.md")
    print("2. Convert to PDF if needed: pandoc generated/study-guide-complete-printable.md -o study-guide.pdf")
    print("3. Print or use for offline study")

if __name__ == "__main__":
    main()

