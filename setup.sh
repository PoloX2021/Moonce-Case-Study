#!/bin/bash

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "Setup complete. Run 'source venv/bin/activate' to activate the environment."
