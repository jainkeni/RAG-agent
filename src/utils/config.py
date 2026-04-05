# src/utils/config.py
import os
from dotenv import load_dotenv

# Get the root directory path
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent.parent  # Goes to project root

# Load .env file from root
env_path = ROOT_DIR / ".env"
print(f"Loading .env from: {env_path}")
load_dotenv(dotenv_path=env_path, override=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
HR_ORG_NAME = os.getenv("HR_ORG_NAME", "Your Company")
CURRENT_YEAR = os.getenv("CURRENT_YEAR", "2026")

# Verify keys are loaded
if not OPENAI_API_KEY:
    print("❌ WARNING: OPENAI_API_KEY not found in .env file!")
    print(f"   Expected .env at: {env_path}")
else:
    print(f"✅ OPENAI_API_KEY loaded successfully")