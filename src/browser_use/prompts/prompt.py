PROMPT_WALLET_ADDRESS = """
Go to https://etherscan.io/address/{wallet_address}.

Analyze this wallet's cryptocurrency portfolio to get:

**1. Token Holdings:**
   - List all tokens (ETH and ERC-20) held.
   - For each, get name/symbol and balance.

**2. USD Value per Token:**
   - Find the current USD price for each token via web search (e.g., "[Token Name/Symbol] price USD").
   - Note if the price is not found.

**3. USD Value of Holdings:**
   - Calculate USD value for each token holding (Balance * USD Price).

**4. Total Portfolio USD Value:**
   - Sum the USD values of all holdings.

**5. Asset Percentage Distribution:**
   - Calculate the percentage of each token's USD value relative to the total portfolio value.

**6. First Transaction Date:**
   - Find the date of the wallet's first transaction in YYYY-MM-DD format.

**7. Wallet Age:**
   - Calculate the wallet's age in years, months, and days from the first transaction date.

**8. Wallet Experience Level:**
   - Categorize the wallet as one of the following based on its age:
     - "Veteran" (5+ years)
     - "Established" (2-5 years)
     - "Intermediate" (1-2 years)
     - "Newcomer" (less than 1 year)

**9. Interpretation of Wallet Age:**
   - Provide a brief interpretation of what the wallet's age suggests about the holder's experience with cryptocurrencies.

**Output Format:**

Please present the extracted and calculated information in a clear and organized text format under the following headings:
Wallet Address: {wallet_address}

--- Portfolio Analysis ---

--- Token Holdings & USD Values ---
[Token 1 Name/Symbol]: Balance: [Token 1 Balance], USD Price: [USD Price or 'Price not found'], USD Value: [USD Value or 'Price not found']
[Token 2 Name/Symbol]: Balance: [Token 2 Balance], USD Price: [USD Price or 'Price not found'], USD Value: [USD Value or 'Price not found']
... (and so on for all tokens)

--- Total Portfolio Value (USD): [Total USD Value]

--- Asset Distribution (%) ---
[Token 1 Name/Symbol]: [Percentage]%
[Token 2 Name/Symbol]: [Percentage]%
... (and so on for all tokens with USD value)

--- First Transaction: [YYYY-MM-DD]
--- Wallet Age: [X] years, [Y] months, [Z] days  
--- Category: [Veteran/Established/Intermediate/Newcomer]
--- Analysis: [Brief interpretation of wallet age and holder's experience]

**Important Notes:**

*   USD prices are estimates from web search.
*   Indicate "Price not found" when USD price is unavailable.
*   Base token list on Etherscan's "Tokens" section.
"""

WALLET_AGE = """
Task: Cryptocurrency Wallet Portfolio Analysis on Etherscan

Objective: Analyze the cryptocurrency portfolio of a given Ethereum wallet address using Etherscan to determine its age, categorize its activity, and provide a brief interpretation of its transactional history.

Instructions:
1. Go to https://etherscan.io/address/{wallet_address}

2. **Once on the Etherscan page for the specified wallet address, perform the following analysis by examining the webpage content:**

   * **First Transaction Date:**
     * Locate the "Transactions" section (typically labeled as "Transactions").
     * Find the very first transaction listed in the "Transactions" history. This will usually be at the bottom of the transaction list (oldest transactions first).
     * Extract the date of this first transaction in YYYY-MM-DD format.

   * **Wallet Age:**
     * Calculate the age of the wallet based on the "First Transaction Date" and the current date.
     * Express the wallet age in years, months, and days.

   * **Category:**
     - "Veteran" (5+ years)
    - "Established" (2-5 years)
    - "Intermediate" (1-2 years)
    - "Newcomer" (less than 1 year)

   * **Analysis:**
     * Write a brief interpretation of your findings.
     * Justify your chosen category based on the observed transaction patterns.
     * Highlight any interesting observations or notable patterns in the wallet's activity.

**Output Format:**
First Transaction: YYYY-MM-DD
Wallet Age: X years, Y months, Z days
Category: [Category]
Analysis: [Brief interpretation]
"""
