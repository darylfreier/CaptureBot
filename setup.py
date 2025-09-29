#!/usr/bin/env python3
"""
Setup script for CaptureBot.
Installs dependencies and creates initial configuration.
"""

import os
import sys
import subprocess
import yaml
from pathlib import Path


def install_dependencies():
    """Install required Python packages."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = ['screenshots', 'output', 'logs']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   Created: {directory}/")
    print("✅ Directories created")


def create_sample_config():
    """Create a sample configuration file."""
    print("⚙️  Creating sample configuration...")
    
    sample_config = {
        'WEB_DRIVER': {
            'browser': 'chrome',
            'headless': False,
            'window_size': [1920, 1080],
            'implicit_wait': 10
        },
        'SCREENSHOTS': {
            'format': 'png',
            'quality': 95,
            'full_page': True,
            'delay_after_action': 2
        },
        'PRESENTATION': {
            'title': 'User Flow Documentation',
            'author': 'CaptureBot',
            'slide_width': 9144000,
            'slide_height': 6858000
        },
        'USER_FLOW': {
            'login': {
                'url': 'https://example.com/login',
                'username_field': 'input[name="username"]',
                'password_field': 'input[name="password"]',
                'login_button': 'button[type="submit"]',
                'username': 'your_username',
                'password': 'your_password'
            },
            'steps': [
                {
                    'name': 'Login Page',
                    'description': 'Navigate to the login page',
                    'action': 'navigate',
                    'url': 'https://example.com/login'
                },
                {
                    'name': 'Enter Credentials',
                    'description': 'Fill in username and password',
                    'action': 'fill_form',
                    'fields': {
                        'input[name="username"]': 'your_username',
                        'input[name="password"]': 'your_password'
                    }
                },
                {
                    'name': 'Submit Login',
                    'description': 'Click the login button',
                    'action': 'click',
                    'selector': 'button[type="submit"]'
                },
                {
                    'name': 'Dashboard',
                    'description': 'Wait for dashboard to load',
                    'action': 'wait_for_element',
                    'selector': '.dashboard',
                    'timeout': 10
                }
            ]
        }
    }
    
    with open('config.yaml', 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False, indent=2)
    
    print("✅ Sample configuration created: config.yaml")


def check_browser_drivers():
    """Check if browser drivers are available."""
    print("🌐 Checking browser drivers...")
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from webdriver_manager.firefox import GeckoDriverManager
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        
        print("✅ WebDriver Manager available")
        print("   Chrome driver will be downloaded automatically")
        print("   Firefox driver will be downloaded automatically")
        print("   Edge driver will be downloaded automatically")
        
    except ImportError:
        print("❌ WebDriver Manager not available")
        return False
    
    return True


def main():
    """Main setup function."""
    print("🚀 CaptureBot Setup")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return 1
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create directories
    create_directories()
    
    # Create sample configuration
    create_sample_config()
    
    # Check browser drivers
    if not check_browser_drivers():
        return 1
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit 'config.yaml' to configure your user flow")
    print("2. Run: python capture_bot.py")
    print("3. Or run: python example.py for a demo")
    print("\nFor help, see README.md")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
