#!/usr/bin/env python3
"""
Markdown File Metadata Generator

This script processes a fixed list of Markdown filenames and generates
structured JSON metadata for each file, including filename, category,
and GitHub raw URL.
"""

import json


def generate_metadata(filenames):
    """
    Generate metadata for each markdown file.
    
    Args:
        filenames (list): List of markdown filenames
        
    Returns:
        list: List of dictionaries containing metadata for each file
    """
    metadata = []
    base_url = "https://raw.githubusercontent.com/fmhy/edit/refs/heads/main/docs/"
    
    for filename in filenames:
        # Extract category by removing .md extension and replacing dashes with spaces
        category = filename.replace('.md', '').replace('-', ' ')
        
        # Construct the raw GitHub URL
        raw_url = base_url + filename
        
        # Create metadata object
        file_metadata = {
            "filename": filename,
            "category": category,
            "raw_url": raw_url
        }
        
        metadata.append(file_metadata)
    
    return metadata


def main():
    """
    Main function to process markdown files and generate JSON output.
    """
    # Fixed list of markdown filenames
    markdown_files = [
        "adblockvpnguide.md",
        "ai.md",
        "android-iosguide.md",
        "audiopiracyguide.md",
        "beginners-guide.md",
        "devtools.md",
        "downloadpiracyguide.md",
        "edupiracyguide.md",
        "feedback.md",
        "file-tools.md",
        "gaming-tools.md",
        "gamingpiracyguide.md",
        "img-tools.md",
        "index.md",
        "internet-tools.md",
        "linuxguide.md",
        "miscguide.md",
        "non-english.md",
        "posts.md",
        "readingpiracyguide.md",
        "sandbox.md",
        "social-media-tools.md",
        "startpage.md",
        "storage.md",
        "system-tools.md",
        "text-tools.md",
        "torrentpiracyguide.md",
        "unsafesites.md",
        "video-tools.md",
        "videopiracyguide.md"
    ]
    
    print(f"Processing {len(markdown_files)} markdown files...")
    
    # Generate metadata for all files
    metadata_list = generate_metadata(markdown_files)
    
    # Write to JSON file
    try:
        with open('output.json', 'w', encoding='utf-8') as f:
            json.dump(metadata_list, f, indent=2, ensure_ascii=False)
        
        print(f"Successfully generated metadata for {len(metadata_list)} files.")
        print("Output saved to: output.json")
        
    except IOError as e:
        print(f"Error writing to output.json: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
