#!/bin/bash

# This script runs the 'poetry env info' command to display information about the Poetry environment.

# running script from file
poetry run python scripts/get_sys_info.py
# Running the 'poetry env info' command
poetry env info

