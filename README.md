# CaptureBot - Web Automation and Presentation Generator

A Python bot that automates web interactions, captures screenshots, and generates PowerPoint presentations documenting user flows.

## 🚀 Features

- **Web Automation**: Uses Selenium to automate browser interactions
- **Screenshot Capture**: Takes screenshots at each step of the user flow
- **PowerPoint Generation**: Automatically creates .pptx presentations with:
  - Cover slide
  - Table of contents
  - One slide per step with screenshots
  - Summary slide
- **Configurable**: YAML-based configuration for easy customization
- **Multi-browser Support**: Chrome, Firefox, and Edge
- **Error Handling**: Comprehensive logging and error recovery

## 📦 Installation

### Quick Setup

1. **Clone or download this repository**
2. **Run the setup script**:
   ```bash
   python setup.py
   ```

### Manual Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Create necessary directories**:
   ```bash
   mkdir screenshots output logs
   ```

3. **Configure your user flow** in `config.yaml`

## ⚙️ Configuration

Edit `config.yaml` to customize your bot:

### Web Driver Settings
```yaml
WEB_DRIVER:
  browser: "chrome"  # chrome, firefox, edge
  headless: false     # Set to true for headless mode
  window_size: [1920, 1080]
  implicit_wait: 10
```

### User Flow Steps
```yaml
USER_FLOW:
  steps:
    - name: "Login Page"
      description: "Navigate to login page"
      action: "navigate"
      url: "https://example.com/login"
    
    - name: "Enter Credentials"
      description: "Fill in username and password"
      action: "fill_form"
      fields:
        'input[name="username"]': 'your_username'
        'input[name="password"]': 'your_password'
    
    - name: "Submit Login"
      description: "Click login button"
      action: "click"
      selector: 'button[type="submit"]'
```

### Supported Actions

- `navigate`: Navigate to a URL
- `fill_form`: Fill form fields
- `click`: Click an element
- `wait_for_element`: Wait for an element to appear
- `scroll`: Scroll the page (direction: up/down/top/bottom)
- `hover`: Hover over an element

## 🎯 Usage

### Basic Usage
```bash
python capture_bot.py
```

### With Custom Config
```bash
python capture_bot.py --config my_config.yaml
```

### Dry Run (Validation Only)
```bash
python capture_bot.py --dry-run
```

### Example Demo
```bash
python example.py
```

## 📊 Output

The bot generates:
- **PowerPoint Presentation**: `user_flow_documentation.pptx`
- **Screenshots**: Saved in `screenshots/` directory
- **Log File**: `capture_bot.log`

## 🔧 Advanced Usage

### Command Line Options
```bash
python capture_bot.py --help
```

Options:
- `--config, -c`: Specify configuration file
- `--dry-run, -d`: Run validation only
- `--verbose, -v`: Enable verbose logging

### Programmatic Usage
```python
from capture_bot import CaptureBot

# Create bot instance
bot = CaptureBot('config.yaml')

# Run the complete process
presentation_file = bot.run()

# Or run individual components
bot.initialize_components()
screenshots = bot.execute_user_flow()
presentation = bot.generate_presentation()
```

## 🛠️ Troubleshooting

### Common Issues

1. **Browser Driver Issues**:
   - Drivers are automatically managed by webdriver-manager
   - Ensure you have Chrome, Firefox, or Edge installed

2. **Element Not Found**:
   - Check CSS selectors in your configuration
   - Increase `implicit_wait` time
   - Use browser developer tools to verify selectors

3. **Screenshot Issues**:
   - Ensure `screenshots/` directory exists
   - Check file permissions

4. **PowerPoint Generation**:
   - Ensure `python-pptx` is installed
   - Check that screenshots exist before generating presentation

### Debug Mode
```bash
python capture_bot.py --verbose
```

## 📁 Project Structure

```
CaptureBot/
├── capture_bot.py          # Main bot orchestrator
├── web_automation.py        # Selenium web automation
├── presentation_generator.py # PowerPoint generation
├── config_manager.py        # Configuration management
├── example.py              # Example usage script
├── setup.py                # Setup script
├── config.yaml             # Configuration file
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── screenshots/            # Screenshot output directory
├── output/                 # Presentation output directory
└── logs/                   # Log files
```

## 🔒 Security Notes

- **Credentials**: Store sensitive information in environment variables or secure config files
- **Headless Mode**: Use headless mode for production environments
- **Rate Limiting**: Add delays between actions to avoid overwhelming target sites

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed.

## 🆘 Support

For issues and questions:
1. Check the log file: `capture_bot.log`
2. Run with `--verbose` flag for detailed output
3. Validate configuration with `--dry-run`
4. Check browser console for JavaScript errors

## 🔄 Requirements

- Python 3.7+
- Chrome, Firefox, or Edge browser
- Internet connection for web automation
- Sufficient disk space for screenshots and presentations
