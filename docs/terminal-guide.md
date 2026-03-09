# Anteater Repository: Terminal Command & Organization Guide

This document summarizes the steps taken to organize the `~/bin` repository and provides a reference for useful generic terminal commands.

## GitHub Repository Link

**[https://github.com/jensonp/anteater](https://github.com/jensonp/anteater)**

---

## Log of Operations: How we organized ~/bin

To clean up the repository and separate personal career roadmaps from the shared code, the following sequence was executed:

1. **Reverted Accidental Push:**
   `git reset HEAD~1` (Undid the local commit that included roadmaps)
2. **Created Directory Structure:**
   `mkdir -p docs logs evaluations scripts config tests`
3. **Moved Private Files (Excluded from Git):**
   `mv Project-Evaluation*.md FAANG-L3-Roadmap.md evaluations/`
4. **Organized Code & Tests (Preserving Git History):**
   `git mv test*.py mini-test.py canvas_test/ tests/`
   `git mv commands.txt SSHMacToWindows.txt docs/`
5. **Staged Generic Content Only:**
   `git add mdc/generics/ mdc/L6-7/`
6. **Finalized & Force Pushed:**
   `git commit -m "Add MDC generic guidelines and architecture logic"`
   `git push --force` (Used to overwrite the remote history with the clean version)

---

## Useful Generic Terminal Commands

### 1. Navigation & Inspection

- `ls -lah`: List all files (including hidden ones) with sizes and permissions.
- `pwd`: Print Working Directory (where am I?).
- `du -sh *`: Check the disk usage of every folder in the current directory.
- `find . -name "*.py"`: Find every Python file in the current folder or subfolders.

### 2. File Manipulation

- `mkdir -p path/to/folder`: Create a folder and any missing parent folders.
- `cp -r source destination`: Copy a folder/file recursively.
- `mv old_name new_name`: Rename or move a file.
- `rm -rf folder_name`: Forcefully delete a folder (use with caution!).

### 3. Searching inside Files (The Power User Way)

- `grep -r "search_term" .`: Search for text inside every file in the current directory.
- `cat filename.txt | grep "specific_line"`: Filter a file's output for a specific word.

### 4. Git Mastery

- `git status`: Check what has changed and what is staged.
- `git log --oneline -n 5`: See the last 5 commits concisely.
- `git diff`: See exactly what lines you changed since your last commit.
- `git checkout -b new_feature`: Create and switch to a new branch for testing.

### 5. System & Network

- `top` or `htop`: See which processes are eating your CPU/RAM.
- `ssh user@ip_address`: Connect to a remote server.
- `tail -f logs/app.log`: Watch a log file update in real-time.
- `ps aux | grep python`: Find all running Python processes on the system.

---

## Log: Creating the Independent `mdc-rules` Repository

To create a strictly separate, public-facing repository for just the generic MDC rules:

1. **Create Remote Repository (via GH CLI):**
   `gh repo create mdc-rules --public --description "Generic MDC rules" --confirm`
2. **Setup Local Workspace:**
   `mkdir -p ~/Desktop/mdc-rules/generics ~/Desktop/mdc-rules/L6-7`
3. **Isolate Specific Files:**
   `cp ~/bin/mdc/generics/*.mdc ~/Desktop/mdc-rules/generics/`
   `cp ~/bin/mdc/L6-7/*.mdc ~/Desktop/mdc-rules/L6-7/`
4. **Push to New Main:**
   `git init`
   `git add .`
   `git commit -m "Initial commit"`
   `git remote add origin https://github.com/jensonp/mdc-rules.git`
   `git push -u origin main`
