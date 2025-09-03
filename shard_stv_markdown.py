#!/usr/bin/env python3
"""
Script to shard a large markdown file by level 1 headings.
Specifically designed for the STV markdown file.
"""

import os
import re
from pathlib import Path


def sanitize_filename(heading):
    """Convert heading to a valid filename."""
    # Remove # and extra spaces
    heading = heading.strip('#').strip()
    
    # Convert to lowercase and replace spaces with underscores
    filename = heading.lower().replace(' ', '_')
    
    # Remove or replace problematic characters
    filename = re.sub(r'[^\w\-_]', '', filename)
    
    # Handle duplicates and special cases
    filename_map = {
        'stv_annual_report_and_accounts_2024': 'stv_annual_report_2024',
        'esg_report': 'esg_report_main',
        'directors_report_ownership': 'directors_report_ownership'
    }
    
    if filename in filename_map:
        filename = filename_map[filename]
    
    # Add prefix and extension
    return f"stv_{filename}.md"


def shard_markdown_file(input_file, output_dir):
    """
    Shard a markdown file by level 1 headings.
    
    Args:
        input_file: Path to the input markdown file
        output_dir: Directory where output files will be saved
    """
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines in file: {len(lines)}")
    
    # Find all level 1 headings and their positions
    headings = []
    for i, line in enumerate(lines):
        if line.startswith('# ') and not line.startswith('## '):
            headings.append({
                'line_num': i + 1,  # 1-indexed for human readability
                'index': i,         # 0-indexed for array access
                'heading': line.strip(),
                'filename': sanitize_filename(line)
            })
    
    print(f"\nFound {len(headings)} level 1 headings:")
    for h in headings:
        print(f"  Line {h['line_num']:4d}: {h['heading']}")
    
    # Process each section
    files_created = []
    
    for i, heading_info in enumerate(headings):
        start_idx = heading_info['index']
        
        # Determine end index (start of next section or end of file)
        if i < len(headings) - 1:
            end_idx = headings[i + 1]['index']
        else:
            end_idx = len(lines)
        
        # Extract content for this section
        section_content = ''.join(lines[start_idx:end_idx])
        
        # Create output file
        output_file = os.path.join(output_dir, heading_info['filename'])
        
        # Write content to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(section_content)
        
        files_created.append({
            'filename': heading_info['filename'],
            'lines': f"{start_idx + 1}-{end_idx}",
            'size': len(section_content)
        })
        
        print(f"Created: {heading_info['filename']} (lines {start_idx + 1}-{end_idx}, {len(section_content)} chars)")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY: Successfully sharded {input_file}")
    print(f"Created {len(files_created)} files in {output_dir}")
    print(f"{'='*60}")
    
    # List all created files with details
    print("\nFiles created:")
    for file_info in files_created:
        print(f"  - {file_info['filename']:50s} Lines: {file_info['lines']:12s} Size: {file_info['size']:,} chars")
    
    return files_created


def main():
    """Main function to run the sharding process."""
    
    # Configuration
    input_file = '/Users/Chris/Desktop/insig/demo/insig_analyst_demo/data/STV/stv.md'
    output_dir = '/Users/Chris/Desktop/insig/demo/insig_analyst_demo/data/STV'
    
    print(f"Sharding markdown file by level 1 headings")
    print(f"Input:  {input_file}")
    print(f"Output: {output_dir}")
    print(f"{'='*60}")
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"ERROR: Input file not found: {input_file}")
        return 1
    
    # Get file size
    file_size = os.path.getsize(input_file)
    print(f"Input file size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    try:
        # Perform the sharding
        files = shard_markdown_file(input_file, output_dir)
        print(f"\nSharding completed successfully!")
        return 0
        
    except Exception as e:
        print(f"\nERROR during sharding: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())