#!/usr/bin/env python3
"""Setup script for the Telegram bot project."""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command: str, check: bool = True) -> bool:
    """Run a shell command."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        return False

def setup_environment():
    """Set up the development environment."""
    print("Setting up Telegram bot development environment...")
    
    # Check if virtual environment exists
    if not Path("venv").exists():
        print("Creating virtual environment...")
        if not run_command("python -m venv venv"):
            print("Failed to create virtual environment")
            return False
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    commands = [
        f"{activate_cmd} && pip install --upgrade pip",
        f"{activate_cmd} && pip install -r requirements.txt",
        f"{activate_cmd} && pip install -r requirements-dev.txt",
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"Failed to run: {cmd}")
            return False
    
    # Set up pre-commit hooks
    if not run_command(f"{activate_cmd} && pre-commit install"):
        print("Failed to install pre-commit hooks")
        return False
    
    # Create .env file from example if it doesn't exist
    if not Path(".env").exists():
        if Path(".env.example").exists():
            print("Creating .env file from .env.example...")
            if sys.platform == "win32":
                run_command("copy .env.example .env")
            else:
                run_command("cp .env.example .env")
            print("Please edit .env file with your configuration")
        else:
            print("Warning: .env.example not found")
    
    print("Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file with your bot token and database credentials")
    print("2. Run: python -m src.bot.main")
    print("3. For development: pre-commit run --all-files")
    
    return True

def setup_database():
    """Set up the database."""
    print("Setting up database...")
    
    # Check if alembic is available
    if not run_command("alembic --version", check=False):
        print("Alembic not found. Please install requirements first.")
        return False
    
    # Initialize alembic if needed
    if not Path("migrations/versions").exists():
        print("Initializing database migrations...")
        if not run_command("alembic init migrations"):
            print("Failed to initialize alembic")
            return False
    
    # Create initial migration
    if not run_command("alembic revision --autogenerate -m 'Initial migration'"):
        print("Failed to create initial migration")
        return False
    
    # Apply migrations
    if not run_command("alembic upgrade head"):
        print("Failed to apply migrations")
        return False
    
    print("Database setup completed successfully!")
    return True

def main():
    """Main setup function."""
    if len(sys.argv) > 1 and sys.argv[1] == "db":
        setup_database()
    else:
        setup_environment()

if __name__ == "__main__":
    main()