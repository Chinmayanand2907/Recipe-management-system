# GitHub Setup Instructions

This guide will help you push your Recipe Management System project to GitHub.

## Prerequisites

1. Create a GitHub account if you don't have one: [GitHub Sign Up](https://github.com/signup)
2. Install Git on your computer: [Git Downloads](https://git-scm.com/downloads)

## Steps to Push Your Project to GitHub

### 1. Create a New Repository on GitHub

1. Log in to your GitHub account
2. Click on the "+" icon in the top right corner and select "New repository"
3. Name your repository (e.g., "recipe-management-system")
4. Add a description (optional): "A web application for managing and sharing recipes, built with Flask and MySQL"
5. Keep it as a Public repository (or choose Private if you prefer)
6. Do NOT initialize the repository with a README, .gitignore, or license file (we already have these)
7. Click "Create repository"

### 2. Initialize Git in Your Local Project

Open your terminal/command prompt in your project directory and run:

```bash
# Initialize Git repository
git init

# Add all files to the staging area
git add .

# Commit the files
git commit -m "Initial commit: Recipe Management System"
```

### 3. Link Your Local Repository to GitHub

GitHub will show you the commands after creating the repository. They will look similar to:

```bash
# Add the remote repository
git remote add origin https://github.com/your-username/recipe-management-system.git

# Push your code to GitHub
git push -u origin main
```

Note: If you're using an older version of Git, you might need to use `master` instead of `main`:

```bash
git push -u origin master
```

### 4. Verify Your Upload

1. Go to your GitHub repository page
2. Refresh the page, and you should see all your project files

## Common Issues and Solutions

### Authentication Issues

If you encounter authentication issues, you may need to use a personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens → Generate new token
2. Give it a name, set an expiration, and select the "repo" scope
3. Generate the token and copy it
4. Use it as your password when Git asks for credentials

### Large Files

If you have large files that exceed GitHub's file size limit:

1. Add them to `.gitignore`
2. Consider using Git LFS (Large File Storage) for large files

### Line Endings

If you see many changes related to line endings:

```bash
# Configure Git to handle line endings appropriately
git config --global core.autocrlf input  # For macOS/Linux
git config --global core.autocrlf true   # For Windows
```

## Future Updates

To update your GitHub repository after making changes:

```bash
# Check which files have been modified
git status

# Add the changes
git add .

# Commit the changes with a descriptive message
git commit -m "Description of your changes"

# Push the changes to GitHub
git push
```

## Setting Up GitHub Pages (Optional)

If you want to showcase your project documentation:

1. Go to your repository settings
2. Scroll down to the "GitHub Pages" section
3. Select the branch to deploy (usually main)
4. Choose the /docs folder as the source if you've created documentation

---

Congratulations! Your Recipe Management System is now on GitHub! 