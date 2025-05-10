@echo off
echo ======================================================
echo   Recipe Management System - GitHub Setup Script
echo ======================================================
echo.

REM Check if Git is installed
where git >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Error: Git is not installed.
    echo Please install Git from https://git-scm.com/downloads
    pause
    exit /b 1
)

REM Initialize Git repository if not already initialized
if not exist .git\ (
    echo Initializing Git repository...
    git init
    echo Git repository initialized.
) else (
    echo Git repository already initialized.
)

REM Ask for GitHub repository details
echo.
set /p github_username=Enter your GitHub username: 
set /p repo_name=Enter your repository name (e.g., recipe-management-system): 

REM Check repository URL
set repo_url=https://github.com/%github_username%/%repo_name%.git
echo.
echo Repository URL: %repo_url%
set /p confirm=Is this correct? (y/n): 

if /i not "%confirm%"=="y" (
    echo Setup aborted. Please run the script again with correct information.
    pause
    exit /b 1
)

REM Check if files are ready
echo.
echo Running file check script...
python check_files.py

REM Ask for confirmation to continue
echo.
set /p push_confirm=Do you want to continue with pushing to GitHub? (y/n): 

if /i not "%push_confirm%"=="y" (
    echo Push aborted. You can run this script again when ready.
    pause
    exit /b 1
)

REM Add remote repository
echo.
echo Adding remote repository...
git remote remove origin 2>nul
git remote add origin %repo_url%
echo Remote repository added.

REM Add all files
echo.
echo Adding files to staging area...
git add .
echo Files added.

REM Commit changes
echo.
echo Committing files...
git commit -m "Initial commit: Recipe Management System"
echo Files committed.

REM Get the default branch name
for /f "tokens=*" %%a in ('git branch --show-current') do set default_branch=%%a
if "%default_branch%"=="" (
    set default_branch=main
)

REM Push to GitHub
echo.
echo Pushing to GitHub...
echo Using branch: %default_branch%
git push -u origin %default_branch%

REM Check push status
if %ERRORLEVEL% equ 0 (
    echo.
    echo =======================================================
    echo   Success! Your project is now on GitHub.
    echo   Repository URL: %repo_url%
    echo =======================================================
) else (
    echo.
    echo =======================================================
    echo   Error pushing to GitHub.
    echo   Please check your credentials and try again.
    echo   If using a token, use it as your password when prompted.
    echo =======================================================
)

pause 