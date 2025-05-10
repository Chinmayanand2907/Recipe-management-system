#!/usr/bin/env python3
"""
Script to check if all required project files are present before pushing to GitHub.
"""

import os
import sys

REQUIRED_FILES = [
    # Core application files
    'mysql_app.py',
    'mysql_db.py',
    'forms.py',
    'setup_mysql.py',
    'fixed_schema.sql',
    'requirements.txt',
    'README.md',
    'LICENSE',
    '.gitignore',
    
    # Templates
    'templates/base.html',
    'templates/index.html',
    'templates/login.html',
    'templates/register.html',
    'templates/recipes.html',
    'templates/recipe_detail.html',
    'templates/recipe_form.html',
    'templates/ingredients.html',
    'templates/add_ingredient.html',
    'templates/404.html',
    
    # Static files
    'static/css/style.css',
]

REQUIRED_DIRS = [
    'templates',
    'static',
    'static/css',
    'static/uploads',
]

def check_files():
    """Check if all required files and directories exist."""
    missing_files = []
    missing_dirs = []
    
    print("Checking directories...")
    # Check directories
    for directory in REQUIRED_DIRS:
        if not os.path.isdir(directory):
            missing_dirs.append(directory)
            print(f"  Missing: {directory}")
        else:
            print(f"  Found: {directory}")
    
    print("\nChecking files...")
    # Check files
    for file_path in REQUIRED_FILES:
        if not os.path.isfile(file_path):
            missing_files.append(file_path)
            print(f"  Missing: {file_path}")
        else:
            print(f"  Found: {file_path}")
    
    return missing_files, missing_dirs

def main():
    """Main function."""
    print("=========================================")
    print("CHECKING FILES FOR GITHUB REPOSITORY")
    print("=========================================\n")
    
    missing_files, missing_dirs = check_files()
    
    print("\n=========================================")
    print("SUMMARY")
    print("=========================================")
    
    if missing_dirs:
        print("\n❌ Missing directories:")
        for directory in missing_dirs:
            print(f"  - {directory}")
            
    if missing_files:
        print("\n❌ Missing files:")
        for file_path in missing_files:
            print(f"  - {file_path}")
    
    if not missing_files and not missing_dirs:
        print("\n✅ All required files and directories are present!")
        print("   Your project is ready to be pushed to GitHub.")
        return 0
    else:
        print("\n⚠️ Please create the missing files and directories before pushing to GitHub.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 