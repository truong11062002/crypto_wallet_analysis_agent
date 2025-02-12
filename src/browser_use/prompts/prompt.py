PROMPT_WALLET_ADDRESS = """
Go to https://etherscan.io/address/{wallet_address} to get complete list of all cryptocurrency tokens held, current USD value of each token, total portfolio value in USD, and percentage distribution of assets

Objective: 
Analyze the wallet's cryptocurrency portfolio to get complete list of all cryptocurrency tokens held, current USD value of each token, total portfolio value in USD, and percentage distribution of assets.

Instructions:

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

** 5. Percentage distribution of assets **
   - Calculate the percentage of each token's USD value relative to the total portfolio value.


**Output Format:**
--- Token Holdings & USD Values ---
[Token 1 Name/Symbol]: Balance: [Token 1 Balance], USD Price: [USD Price or 'Price not found'], USD Value: [USD Value or 'Price not found']
[Token 2 Name/Symbol]: Balance: [Token 2 Balance], USD Price: [USD Price or 'Price not found'], USD Value: [USD Value or 'Price not found']
... (and so on for all tokens)

--- Total Portfolio Value (USD): [Total USD Value]

--- Asset Distribution (%) ---
[Token 1 Name/Symbol]: [Percentage]%
[Token 2 Name/Symbol]: [Percentage]%
... (and so on for all tokens with USD value)

-- Percentage Distribution --
[Token 1 Name/Symbol]: [Percentage]%
[Token 2 Name/Symbol]: [Percentage]%
... (and so on for all tokens with USD value)
"""

WALLET_AGE = """
Go to https://etherscan.io/address/{wallet_address} to determine the age of the wallet, first transaction date, and categorization.

Objective: Analyze the cryptocurrency portfolio of a given Ethereum wallet address using Etherscan to determine its age, categorize its activity, and provide a brief interpretation of its transactional history.

Instructions:
1. **Once on the Etherscan page for the specified wallet address, perform the following analysis by examining the webpage content:**

2. **First Transaction Date:**
   * Locate the "Transactions" section (typically labeled as "Transactions").
   * Find the very first transaction listed in the "Transactions" history. This will usually be at the bottom of the transaction list (oldest transactions first).
   * Extract the date of this first transaction in YYYY-MM-DD format.

3. **Wallet Age:**
   * Calculate the age of the wallet based on the "First Transaction Date" and the current date.
   * Express the wallet age in years, months, and days.

4. **Category:**
   - "Veteran" (5+ years)
   - "Established" (2-5 years)
   - "Intermediate" (1-2 years)
   - "Newcomer" (less than 1 year)

5. **Analysis:**
   * Write a brief interpretation of your findings.
   * Justify your chosen category based on the observed transaction patterns.
   * Highlight any interesting observations or notable patterns in the wallet's activity.

**Output Format:**
First Transaction: YYYY-MM-DD
Wallet Age: X years, Y months, Z days
Category: [Category]
Analysis: [Brief interpretation]

"""

TREND_PROMPT = """
Go go https://etherscan.io/address/{wallet_address}#analytics to identify portfolio trends over the last 30, 90, and 180 days.

Objective: Analyze the cryptocurrency portfolio of a given Ethereum wallet address using Etherscan to determine its trends over the last 30, 90, and 180 days.
Instructions:
For each timeframe (30-day, 90-day, and 180-day), analyze the following:

1. **Overall Portfolio Value Change:** Determine if the overall portfolio value has increased, decreased, or remained stable.  Infer this from the balance chart and transaction history.  Focus on the net change in value over each period.

2. **Notable Asset Acquisitions or Sales:** Identify significant transactions that indicate the acquisition or sale of assets (ETH, ERC-20 tokens, NFTs if visible in transaction history or implied by balance changes).  "Notable" implies large transactions in value or transactions involving assets that appear to be strategically important within the portfolio based on context clues.

3. **Significant Pattern Changes:** Look for any shifts in transaction patterns. This could include changes in transaction frequency, types of assets being traded, or shifts in the overall balance trend (e.g., moving from accumulation to distribution, or vice versa).

**Output Format:**
30-Day Trend:
- Overall change: [increase/decrease/stable]
- Notable changes: [List significant asset acquisitions/sales and pattern changes as bullet points]

90-Day Trend:
- Overall change: [increase/decrease/stable]
- Notable changes: [List significant asset acquisitions/sales and pattern changes as bullet points]

180-Day Trend:
- Overall change: [increase/decrease/stable]
- Notable changes: [List significant asset acquisitions/sales and pattern changes as bullet points]
"""

