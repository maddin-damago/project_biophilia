# 🌿 Team Git Workflow Guide

Welcome to the team! This guide covers the essential Git commands you will use daily to collaborate on **Project Biophilia** without stepping on each other's toes.

## Prerequisites

After installing git and before first pull or push, set up your username and email for git. This is NOT a login of any kind, it is what will be your signature for your git work.

```bash
# Set your global username
git config --global user.name "Your Name"

# Set your global email address
git config --global user.email "your.email@example.com"
```

To check your current settings

```bash
# View your current configuration values
git config --global --list
```

---

## 🚀 1. Every Morning (Get the Latest Code)

Before you start writing any new code, always pull the latest changes that your teammates merged.

```bash
# Switch to the main branch
git checkout main

# Get the newest updates from GitHub
git pull origin main
```

## 🛠️ 2. Starting a New Feature (Create a Branch)

Rule: Never write code directly on the main branch. Always create a personal "feature branch" for your specific task.

```bash

# Create and switch to a new branch

# Example: git checkout -b feature/weather-icons

git checkout -b feature/your-feature-name
```

## 💾 3. Saving Your Progress (Stage & Commit)

As you work throughout the day, save your progress locally. Think of a commit like a video game save point.

```bash

# Check what files you have modified or created
git status

# Stage ALL your changes to be saved
git add .

# Save the changes with a clear, descriptive message
# Example: git commit -m "feat: fetch current temperature from open-meteo"
git commit -m "feat: short description of what you did"
```

## 📤 4. Sharing with the Team (Push & Pull Request)

When your feature is done, working, and ready to be added to the project, send it to GitHub.

```bash
# Push your local branch up to GitHub
git push origin feature/your-feature-name
```

Next Step: Go to our GitHub repository webpage. You will see a yellow banner asking you to "Compare & pull request". Click it, add a short description, and submit it for review!

## 🚨 5. Emergency / Oops Commands

Did something go wrong? Don't panic.

I messed up my local code and want to completely reset to the last save point:

```bash
# WARNING: This deletes all uncommitted changes in your current files!
git reset --hard HEAD
```

I committed, but realized I made a typo in my commit message:

```bash
git commit --amend -m "your new corrected message"
```

I am on the wrong branch and want to see all available branches:

```bash
git branch -a
```
