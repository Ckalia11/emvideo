#!/bin/bash

# Check if current directory or any parent directories are Git repositories
while [[ ! -d .git && $PWD != '/' ]]; do
    cd ..
done

if [[ $PWD == '/' ]]; then
    echo "No Git repository found."
    exit 1
fi

# Check if there are any changes to commit
if [[ -n $(git status -s) ]]; then

    # Get the current branch name
    branch=$(git rev-parse --abbrev-ref HEAD)

    # Create upstream branch if doesn't exist
    git push -u origin $branch

    # Add all changes
    git add .

    # Default commit message
    commit_message="WIP"

    if [ "$1" ]; then
        commit_message=$1        
    fi

    # Commit with a default message or you can customize it
    git commit -m "$commit_message"

    # Push to the remote repository
    git push
else
    echo "No changes to commit."
fi