TRANSACTIONS_PROMPT = """
Go to https://etherscan.io/address/{wallet_address}#transactions to analyze the transaction history of the wallet.

Objective: Analyze the transaction history of a given Ethereum wallet address using Etherscan to identify patterns and trends.

**Instructions:**

1. **Average Transaction Analysis:**
- Calculate the average transaction size in USD for the last 30 days. To do this, convert each transaction value (in ETH or tokens) to USD at the time of the transaction (if possible, use current prices as a reasonable approximation if historical prices are unavailable directly from the page). Consider both incoming and outgoing transactions.
- Classify the average transaction size into one of the following categories:
   - "Large":  Average transaction size > $100,000 USD
   - "Medium": Average transaction size between $10,000 and $100,000 USD (inclusive of $10,000, exclusive of $100,000)
   - "Small": Average transaction size < $10,000 USD

2. **Volume Analysis:**
- Calculate the total transaction volume in USD for the last 30 days. Sum the USD value of all transactions (both incoming and outgoing) within the timeframe.
- Estimate the current total wallet value in USD.  You can infer this from the balance shown on the Etherscan page or by summing the current USD value of holdings based on recent transactions.  Then calculate the percentage of the total 30-day transaction volume relative to this estimated total wallet value.
- Calculate the average daily transaction frequency. Count the total number of transactions in the last 30 days and divide by 30.

3. **Top Assets in Transactions:**
- Identify the top 3-5 most frequently transacted assets (ETH and ERC-20 tokens) within the last 30 days. Count transactions involving each distinct asset.
- For each of the top assets, analyze the transaction direction patterns. Classify the direction as:
   - 1. Asset 'A': X % of transactions are (incoming/outgoing/balanced).
   - 2. Asset 'B': X % of transactions are (incoming/outgoing/balanced).
   - 3. Asset 'C': X % of transactions are (incoming/outgoing/balanced).

4. ** Average Daily Transactions **
- Calculate the average daily transaction frequency. Count the total number of transactions in the last 30 days and divide by 30.

5. ** Percentage of Total Volume **
- For each of the top assets, calculate the percentage of the total 30-day transaction volume (in USD) that is attributed to transactions involving that asset.

6. ** Analysis **
- Provide a brief interpretation of the transaction patterns and trends. This should include a summary of the top assets in transactions, the average transaction size, and the average daily transaction frequency.

** Output Format **

Average Transaction Size: $X (Classification: [Size Category])
Total 30-Day Volume: $Y (X% of total wallet value)

Top Assets in Transactions:
1. Asset A: X% (Direction: [Pattern])
2. Asset B: Y% (Direction: [Pattern])
3. Asset C: Z% (Direction: [Pattern])

Average Daily Transactions: X
Analysis: [Interpretation of behavior]

"""

BEHAVIOR_PROMPT = """
Go to https://etherscan.io/address/{wallet_address}#transactions) to determine if the wallet is likely operated by a bot or a human.  Focus on the entire transaction history available on the page.

Objective: Analyze the transaction history of a given Ethereum wallet address using Etherscan to determine if the wallet is likely operated by a bot or a human. Finding transactions frequency patterns, clasifying (bot, human, uncertain ), confidence level (high, medium, low), key indicators (list key factors supporting classification, list any contradicting factors) and other relevant information.

** Instructions **

1. **Transaction Frequency Patterns:**
- Analyze the frequency of transactions over time. Are transactions clustered in bursts, evenly spaced, or sporadic?
- Calculate the average transaction frequency per day/hour over different periods (e.g., last 7 days, last 30 days, overall history).

2. **Response to Market Conditions (Infer from Transaction Timing and Asset Choice - Qualitative Assessment):**
- Examine if transaction timing seems correlated with typical market hours or if activity is consistent 24/7.
- Look for patterns suggesting rapid reactions to market events (if discernible from transaction timestamps and asset types traded, though this is challenging on Etherscan directly and may require external context).  For example, sudden bursts of activity around times of known market volatility (if such events can be inferred indirectly). *Acknowledge limitations here, as direct market data is not on Etherscan.*

3. **Fee Expenditure Patterns:**
- Analyze the gas prices used in transactions. Are they consistently similar, highly variable, or following a pattern (e.g., consistently using fast gas, or systematically adjusting gas)?
- Look for patterns in gas usage efficiency. Are transactions typically optimized for gas, or is gas expenditure less of a concern? (This is harder to assess directly from Etherscan, focus more on consistency and variability of gas prices used).

4. **Activity Consistency:**
- Assess the consistency of transaction activity levels over different timeframes (days, weeks, months if history is long enough). Is activity relatively stable or highly variable?
- Are there predictable periods of high and low activity, or is it more random?

5. **Time Patterns of Transactions:**
- Analyze the distribution of transactions across different hours of the day and days of the week.
- Are transactions concentrated during specific hours or days, or are they evenly distributed across all times?
- Look for patterns related to typical human activity hours (e.g., more activity during daytime hours in a specific timezone, less overnight) vs. 24/7 activity.

** Output Format **
Classification: [Bot/Human/Uncertain]
Confidence Level: [High/Medium/Low]
Key Indicators:
- [List key factors supporting classification]
- [List any contradicting factors]
Analysis: [Brief explanation of conclusion]
"""
