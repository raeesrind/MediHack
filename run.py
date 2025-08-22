# run.py

import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.main import run_bot

if __name__ == "__main__":
    run_bot()
