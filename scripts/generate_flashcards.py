#!/usr/bin/env python3
"""
Generate algorithm flashcards from the study guide content.
Creates individual flashcard files for different algorithm patterns.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

# Flashcard templates for different formats
ANKI_TEMPLATE = """# Algorithm Flashcards - {pattern_name}

## Card {card_number}: {problem_type}

**Front:**
{front_content}

**Back:**
{back_content}

---

"""

CSV_TEMPLATE = """front,back
"{front_content}","{back_content}"
"""

# Algorithm patterns to extract
ALGORITHM_PATTERNS = [
    {
        "name": "Two Pointers",
        "keywords": ["two pointers", "sum to target", "palindrome", "merge sorted"],
        "examples": ["Two Sum in sorted array", "Remove duplicates", "Valid palindrome"]
    },
    {
        "name": "Sliding Window", 
        "keywords": ["sliding window", "longest substring", "subarray", "anagrams"],
        "examples": ["Longest substring without repeating", "Minimum window substring"]
    },
    {
        "name": "Binary Search",
        "keywords": ["binary search", "sorted array", "find element", "capacity"],
        "examples": ["Find minimum capacity", "Search in rotated array"]
    },
    {
        "name": "Tree Traversal",
        "keywords": ["tree traversal", "binary search tree", "inorder", "level order"],
        "examples": ["Validate BST", "Level order traversal"]
    },
    {
        "name": "Graph Traversal",
        "keywords": ["graph", "shortest path", "cycle detection", "topological sort"],
        "examples": ["Detect cycle", "Shortest path", "Number of islands"]
    },
    {
        "name": "Dynamic Programming",
        "keywords": ["dynamic programming", "maximum", "minimum", "coin change"],
        "examples": ["Coin change", "Longest increasing subsequence"]
    },
    {
        "name": "Heap",
        "keywords": ["heap", "k-th", "priority queue", "median"],
        "examples": ["K-th largest element", "Merge k sorted lists"]
    },
    {
        "name": "Backtracking",
        "keywords": ["backtracking", "permutations", "combinations", "n-queens"],
        "examples": ["Generate permutations", "N-queens problem"]
    }
]

def extract_algorithm_content(algo_file: Path) -> Dict[str, str]:
    """Extract algorithm pattern content from the algo.md file."""
    content = algo_file.read_text(encoding='utf-8')
    
    # Find the Algorithm Problem Identification Guide section
    guide_start = content.find("## Algorithm Problem Identification Guide")
    if guide_start == -1:
        print("Warning: Algorithm Problem Identification Guide section not found")
        return {}
    
    # Extract content from the guide section
    guide_content = content[guide_start:]
    
    # Split into sections based on pattern headers
    sections = {}
    current_section = ""
    current_content = []
    
    lines = guide_content.split('\n')
    for line in lines:
        if line.startswith("#### **") and "Pattern" in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = line.strip()
            current_content = []
        elif current_section:
            current_content.append(line)
    
    # Add the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

def create_flashcard_content(pattern_name: str, section_content: str) -> List[Dict[str, str]]:
    """Create flashcard content for a specific algorithm pattern."""
    flashcards = []
    
    # Extract key indicators
    indicators_match = re.search(r'\*\*Key indicators\*\*:(.*?)(?=\*\*Examples\*\*:|$)', 
                                section_content, re.DOTALL)
    if indicators_match:
        indicators = indicators_match.group(1).strip()
        indicator_list = [item.strip() for item in indicators.split('-') if item.strip()]
        
        # Create flashcard for key indicators
        flashcards.append({
            "front": f"Identify the algorithm pattern for: {pattern_name}",
            "back": f"Key indicators:\n" + '\n'.join([f"• {indicator}" for indicator in indicator_list])
        })
    
    # Extract examples
    examples_match = re.search(r'\*\*Examples\*\*:(.*?)(?=```|$)', 
                              section_content, re.DOTALL)
    if examples_match:
        examples = examples_match.group(1).strip()
        example_list = [item.strip() for item in examples.split('-') if item.strip()]
        
        # Create flashcard for examples
        flashcards.append({
            "front": f"Give examples of {pattern_name} problems",
            "back": f"Common examples:\n" + '\n'.join([f"• {example}" for example in example_list])
        })
    
    # Extract code examples
    code_blocks = re.findall(r'```python\n(.*?)\n```', section_content, re.DOTALL)
    if code_blocks:
        for i, code in enumerate(code_blocks[:2]):  # Limit to first 2 code examples
            # Extract function name
            func_match = re.search(r'def (\w+)', code)
            if func_match:
                func_name = func_match.group(1)
                flashcards.append({
                    "front": f"Implement {func_name} using {pattern_name}",
                    "back": f"```python\n{code}\n```"
                })
    
    # Create complexity flashcard
    complexity_info = {
        "Two Pointers": "O(n) time, O(1) space",
        "Sliding Window": "O(n) time, O(k) space",
        "Binary Search": "O(log n) time, O(1) space", 
        "Tree Traversal": "O(n) time, O(h) space",
        "Graph Traversal": "O(V + E) time, O(V) space",
        "Dynamic Programming": "Varies by problem",
        "Heap": "O(n log k) time, O(k) space",
        "Backtracking": "O(n!) time, O(n) space"
    }
    
    flashcards.append({
        "front": f"What is the time/space complexity of {pattern_name}?",
        "back": complexity_info.get(pattern_name, "Varies by implementation")
    })
    
    return flashcards

def generate_flashcard_files(sections: Dict[str, str], output_dir: Path):
    """Generate flashcard files in different formats."""
    output_dir.mkdir(exist_ok=True)
    
    # Create Anki format file
    anki_content = []
    anki_content.append("# Algorithm Flashcards - Anki Format\n")
    anki_content.append("Generated for interview preparation\n\n")
    
    # Create CSV format for import
    csv_content = ["front,back"]
    
    card_number = 1
    
    for section_header, section_content in sections.items():
        # Extract pattern name
        pattern_match = re.search(r'\*\*(.*?)\*\*', section_header)
        if pattern_match:
            pattern_name = pattern_match.group(1)
            
            # Create flashcards for this pattern
            flashcards = create_flashcard_content(pattern_name, section_content)
            
            for flashcard in flashcards:
                # Add to Anki format
                anki_content.append(ANKI_TEMPLATE.format(
                    pattern_name=pattern_name,
                    card_number=card_number,
                    problem_type=flashcard["front"][:50] + "...",
                    front_content=flashcard["front"],
                    back_content=flashcard["back"]
                ))
                
                # Add to CSV format
                csv_content.append(f'"{flashcard["front"]}","{flashcard["back"]}"')
                
                card_number += 1
    
    # Write Anki format file
    anki_file = output_dir / "algorithm-flashcards-anki.md"
    anki_file.write_text('\n'.join(anki_content), encoding='utf-8')
    
    # Write CSV format file
    csv_file = output_dir / "algorithm-flashcards.csv"
    csv_file.write_text('\n'.join(csv_content), encoding='utf-8')
    
    # Create individual pattern files
    for section_header, section_content in sections.items():
        pattern_match = re.search(r'\*\*(.*?)\*\*', section_header)
        if pattern_match:
            pattern_name = pattern_match.group(1)
            pattern_file = output_dir / f"{pattern_name.lower().replace(' ', '-')}-flashcards.md"
            
            pattern_content = []
            pattern_content.append(f"# {pattern_name} Flashcards\n")
            pattern_content.append("Generated for interview preparation\n\n")
            
            flashcards = create_flashcard_content(pattern_name, section_content)
            for i, flashcard in enumerate(flashcards, 1):
                pattern_content.append(f"## Card {i}\n")
                pattern_content.append(f"**Front:** {flashcard['front']}\n")
                pattern_content.append(f"**Back:** {flashcard['back']}\n\n")
            
            pattern_file.write_text('\n'.join(pattern_content), encoding='utf-8')
    
    print(f"Generated {card_number - 1} flashcards in {output_dir}")

def main():
    """Main function to generate flashcards."""
    print("Generating Algorithm Flashcards...")
    
    # Paths
    docs_dir = Path("docs")
    output_dir = Path("generated/flashcards")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Read algorithm content
    algo_file = docs_dir / "algo.md"
    if not algo_file.exists():
        print(f"Error: {algo_file} not found")
        return
    
    # Extract algorithm sections
    sections = extract_algorithm_content(algo_file)
    
    if not sections:
        print("No algorithm sections found")
        return
    
    # Generate flashcard files
    generate_flashcard_files(sections, output_dir)
    
    print("Flashcard generation complete!")
    print(f"Files generated in: {output_dir}")

if __name__ == "__main__":
    main()
