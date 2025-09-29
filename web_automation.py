"""
Web automation module using Selenium WebDriver.
Handles browser setup, navigation, and user interactions.
"""

import time
import logging
from typing import Dict, List, Optional, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class WebAutomation:
    """Handles web automation using Selenium WebDriver."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the web automation with configuration."""
        self.config = config
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = logging.getLogger(__name__)
        
    def setup_driver(self) -> None:
        """Set up the WebDriver based on configuration."""
        browser = self.config['WEB_DRIVER']['browser'].lower()
        headless = self.config['WEB_DRIVER']['headless']
        window_size = self.config['WEB_DRIVER']['window_size']
        implicit_wait = self.config['WEB_DRIVER']['implicit_wait']
        
        try:
            if browser == 'chrome':
                options = webdriver.ChromeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
                
                driver_path = ChromeDriverManager().install()
                # Fix for webdriver manager issue - use the actual chromedriver file
                if 'THIRD_PARTY_NOTICES.chromedriver' in driver_path:
                    driver_path = driver_path.replace('THIRD_PARTY_NOTICES.chromedriver', 'chromedriver')
                service = ChromeService(driver_path)
                self.driver = webdriver.Chrome(service=service, options=options)
                
            elif browser == 'firefox':
                options = webdriver.FirefoxOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument(f'--width={window_size[0]}')
                options.add_argument(f'--height={window_size[1]}')
                
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
                
            elif browser == 'edge':
                options = webdriver.EdgeOptions()
                if headless:
                    options.add_argument('--headless')
                options.add_argument(f'--window-size={window_size[0]},{window_size[1]}')
                
                service = EdgeService(EdgeChromiumDriverManager().install())
                self.driver = webdriver.Edge(service=service, options=options)
                
            else:
                raise ValueError(f"Unsupported browser: {browser}")
            
            self.driver.implicitly_wait(implicit_wait)
            self.wait = WebDriverWait(self.driver, implicit_wait)
            self.logger.info(f"WebDriver initialized for {browser}")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL."""
        try:
            self.driver.get(url)
            self.logger.info(f"Navigated to: {url}")
            time.sleep(2)  # Allow page to load
        except Exception as e:
            self.logger.error(f"Failed to navigate to {url}: {e}")
            raise
    
    def find_element(self, selector: str, timeout: int = 10) -> Any:
        """Find an element using CSS selector or XPath."""
        try:
            if selector.startswith('//') or selector.startswith('(//'):
                # XPath selector
                element = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
            else:
                # CSS selector
                element = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {selector}")
            raise
        except Exception as e:
            self.logger.error(f"Error finding element {selector}: {e}")
            raise
    
    def click_element(self, selector: str, timeout: int = 10) -> None:
        """Click an element."""
        try:
            element = self.find_element(selector, timeout)
            # Scroll element into view
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(0.5)
            
            # Try regular click first
            try:
                element.click()
            except:
                # If regular click fails, use JavaScript click
                self.driver.execute_script("arguments[0].click();", element)
            
            self.logger.info(f"Clicked element: {selector}")
            time.sleep(1)  # Allow for page changes
            
        except Exception as e:
            self.logger.error(f"Failed to click element {selector}: {e}")
            raise
    
    def fill_form_field(self, selector: str, value: str, timeout: int = 10) -> None:
        """Fill a form field with a value."""
        try:
            element = self.find_element(selector, timeout)
            element.clear()
            element.send_keys(value)
            self.logger.info(f"Filled field {selector} with value: {value}")
            time.sleep(0.5)
        except Exception as e:
            self.logger.error(f"Failed to fill field {selector}: {e}")
            raise
    
    def fill_form_fields(self, fields: Dict[str, str]) -> None:
        """Fill multiple form fields."""
        for selector, value in fields.items():
            self.fill_form_field(selector, value)
    
    def wait_for_element(self, selector: str, timeout: int = 10) -> None:
        """Wait for an element to be present."""
        try:
            self.find_element(selector, timeout)
            self.logger.info(f"Element appeared: {selector}")
        except Exception as e:
            self.logger.error(f"Element did not appear: {selector}")
            raise
    
    def scroll_page(self, direction: str = "down", pixels: int = 500) -> None:
        """Scroll the page."""
        try:
            if direction == "down":
                self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            elif direction == "up":
                self.driver.execute_script(f"window.scrollBy(0, -{pixels});")
            elif direction == "top":
                self.driver.execute_script("window.scrollTo(0, 0);")
            elif direction == "bottom":
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            self.logger.info(f"Scrolled {direction}")
            time.sleep(1)
        except Exception as e:
            self.logger.error(f"Failed to scroll: {e}")
            raise
    
    def hover_element(self, selector: str, timeout: int = 10) -> None:
        """Hover over an element."""
        try:
            element = self.find_element(selector, timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {selector}")
            time.sleep(1)
        except Exception as e:
            self.logger.error(f"Failed to hover over element {selector}: {e}")
            raise
    
    def execute_step(self, step: Dict[str, Any]) -> None:
        """Execute a single step in the user flow."""
        action = step.get('action', '').lower()
        name = step.get('name', 'Unknown Step')
        
        self.logger.info(f"Executing step: {name}")
        
        try:
            if action == 'navigate':
                url = step.get('url')
                if url:
                    self.navigate_to(url)
                else:
                    raise ValueError("URL not specified for navigate action")
            
            elif action == 'click':
                selector = step.get('selector')
                timeout = step.get('timeout', 10)
                if selector:
                    self.click_element(selector, timeout)
                else:
                    raise ValueError("Selector not specified for click action")
            
            elif action == 'fill_form':
                fields = step.get('fields', {})
                if fields:
                    self.fill_form_fields(fields)
                else:
                    raise ValueError("Fields not specified for fill_form action")
            
            elif action == 'wait_for_element':
                selector = step.get('selector')
                timeout = step.get('timeout', 10)
                if selector:
                    self.wait_for_element(selector, timeout)
                else:
                    raise ValueError("Selector not specified for wait_for_element action")
            
            elif action == 'scroll':
                direction = step.get('direction', 'down')
                pixels = step.get('pixels', 500)
                self.scroll_page(direction, pixels)
            
            elif action == 'hover':
                selector = step.get('selector')
                timeout = step.get('timeout', 10)
                if selector:
                    self.hover_element(selector, timeout)
                else:
                    raise ValueError("Selector not specified for hover action")
            
            else:
                raise ValueError(f"Unknown action: {action}")
            
            # Wait after action for page to stabilize
            delay = self.config.get('SCREENSHOTS', {}).get('delay_after_action', 2)
            time.sleep(delay)
            
        except Exception as e:
            self.logger.error(f"Failed to execute step '{name}': {e}")
            raise
    
    def take_screenshot(self, filename: str) -> str:
        """Take a screenshot and save it."""
        try:
            if self.config.get('SCREENSHOTS', {}).get('full_page', True):
                # Full page screenshot
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                viewport_height = self.driver.execute_script("return window.innerHeight")
                
                if total_height > viewport_height:
                    # Take multiple screenshots and stitch them together
                    screenshots = []
                    for i in range(0, total_height, viewport_height):
                        self.driver.execute_script(f"window.scrollTo(0, {i});")
                        time.sleep(0.5)
                        screenshot = self.driver.get_screenshot_as_png()
                        screenshots.append(screenshot)
                    
                    # For now, just take a single screenshot of the current viewport
                    # In a production version, you'd stitch the screenshots together
                    screenshot_path = f"screenshots/{filename}"
                    self.driver.save_screenshot(screenshot_path)
                else:
                    screenshot_path = f"screenshots/{filename}"
                    self.driver.save_screenshot(screenshot_path)
            else:
                screenshot_path = f"screenshots/{filename}"
                self.driver.save_screenshot(screenshot_path)
            
            self.logger.info(f"Screenshot saved: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {e}")
            raise
    
    def close(self) -> None:
        """Close the browser."""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")
