#!/usr/bin/env python3
"""
Fix Japanese documentation paths and links
"""
import os
import re
import glob

def fix_markdown_file(filepath):
    """Fix paths in a single markdown file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix image paths - change relative paths to absolute
        # ../../../static/img/ -> /img/
        content = re.sub(r'\.\./.*?/static/img/', '/img/', content)
        
        # Fix internal doc links that use the old structure
        # ../../../docs/ -> ../
        content = re.sub(r'\.\./.*?/docs/', '../', content)
        
        # Fix absolute doc links 
        # (/docs/ -> (/
        content = re.sub(r'\(/docs/', '(/', content)
        
        # Fix links to static images in markdown
        # ![something](../static/img/file.ext) -> ![something](/img/file.ext)
        content = re.sub(r'\!\[([^\]]*)\]\(\.\./.*?/static/img/([^)]+)\)', r'![\1](/img/\2)', content)
        
        # Write back if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main function"""
    base_path = "i18n/ja/docusaurus-plugin-content-docs/current"
    
    if not os.path.exists(base_path):
        print(f"Directory {base_path} not found")
        return
    
    # Find all markdown files
    md_files = glob.glob(f"{base_path}/**/*.md", recursive=True)
    
    print(f"Found {len(md_files)} markdown files to process")
    
    fixed_count = 0
    for filepath in md_files:
        if fix_markdown_file(filepath):
            fixed_count += 1
    
    print(f"Fixed {fixed_count} files")

if __name__ == "__main__":
    main()