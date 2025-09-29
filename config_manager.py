"""
Configuration management module.
Handles loading and validation of configuration files.
"""

import os
import yaml
import logging
from typing import Dict, Any, List
from pathlib import Path


class ConfigManager:
    """Manages configuration loading and validation."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the configuration manager."""
        self.config_path = config_path
        self.config: Dict[str, Any] = {}
        self.logger = logging.getLogger(__name__)
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            if not os.path.exists(self.config_path):
                self.logger.warning(f"Config file {self.config_path} not found, using defaults")
                return self._get_default_config()
            
            with open(self.config_path, 'r', encoding='utf-8') as file:
                self.config = yaml.safe_load(file) or {}
            
            # Merge with defaults for missing keys
            default_config = self._get_default_config()
            self.config = self._merge_configs(default_config, self.config)
            
            self.logger.info(f"Configuration loaded from {self.config_path}")
            return self.config
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.logger.info("Using default configuration")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration."""
        return {
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
                        'description': 'Initial login screen',
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
                        'description': 'Click login button',
                        'action': 'click',
                        'selector': 'button[type="submit"]'
                    },
                    {
                        'name': 'Dashboard',
                        'description': 'Main dashboard after login',
                        'action': 'wait_for_element',
                        'selector': '.dashboard',
                        'timeout': 10
                    }
                ]
            }
        }
    
    def _merge_configs(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """Merge user configuration with defaults."""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        
        return result
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return list of errors."""
        errors = []
        
        # Validate web driver settings
        web_driver = self.config.get('WEB_DRIVER', {})
        if web_driver.get('browser') not in ['chrome', 'firefox', 'edge']:
            errors.append("WEB_DRIVER.browser must be 'chrome', 'firefox', or 'edge'")
        
        window_size = web_driver.get('window_size', [])
        if not isinstance(window_size, list) or len(window_size) != 2:
            errors.append("WEB_DRIVER.window_size must be a list of two integers")
        
        # Validate user flow
        user_flow = self.config.get('USER_FLOW', {})
        steps = user_flow.get('steps', [])
        
        if not steps:
            errors.append("USER_FLOW.steps cannot be empty")
        
        for i, step in enumerate(steps):
            if not isinstance(step, dict):
                errors.append(f"Step {i+1} must be a dictionary")
                continue
            
            if not step.get('name'):
                errors.append(f"Step {i+1} must have a 'name' field")
            
            if not step.get('action'):
                errors.append(f"Step {i+1} must have an 'action' field")
            
            action = step.get('action', '').lower()
            if action == 'navigate' and not step.get('url'):
                errors.append(f"Step {i+1} with 'navigate' action must have a 'url' field")
            
            elif action == 'click' and not step.get('selector'):
                errors.append(f"Step {i+1} with 'click' action must have a 'selector' field")
            
            elif action == 'fill_form' and not step.get('fields'):
                errors.append(f"Step {i+1} with 'fill_form' action must have a 'fields' field")
            
            elif action == 'wait_for_element' and not step.get('selector'):
                errors.append(f"Step {i+1} with 'wait_for_element' action must have a 'selector' field")
        
        return errors
    
    def get_step_by_name(self, name: str) -> Dict[str, Any]:
        """Get a step by its name."""
        steps = self.config.get('USER_FLOW', {}).get('steps', [])
        for step in steps:
            if step.get('name') == name:
                return step
        return {}
    
    def get_login_config(self) -> Dict[str, Any]:
        """Get login configuration."""
        return self.config.get('USER_FLOW', {}).get('login', {})
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """Get all user flow steps."""
        return self.config.get('USER_FLOW', {}).get('steps', [])
    
    def get_web_driver_config(self) -> Dict[str, Any]:
        """Get web driver configuration."""
        return self.config.get('WEB_DRIVER', {})
    
    def get_screenshot_config(self) -> Dict[str, Any]:
        """Get screenshot configuration."""
        return self.config.get('SCREENSHOTS', {})
    
    def get_presentation_config(self) -> Dict[str, Any]:
        """Get presentation configuration."""
        return self.config.get('PRESENTATION', {})
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """Save configuration to file."""
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(config, file, default_flow_style=False, indent=2)
            self.logger.info(f"Configuration saved to {self.config_path}")
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            raise
    
    def create_sample_config(self) -> None:
        """Create a sample configuration file."""
        sample_config = self._get_default_config()
        self.save_config(sample_config)
        self.logger.info(f"Sample configuration created at {self.config_path}")
