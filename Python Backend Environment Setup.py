"""
---------------------------------------------------------
FinRelief AI
Story 1: Python Backend Environment Setup
---------------------------------------------------------
Author : Your Name
Description:
    This script automates the backend environment setup
    for the FinRelief AI project.
---------------------------------------------------------
"""

import os
import sys
import subprocess
from pathlib import Path

PROJECT_NAME = "FinReliefAI"

BACKEND_STRUCTURE = [
    "backend",
    "backend/app",
    "backend/app/api",
    "backend/app/models",
    "backend/app/services",
    "backend/app/utils",
    "backend/app/database",
    "backend/app/schemas",
    "backend/app/core",
    "backend/tests"
]


def check_python_version():
    """Verify Python version."""
    print("Checking Python Version...")

    if sys.version_info < (3, 10):
        print("Python 3.10 or higher is required.")
        sys.exit()

    print(f"Python Version: {sys.version.split()[0]}\n")


def create_virtual_environment():
    """Create virtual environment."""

    print("Creating Virtual Environment...")

    if not os.path.exists("venv"):
        subprocess.run([sys.executable, "-m", "venv", "venv"])
        print("Virtual Environment Created.\n")
    else:
        print("Virtual Environment Already Exists.\n")


def install_requirements():
    """Install dependencies."""

    print("Installing Requirements...")

    if os.path.exists("requirements.txt"):
        pip = "venv/Scripts/pip" if os.name == "nt" else "venv/bin/pip"

        subprocess.run([pip, "install", "-r", "requirements.txt"])

        print("Dependencies Installed.\n")
    else:
        print("requirements.txt not found.\n")


def create_project_structure():
    """Create backend folders."""

    print("Creating Backend Structure...")

    for folder in BACKEND_STRUCTURE:
        Path(folder).mkdir(parents=True, exist_ok=True)

    print("Folders Created.\n")


def create_init_files():
    """Create __init__.py files."""

    print("Creating __init__.py files...")

    directories = [
        "backend/app",
        "backend/app/api",
        "backend/app/models",
        "backend/app/services",
        "backend/app/utils",
        "backend/app/database",
        "backend/app/schemas",
        "backend/app/core"
    ]

    for directory in directories:
        init_file = os.path.join(directory, "__init__.py")

        if not os.path.exists(init_file):
            open(init_file, "w").close()

    print("__init__.py Files Created.\n")


def create_main_file():
    """Create FastAPI entry point."""

    print("Creating main.py...")

    content = '''from fastapi import FastAPI

app = FastAPI(
    title="FinRelief AI API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to FinRelief AI Backend"
    }
'''

    filepath = "backend/app/main.py"

    with open(filepath, "w") as file:
        file.write(content)

    print("main.py Created.\n")


def create_env_file():

    env_content = """# Environment Variables

DATABASE_URL=

SECRET_KEY=

OPENAI_API_KEY=

JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
"""

    with open(".env", "w") as file:
        file.write(env_content)

    print(".env File Created.\n")


def create_gitignore():

    gitignore = """
venv/
__pycache__/
.env
*.pyc
.idea/
.vscode/
"""

    with open(".gitignore", "w") as file:
        file.write(gitignore)

    print(".gitignore Created.\n")


def main():

    print("=" * 60)
    print("FinRelief AI Backend Environment Setup")
    print("=" * 60)

    check_python_version()

    create_virtual_environment()

    install_requirements()

    create_project_structure()

    create_init_files()

    create_main_file()

    create_env_file()

    create_gitignore()

    print("=" * 60)
    print("Backend Environment Setup Completed Successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()