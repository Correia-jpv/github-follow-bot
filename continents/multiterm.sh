#!/bin/bash

# Script to create tmux sessions for continents

# Define the continent names and respective commands
continents=("Africa" "America" "Asia" "Australia" "Europe")
commands=("africa.sh" "america.sh" "asia.sh" "australia.sh" "europe.sh")

# Loop through the continents and start a tmux session for each
for ((i=0; i<${#continents[@]}; i++)); do
  continent="${continents[$i]}"
  command="bash ${commands[$i]}"

  # Create tmux session and run the command
  tmux new-session -d -s "$continent" "$command"
  echo "Created session: $continent"

  # Optional: Attach to the session after creating
  
done
