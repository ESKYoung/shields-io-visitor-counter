#!/bin/sh

# Create a .bashrc file
touch ~/.bashrc;

# Add direnv hooks
echo 'eval "$(direnv hook bash)"' > ~/.bashrc;

# Print the Python version
echo $(python3 --version)
