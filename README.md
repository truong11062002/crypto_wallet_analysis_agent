# Crypto Wallet Analysis Agent

A comprehensive tool for analyzing Ethereum wallet behavior, transactions, and patterns using automated browser interactions and AI-powered analysis.

## Features

- Automated wallet data collection from Etherscan
- AI-powered analysis of wallet behavior patterns
- Multiple analysis modes:
  - Basic portfolio analysis
  - Wallet age analysis
  - Transaction pattern analysis
  - Behavioral analysis (bot vs human detection)
  - Trend analysis
- Support for multiple LLM providers (OpenAI, Google, Anthropic, DeepSeek, etc.)
- Browser automation with persistent session support
- Customizable browser settings and configurations

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Chrome browser (for web automation)
- API keys for LLM providers (OpenAI, Google, etc.)

### Installation

1. Clone the repository:

```bash
git clone [repository-url]
cd crypto-wallet-analysis-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright for browser automation:

```bash
playwright install
```

5. Create configuration file:

```bash
cp .env.example .env
```

6. Configure your environment variables in `.env`:

```
OPENAI_API_KEY=your_api_key_here
GOOGLE_API_KEY=your_api_key_here
CHROME_PATH=/path/to/chrome  # Optional, for custom browser
CHROME_USER_DATA=/path/to/user/data  # Optional, for persistent sessions
```

## Usage Examples

### Basic Wallet Analysis

```python
from src.analyzer import EthereumWalletAnalyzer

# Initialize analyzer
analyzer = EthereumWalletAnalyzer()

# Analyze a single wallet
analysis = analyzer.analyze_single_wallet(wallet_data)

# Analyze multiple wallets
results = analyzer.analyze_all_wallets()
analyzer.save_analysis(results, "analysis_results")
```

### Running Automated Analysis

```python
# Using the command line
python main.py

# With specific analysis modes
python main.py --analyze-age
python main.py --analyze-transactions
python main.py --analyze-behavior
```

### Scraping Ethereum Data

1. Create a file named `wallet_addresses.txt` with Ethereum addresses:

```text
0x123...
0x456...
```

2. Run the scraper with different analysis modes:

```python
# Portfolio Analysis
python scraper.py PROMPT_WALLET_ADDRESS

# Wallet Age Analysis
python scraper.py WALLET_AGE

# Transaction Pattern Analysis
python scraper.py TRANSACTIONS_PROMPT

# Trend Analysis
python scraper.py TREND_PROMPT

# Behavioral Analysis (Bot vs Human)
python scraper.py BEHAVIOR_PROMPT
```

The scraper will:

- Process each wallet address
- Save data in the `etherscan_wallet_*` directory
- Create separate files for each analysis type
- Handle rate limiting automatically
- Generate detailed reports for each wallet

### Custom Browser Configuration

```python
from browser_use.browser.browser import BrowserConfig
from src.browser.custom_browser import CustomBrowser

browser = CustomBrowser(
    config=BrowserConfig(
        headless=False,
        disable_security=True,
        chrome_instance_path="/path/to/chrome",
        extra_chromium_args=["--window-size=1920,1080"]
    )
)
```

## Design Decisions

### Architecture

1. **Modular Design**

   - Separate modules for data collection, analysis, and browser automation
   - Clean separation between core functionality and UI components
   - Extensible architecture for adding new analysis types

2. **Browser Automation**

   - Uses Playwright for reliable web automation
   - Custom browser management for persistent sessions
   - Configurable browser settings for different use cases

3. **AI Integration**
   - Multiple LLM provider support
   - Custom prompts for different analysis types
   - Structured output formats for consistent results

### Key Components

- `EthereumWalletAnalyzer`: Core analysis engine
- `CustomBrowser`: Enhanced browser automation
- `AgentState`: State management for browser sessions
- `DeepResearch`: Advanced research capabilities

## Limitations and Assumptions

### Limitations

1. **Data Collection**

   - Relies on Etherscan's web interface
   - Rate limited by web scraping constraints
   - May miss some transaction details due to pagination

2. **Analysis**

   - Accuracy depends on LLM model quality
   - May not capture complex trading patterns
   - Limited historical data analysis

3. **Browser Automation**
   - Requires Chrome browser
   - May break with Etherscan UI changes
   - Performance depends on network conditions

### Assumptions

1. **Wallet Activity**

   - Assumes wallet addresses are valid Ethereum addresses
   - Expects transactions to be visible on Etherscan
   - Assumes standard ERC-20 token transactions

2. **Environment**

   - Assumes Python 3.11+ environment
   - Expects Chrome browser installation
   - Requires stable internet connection

3. **API Access**
   - Assumes valid API keys for LLM providers
   - Expects rate limits to be respected
   - Assumes Etherscan accessibility

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## Future Work

### 1. Enhanced Data Accuracy

- Implement cross-validation with multiple data sources beyond Etherscan
- Add support for Layer 2 solutions (Arbitrum, Optimism, etc.)
- Develop methodology for historical price data integration
- Create validation framework for wallet analysis results
- Build automated tests for data accuracy verification

### 2. Robust Error Handling

- Implement comprehensive exception handling for network failures
- Add retry mechanisms with exponential backoff
- Create detailed error logging and reporting system
- Develop recovery mechanisms for interrupted analysis
- Add validation for input data formats and wallet addresses

### 3. Documentation and Methodology

- Create detailed technical documentation for each analysis type
- Document statistical methods and assumptions
- Add case studies and example analyses
- Create user guides for different user personas
- Document best practices for custom analysis implementation

### 4. Rate Limiting and Performance

- Implement smart rate limiting with multiple API keys
- Add caching layer for frequently accessed data
- Develop batch processing for multiple wallets
- Create queue system for large-scale analysis
- Optimize browser automation performance

### 5. Analysis Enhancement

- Add machine learning models for pattern recognition
- Implement sentiment analysis from on-chain data
- Create visualization tools for analysis results
- Add support for NFT transaction analysis
- Develop real-time monitoring capabilities

### 6. User Experience

- Create interactive CLI interface
- Develop web interface for analysis results
- Add customizable report templates
- Implement progress tracking for long-running analyses
- Create API for programmatic access

## License

[MIT License](LICENSE)
