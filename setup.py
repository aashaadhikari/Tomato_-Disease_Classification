#!/usr/bin/env python3
"""
TomatoHealth Setup Script
Automates the initial setup and configuration of the application
"""

import os
import sys
import subprocess
import secrets
from pathlib import Path

def run_command(command):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command: {command}")
        print(f"Error: {e}")
        return False

def create_env_file():
    """Create .env file with default values"""
    env_path = Path('.env')
    if env_path.exists():
        print("✓ .env file already exists")
        return True
    
    try:
        secret_key = secrets.token_hex(32)
        env_content = f"""# Flask Configuration
SECRET_KEY={secret_key}
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=sqlite:///tomato_disease.db

# File Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=5242880

# Security
WTF_CSRF_ENABLED=True
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✓ Created .env file with secure configuration")
        return True
    except Exception as e:
        print(f"✗ Failed to create .env file: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/uploads',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✓ Created necessary directories")
    return True

def check_model_file():
    """Check if the model file exists"""
    model_path = Path('Plant_Disease_Prediction/tomato_disease_model.tflite')
    if model_path.exists():
        print("✓ TensorFlow Lite model found")
        return True
    else:
        print("⚠ Warning: Model file not found at Plant_Disease_Prediction/tomato_disease_model.tflite")
        print("  Please ensure the model file is in the correct location")
        return False

def install_requirements():
    """Install Python requirements"""
    print("Installing Python dependencies...")
    if run_command(f"{sys.executable} -m pip install -r requirements.txt"):
        print("✓ Python dependencies installed successfully")
        return True
    else:
        print("✗ Failed to install Python dependencies")
        return False

def initialize_database():
    """Initialize the database"""
    print("Initializing database...")
    command = f'{sys.executable} -c "from app import app, db; app.app_context().push(); db.create_all(); print(\'Database initialized successfully\')"'
    if run_command(command):
        print("✓ Database initialized successfully")
        return True
    else:
        print("✗ Failed to initialize database")
        return False

def main():
    """Main setup function"""
    print("🍅 TomatoHealth Setup Script")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 9):
        print("✗ Python 3.9 or higher is required")
        sys.exit(1)
    
    print(f"✓ Python version: {sys.version}")
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Check model file
    check_model_file()
    
    # Install requirements
    if not install_requirements():
        print("\nSetup failed. Please check the errors above.")
        sys.exit(1)
    
    # Initialize database
    if not initialize_database():
        print("\nDatabase initialization failed. You can try running it manually:")
        print('python -c "from app import app, db; app.app_context().push(); db.create_all()"')
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run the application: python app.py")
    print("2. Open your browser and go to: http://localhost:5000")
    print("3. Register a new account and start using TomatoHealth!")
    print("\nFor deployment instructions, check the README.md file.")

if __name__ == "__main__":
    main()