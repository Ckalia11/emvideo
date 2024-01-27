#!/bin/bash

# Check if there are any changes to commit
if [[ -n $(git status -s) ]]; then
    # Get the current branch name
    branch=$(git rev-parse --abbrev-ref HEAD)
    echo "Current branch: $branch"
    # Add all changes
    git add .

    # Commit with a default message or you can customize it
    git commit -m "Auto commit"

    # Push to the remote repository
    git push
else
    echo "No changes to commit."
fi
