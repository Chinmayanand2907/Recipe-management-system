#!/bin/bash

# Recipe Management System - GitHub Push Script

echo "======================================================="
echo "  Recipe Management System - GitHub Setup Script"
echo "======================================================="
echo ""

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed."
    echo "Please install Git from https://git-scm.com/downloads"
    exit 1
fi

# Initialize Git repository if not already initialized
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
    echo "Git repository initialized."
else
    echo "Git repository already initialized."
fi

# Ask for GitHub repository details
echo ""
read -p "Enter your GitHub username: " github_username
read -p "Enter your repository name (e.g., recipe-management-system): " repo_name

# Check repository URL
repo_url="https://github.com/$github_username/$repo_name.git"
echo ""
echo "Repository URL: $repo_url"
read -p "Is this correct? (y/n): " confirm

if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Setup aborted. Please run the script again with correct information."
    exit 1
fi

# Check if files are ready
echo ""
echo "Running file check script..."
python check_files.py

# Ask for confirmation to continue
echo ""
read -p "Do you want to continue with pushing to GitHub? (y/n): " push_confirm

if [ "$push_confirm" != "y" ] && [ "$push_confirm" != "Y" ]; then
    echo "Push aborted. You can run this script again when ready."
    exit 1
fi

# Add remote repository
echo ""
echo "Adding remote repository..."
git remote remove origin 2>/dev/null
git remote add origin $repo_url
echo "Remote repository added."

# Add all files
echo ""
echo "Adding files to staging area..."
git add .
echo "Files added."

# Commit changes
echo ""
echo "Committing files..."
git commit -m "Initial commit: Recipe Management System"
echo "Files committed."

# Set the default branch name
default_branch=$(git branch --show-current)
if [ -z "$default_branch" ]; then
    default_branch="main"
fi

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
echo "Using branch: $default_branch"
git push -u origin $default_branch

# Check push status
if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================="
    echo "  Success! Your project is now on GitHub."
    echo "  Repository URL: $repo_url"
    echo "======================================================="
else
    echo ""
    echo "======================================================="
    echo "  Error pushing to GitHub."
    echo "  Please check your credentials and try again."
    echo "  If using a token, use it as your password when prompted."
    echo "======================================================="
fi 