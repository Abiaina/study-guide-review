#!/usr/bin/env python3
"""
Generate combined versions of the study guide:
1. Printable version - single markdown file with all content
2. GitHub Pages version - optimized for web viewing
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
            ("algo.md", "Algorithms & Data Structures"),
            ("Core_Data_Structures.md", "Core Data Structures"),
            ("graphs_linked_lists.md", "Complex Data Structures"),
            ("search.md", "Searching & Sorting"),
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
            ("cheat_sheet.md", "Cheat Sheet"),
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
        "title": "Security & Performance",
        "sections": [
            ("security_compliance.md", "Security & Compliance"),
        ]
    }
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

def clean_markdown_content(content: str, is_printable: bool = True) -> str:
    """Clean and format markdown content for the target format."""
    if not content:
        return ""
    
    # Remove front matter
    content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
    
    # Remove title from content (we'll add our own)
    content = re.sub(r'^#\s+.*?\n', '', content, count=1)
    
    if is_printable:
        # For printable version, keep everything as-is
        return content.strip()
    else:
        # For GitHub Pages, add navigation and optimize for web
        return content.strip()

def generate_printable_version(docs_dir: Path, output_file: Path) -> None:
    """Generate a single printable markdown file."""
    print("Generating printable version...")
    
    content_parts = []
    
    # Add main title
    content_parts.append("# DevOps & Backend Study Guide - Complete Edition\n")
    content_parts.append("*A comprehensive study guide covering DevOps, Chaos Engineering, and Backend Development fundamentals*\n")
    content_parts.append("*Generated for printing and offline study*\n")
    content_parts.append("---\n")
    
    # Add table of contents
    content_parts.append("## Table of Contents\n")
    for section in DOCUMENT_STRUCTURE:
        content_parts.append(f"### {section['title']}\n")
        for file_name, section_title in section['sections']:
            content_parts.append(f"- {section_title}\n")
        content_parts.append("")
    
    content_parts.append("---\n")
    
    # Add content sections
    for section in DOCUMENT_STRUCTURE:
        content_parts.append(f"# {section['title']}\n")
        
        for file_name, section_title in section['sections']:
            file_path = docs_dir / file_name
            if file_path.exists():
                print(f"  Processing {file_name}...")
                content = read_markdown_file(file_path)
                cleaned_content = clean_markdown_content(content, is_printable=True)
                
                if cleaned_content:
                    content_parts.append(f"## {section_title}\n")
                    content_parts.append(cleaned_content)
                    content_parts.append("\n---\n")
            else:
                print(f"  Warning: {file_name} not found")
    
    # Write the combined file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_parts))
    
    print(f"Printable version generated: {output_file}")

def generate_github_pages_version(docs_dir: Path, output_file: Path) -> None:
    """Generate a GitHub Pages optimized version."""
    print("Generating GitHub Pages version...")
    
    content_parts = []
    
    # Add main title and navigation
    content_parts.append("---")
    content_parts.append("title: Complete Study Guide")
    content_parts.append("layout: default")
    content_parts.append("---")
    content_parts.append("")
    content_parts.append("# DevOps & Backend Study Guide - Complete Edition\n")
    content_parts.append("*A comprehensive study guide covering DevOps, Chaos Engineering, and Backend Development fundamentals*\n")
    content_parts.append("*[View individual sections](/) for better navigation*\n")
    content_parts.append("---\n")
    
    # Add navigation
    content_parts.append("## Quick Navigation\n")
    for section in DOCUMENT_STRUCTURE:
        content_parts.append(f"### {section['title']}\n")
        for file_name, section_title in section['sections']:
            # Create anchor links
            anchor = re.sub(r'[^a-zA-Z0-9\s]', '', section_title).lower().replace(' ', '-')
            content_parts.append(f"- [{section_title}](#{anchor})\n")
        content_parts.append("")
    
    content_parts.append("---\n")
    
    # Add content sections with anchors
    for section in DOCUMENT_STRUCTURE:
        content_parts.append(f"# {section['title']}\n")
        
        for file_name, section_title in section['sections']:
            file_path = docs_dir / file_name
            if file_path.exists():
                print(f"  Processing {file_name}...")
                content = read_markdown_file(file_path)
                cleaned_content = clean_markdown_content(content, is_printable=False)
                
                if cleaned_content:
                    # Add anchor for navigation
                    anchor = re.sub(r'[^a-zA-Z0-9\s]', '', section_title).lower().replace(' ', '-')
                    content_parts.append(f"<a name='{anchor}'></a>")
                    content_parts.append(f"## {section_title}\n")
                    content_parts.append(cleaned_content)
                    content_parts.append("\n---\n")
            else:
                print(f"  Warning: {file_name} not found")
    
    # Add back to top links
    content_parts.append("## Navigation\n")
    content_parts.append("[↑ Back to Top](#devops--backend-study-guide---complete-edition)\n")
    content_parts.append("[← Back to Index](/)")
    
    # Write the combined file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content_parts))
    
    print(f"GitHub Pages version generated: {output_file}")

def main():
    """Main function to generate both versions."""
    # Get the project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    docs_dir = project_root / "docs"
    
    if not docs_dir.exists():
        print(f"Error: Docs directory not found at {docs_dir}")
        sys.exit(1)
    
    # Create output directory
    output_dir = project_root / "generated"
    output_dir.mkdir(exist_ok=True)
    
    # Generate both versions
    printable_file = output_dir / "study-guide-printable.md"
    github_pages_file = output_dir / "study-guide-complete.md"
    
    generate_printable_version(docs_dir, printable_file)
    generate_github_pages_version(docs_dir, github_pages_file)
    
    print("\n" + "="*50)
    print("Generation complete!")
    print(f"Printable version: {printable_file}")
    print(f"GitHub Pages version: {github_pages_file}")
    print("\nNext steps:")
    print("1. Review the generated files")
    print("2. Add the GitHub Pages version to your docs/ directory")
    print("3. Update navigation to include the complete version")
    print("4. Consider adding a print button to your website")

if __name__ == "__main__":
    main()
