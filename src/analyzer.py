import os
from pathlib import Path
from typing import Dict, List

from agno.agent import Agent
from agno.models.openai import OpenAIChat

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class EthereumWalletAnalyzer:
    def __init__(self, data_dir: str = "src/web-ui/etherscan_data"):
        self.data_dir = Path(data_dir)

        # Initialize the agent with specific instructions for analyzing wallet data
        # TODO: Agent that uses structured outputs
        self.agent = Agent(
            model=OpenAIChat(id="gpt-4o"),
            description="You are a cryptocurrency wallet analysis expert that specializes in interpreting and formatting wallet data.",
            instructions=[
                "Extract and format wallet data into clear sections:",
                "1. Complete list of all cryptocurrency tokens held",
                "2. Current USD value of each token",
                "3. Total portfolio value in USD",
                "4. Percentage distribution of assets",
                "Format numbers with appropriate decimal places and include symbols ($, %, etc)",
                "Sort token lists by USD value in descending order",
            ],
            markdown=True,
        )

        # TODO: Agent that uses structured outputs to improve quality
        self.agent_wallet_age = Agent(
            model=OpenAIChat(id="gpt-4o"),
            description="You are a cryptocurrency wallet analysis expert that specializes in interpreting and formatting wallet data.",
            instructions=[
                "Extract and format wallet data into clear sections:",
                "First Transaction: YYYY-MM-DD",
                "Wallet Age: X years, Y months, Z days",
                "Category: [Category]",
                "Analysis: [Brief interpretation]",
                "Make sure all numbers are properly formatted with appropriate decimals.",
            ],
        )
        self.agent_trend = Agent(
            model=OpenAIChat(id="gpt-4o"),
            description="You are a cryptocurrency wallet analysis expert that specializes in interpreting and formatting wallet data.",
            instructions=[
                "Extract and format wallet data into clear sections:",
                "30-Day Trend:",
                "- Overall change: [increase/decrease/stable]",
                "- Notable changes: [List significant changes]",
                "90-Day Trend:",
                "- Overall change: [increase/decrease/stable]",
                "- Notable changes: [List significant changes]",
                "180-Day Trend:",
                "- Overall change: [increase/decrease/stable]",
                "- Notable changes: [List significant changes]",
                "Conclusion: [Interpretation of holder's strategy]",
                "Make sure all numbers are properly formatted with appropriate decimals.",
            ],
        )

    def read_wallet_data(self, file_path: Path) -> str:
        """Read wallet data from a text file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return ""

    def get_wallet_files(self) -> List[Path]:
        """Get list of all wallet data files."""
        return [
            f for f in self.data_dir.glob("*.txt") if not f.name.endswith("_error.txt")
        ]

    def analyze_single_wallet(self, wallet_data: str) -> str:
        """Analyze data for a single wallet using the agent."""
        prompt = f"""
        Analyze this wallet data and format it into sections:

        {wallet_data}

        Format the output with these exact sections:
        1. Token Holdings
        2. USD Values
        3. Total Portfolio Value
        4. Asset Distribution

        Make sure all numbers are properly formatted with appropriate decimals.
        Sort tokens by USD value from highest to lowest.
        """

        response = self.agent.run(prompt)
        return response.content if response.content else "No analysis available"

    def analyze_wallets_age(self, wallet_address: str) -> str:
        """Analyze wallet age using the agent."""
        prompt = f"""
        Analyze the wallet age of {wallet_address} using the following information:

        First Transaction: YYYY-MM-DD
        Wallet Age: X years, Y months, Z days
        Category: [Category]
        Analysis: [Brief interpretation]

        Make sure all numbers are properly formatted with appropriate decimals.
        """

        response = self.agent_wallet_age.run(prompt)
        return response.content if response.content else "No analysis available"

    def analyze_wallets_trend(self, wallet_address: str) -> str:
        """Analyze wallet trend using the agent."""
        prompt = f"""
        Analyze the trend of {wallet_address} using the following information:
        30-Day Trend:
        - Overall change: [increase/decrease/stable]
        - Notable changes: [List significant changes]

        90-Day Trend:
        - Overall change: [increase/decrease/stable]
        - Notable changes: [List significant changes]

        180-Day Trend:
        - Overall change: [increase/decrease/stable]
        - Notable changes: [List significant changes]

        Conclusion: [Interpretation of holder's strategy]
        Make sure all numbers are properly formatted with appropriate decimals.
        """
        response = self.agent_trend.run(prompt)
        return response.content if response.content else "No analysis available"

    def analyze_all_wallets(self) -> Dict[str, str]:
        """Analyze all wallet files in the data directory."""
        results = {}

        for file_path in self.get_wallet_files():
            wallet_address = file_path.stem.split("_")[0]
            wallet_data = self.read_wallet_data(file_path)

            if wallet_data:
                print(f"Analyzing wallet: {wallet_address}")
                analysis = self.analyze_single_wallet(wallet_data)
                results[wallet_address] = analysis
            else:
                print(f"No data found for wallet: {wallet_address}")

        return results

    def save_analysis(
        self, results: Dict[str, str], output_dir: str = "analysis_results"
    ):
        """Save analysis results to files."""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save individual wallet analyses
        for wallet_address, analysis in results.items():
            file_path = output_path / f"{wallet_address}_analysis.md"
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Analysis for {wallet_address}\n\n")
                f.write(analysis)

        # Create summary file
        summary_path = output_path / "summary.md"
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("# Wallet Analysis Summary\n\n")
            for wallet_address, analysis in results.items():
                f.write(f"## {wallet_address}\n\n")
                f.write(analysis)
                f.write("\n---\n\n")


if __name__ == "__main__":
    # Example usage
    analyzer = EthereumWalletAnalyzer()
    results = analyzer.analyze_all_wallets()
    analyzer.save_analysis(results)
