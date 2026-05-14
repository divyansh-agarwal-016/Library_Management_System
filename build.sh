#!/usr/bin/env bash
# Render build script
set -o errexit

pip install -r requirements.txt

# Create instance directory and seed the database
python seed.py
