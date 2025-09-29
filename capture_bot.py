"""
Main CaptureBot orchestrator.
Coordinates web automation, screenshot capture, and presentation generation.
"""

import os
import logging
import time
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from config_manager import ConfigManager
from web_automation import WebAutomation
from presentation_generator import PresentationGenerator


class CaptureBot:
    """Main bot that orchestrates the entire capture process."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the CaptureBot."""
        self.config_manager = ConfigManager(config_path)
        self.config = self.config_manager.load_config()
        self.web_automation = None
        self.presentation_generator = None
        self.screenshots = []
        
        # Set up logging
        self._setup_logging()
        self.logger = logging.getLogger(__name__)
        
        # Create necessary directories
        self._create_directories()
    
    def _setup_logging(self) -> None:
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('capture_bot.log'),
                logging.StreamHandler()
            ]
        )
    
    def _create_directories(self) -> None:
        """Create necessary directories."""
        directories = ['screenshots', 'output']
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
    
    def validate_configuration(self) -> bool:
        """Validate the configuration and return True if valid."""
        errors = self.config_manager.validate_config()
        
        if errors:
            self.logger.error("Configuration validation failed:")
            for error in errors:
                self.logger.error(f"  - {error}")
            return False
        
        self.logger.info("Configuration validation passed")
        return True
    
    def initialize_components(self) -> None:
        """Initialize web automation and presentation generator."""
        try:
            self.web_automation = WebAutomation(self.config)
            self.presentation_generator = PresentationGenerator(self.config)
            self.logger.info("Components initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize components: {e}")
            raise
    
    def execute_user_flow(self) -> List[str]:
        """Execute the user flow and capture screenshots."""
        if not self.web_automation:
            raise ValueError("Web automation not initialized")
        
        self.logger.info("Starting user flow execution")
        
        try:
            # Set up browser
            self.web_automation.setup_driver()
            
            # Get steps from configuration
            steps = self.config_manager.get_steps()
            screenshots = []
            
            # Execute each step and take screenshots
            for i, step in enumerate(steps, 1):
                step_name = step.get('name', f'Step {i}')
                self.logger.info(f"Executing step {i}/{len(steps)}: {step_name}")
                
                # Execute the step
                self.web_automation.execute_step(step)
                
                # Take screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_filename = f"step_{i:02d}_{step_name.replace(' ', '_').lower()}_{timestamp}.png"
                screenshot_path = self.web_automation.take_screenshot(screenshot_filename)
                screenshots.append(screenshot_path)
                
                self.logger.info(f"Screenshot captured: {screenshot_path}")
            
            self.screenshots = screenshots
            self.logger.info(f"User flow completed. Captured {len(screenshots)} screenshots")
            return screenshots
            
        except Exception as e:
            self.logger.error(f"Failed to execute user flow: {e}")
            raise
        finally:
            # Always close the browser
            if self.web_automation:
                self.web_automation.close()
    
    def generate_presentation(self) -> str:
        """Generate PowerPoint presentation from captured data."""
        if not self.presentation_generator:
            raise ValueError("Presentation generator not initialized")
        
        if not self.screenshots:
            raise ValueError("No screenshots available for presentation")
        
        self.logger.info("Generating PowerPoint presentation")
        
        try:
            steps = self.config_manager.get_steps()
            presentation_config = self.config_manager.get_presentation_config()
            title = presentation_config.get('title', 'User Flow Documentation')
            
            # Generate presentation
            filename = self.presentation_generator.generate_presentation(
                steps=steps,
                screenshots=self.screenshots,
                title=title
            )
            
            self.logger.info(f"Presentation generated: {filename}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to generate presentation: {e}")
            raise
    
    def run(self) -> str:
        """Run the complete capture process."""
        self.logger.info("Starting CaptureBot")
        
        try:
            # Validate configuration
            if not self.validate_configuration():
                raise ValueError("Configuration validation failed")
            
            # Initialize components
            self.initialize_components()
            
            # Execute user flow and capture screenshots
            self.execute_user_flow()
            
            # Generate presentation
            presentation_file = self.generate_presentation()
            
            self.logger.info(f"CaptureBot completed successfully. Presentation: {presentation_file}")
            return presentation_file
            
        except Exception as e:
            self.logger.error(f"CaptureBot failed: {e}")
            raise
        finally:
            # Cleanup
            if self.web_automation:
                self.web_automation.close()
    
    def run_dry(self) -> None:
        """Run a dry run to validate configuration without executing."""
        self.logger.info("Starting CaptureBot dry run")
        
        try:
            # Validate configuration
            if not self.validate_configuration():
                raise ValueError("Configuration validation failed")
            
            # Initialize components (without starting browser)
            self.presentation_generator = PresentationGenerator(self.config)
            
            # Check if we can access the presentation generator
            steps = self.config_manager.get_steps()
            self.logger.info(f"Configuration valid. Found {len(steps)} steps to execute:")
            
            for i, step in enumerate(steps, 1):
                self.logger.info(f"  {i}. {step.get('name', 'Unknown Step')} - {step.get('action', 'Unknown Action')}")
            
            self.logger.info("Dry run completed successfully")
            
        except Exception as e:
            self.logger.error(f"Dry run failed: {e}")
            raise
    
    def cleanup(self) -> None:
        """Clean up temporary files and resources."""
        try:
            # Close browser if still open
            if self.web_automation:
                self.web_automation.close()
            
            self.logger.info("Cleanup completed")
        except Exception as e:
            self.logger.error(f"Cleanup failed: {e}")


def main():
    """Main entry point for the CaptureBot."""
    import argparse
    
    parser = argparse.ArgumentParser(description='CaptureBot - Web automation and presentation generator')
    parser.add_argument('--config', '-c', default='config.yaml', help='Configuration file path')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Run validation only, do not execute')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create and run bot
    bot = CaptureBot(args.config)
    
    try:
        if args.dry_run:
            bot.run_dry()
        else:
            presentation_file = bot.run()
            print(f"\n✅ CaptureBot completed successfully!")
            print(f"📊 Presentation generated: {presentation_file}")
            print(f"📸 Screenshots saved in: screenshots/")
    except Exception as e:
        print(f"\n❌ CaptureBot failed: {e}")
        return 1
    finally:
        bot.cleanup()
    
    return 0


if __name__ == "__main__":
    exit(main())
