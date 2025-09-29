#!/usr/bin/env python3
"""
Generate PowerPoint from existing screenshots
"""

import os
from presentation_generator import PresentationGenerator

def main():
    # Create presentation generator
    config = {
        'PRESENTATION': {
            'title': 'VentureCare Login Flow Demo',
            'author': 'CaptureBot',
            'slide_width': 9144000,
            'slide_height': 6858000
        }
    }
    
    generator = PresentationGenerator(config)
    
    # Define steps based on captured screenshots
    steps = [
        {
            'name': 'Login Page',
            'description': 'Navigate to VentureCare demo login page'
        },
        {
            'name': 'Enter Email',
            'description': 'Enter seller email address'
        },
        {
            'name': 'Enter Password',
            'description': 'Enter password'
        },
        {
            'name': 'Click Login',
            'description': 'Submit login form'
        }
    ]
    
    # Get screenshot files
    screenshots = []
    screenshot_dir = 'screenshots'
    
    if os.path.exists(screenshot_dir):
        screenshot_files = sorted([f for f in os.listdir(screenshot_dir) if f.endswith('.png')])
        screenshots = [os.path.join(screenshot_dir, f) for f in screenshot_files]
    
    print(f"Found {len(screenshots)} screenshots")
    
    if screenshots:
        # Generate presentation
        filename = generator.generate_presentation(
            steps=steps,
            screenshots=screenshots,
            title="VentureCare Login Flow Demo"
        )
        print(f"✅ Presentation generated: {filename}")
    else:
        print("❌ No screenshots found")

if __name__ == "__main__":
    main()
