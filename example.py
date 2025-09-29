#!/usr/bin/env python3
"""
Example script demonstrating CaptureBot usage.
This script shows how to customize the bot for a specific website.
"""

import os
import sys
from capture_bot import CaptureBot


def create_example_config():
    """Create an example configuration for a demo website."""
    config = {
        'WEB_DRIVER': {
            'browser': 'chrome',
            'headless': False,  # Set to True for headless mode
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
            'title': 'Demo Website User Flow',
            'author': 'CaptureBot',
            'slide_width': 9144000,
            'slide_height': 6858000
        },
        'USER_FLOW': {
            'login': {
                'url': 'https://httpbin.org/forms/post',
                'username_field': 'input[name="custname"]',
                'password_field': 'input[name="custtel"]',
                'login_button': 'input[type="submit"]',
                'username': 'demo_user',
                'password': 'demo_password'
            },
            'steps': [
                {
                    'name': 'Demo Form Page',
                    'description': 'Navigate to the demo form page',
                    'action': 'navigate',
                    'url': 'https://httpbin.org/forms/post'
                },
                {
                    'name': 'Fill Customer Name',
                    'description': 'Enter customer name in the form',
                    'action': 'fill_form',
                    'fields': {
                        'input[name="custname"]': 'John Doe'
                    }
                },
                {
                    'name': 'Fill Customer Email',
                    'description': 'Enter customer email address',
                    'action': 'fill_form',
                    'fields': {
                        'input[name="custemail"]': 'john.doe@example.com'
                    }
                },
                {
                    'name': 'Select Size',
                    'description': 'Select pizza size from dropdown',
                    'action': 'click',
                    'selector': 'select[name="size"]'
                },
                {
                    'name': 'Choose Large Size',
                    'description': 'Select large size option',
                    'action': 'click',
                    'selector': 'option[value="large"]'
                },
                {
                    'name': 'Add Toppings',
                    'description': 'Select additional toppings',
                    'action': 'click',
                    'selector': 'input[name="topping"][value="bacon"]'
                },
                {
                    'name': 'Add Delivery Instructions',
                    'description': 'Enter delivery instructions',
                    'action': 'fill_form',
                    'fields': {
                        'textarea[name="comments"]': 'Please ring the doorbell twice. Leave at front door if no answer.'
                    }
                },
                {
                    'name': 'Review Form',
                    'description': 'Final form review before submission',
                    'action': 'scroll',
                    'direction': 'top'
                }
            ]
        }
    }
    
    return config


def main():
    """Main example function."""
    print("🚀 CaptureBot Example Script")
    print("=" * 50)
    
    # Create example configuration
    print("📝 Creating example configuration...")
    example_config = create_example_config()
    
    # Save configuration to file
    import yaml
    with open('example_config.yaml', 'w') as f:
        yaml.dump(example_config, f, default_flow_style=False, indent=2)
    
    print("✅ Example configuration saved to 'example_config.yaml'")
    
    # Ask user if they want to run the bot
    print("\n" + "=" * 50)
    response = input("Would you like to run CaptureBot with this example? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🤖 Starting CaptureBot...")
        
        try:
            # Create and run bot with example config
            bot = CaptureBot('example_config.yaml')
            presentation_file = bot.run()
            
            print(f"\n✅ CaptureBot completed successfully!")
            print(f"📊 Presentation generated: {presentation_file}")
            print(f"📸 Screenshots saved in: screenshots/")
            print(f"📋 Log file: capture_bot.log")
            
        except Exception as e:
            print(f"\n❌ CaptureBot failed: {e}")
            print("Check the log file 'capture_bot.log' for details.")
            return 1
    
    else:
        print("\n📚 Example configuration created. You can:")
        print("   1. Edit 'example_config.yaml' to customize the flow")
        print("   2. Run: python capture_bot.py --config example_config.yaml")
        print("   3. Or run: python example.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
