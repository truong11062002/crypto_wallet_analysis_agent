import asyncio
import os
from pathlib import Path
from typing import List

from src.analyzer import EthereumWalletAnalyzer


async def read_wallet_addresses(file_path: str) -> List[str]:
    """Read wallet addresses from a file."""
    try:
        with open(file_path, "r") as f:
            return [addr.strip() for addr in f.readlines() if addr.strip()]
    except FileNotFoundError:
        print(f"Error: Wallet addresses file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading wallet addresses: {e}")
        return []


async def analyze_wallets(
    addresses: List[str], output_dir: str = "data/wallet_analysis"
):
    """Analyze multiple wallet addresses."""

    # Initialize analyzer
    analyzer = EthereumWalletAnalyzer(data_dir="src/web-ui/etherscan_data")

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process each wallet address
    results = {}
    for address in addresses:
        try:
            print(f"\nAnalyzing wallet: {address}")

            # Get analysis for this wallet
            data = analyzer.read_wallet_data(
                Path(f"src/web-ui/etherscan_data/{address}_etherscan_data.txt")
            )
            if data:
                analysis = analyzer.analyze_single_wallet(data)
                results[address] = analysis
                print(f"Analysis complete for {address}")
            else:
                print(f"No data found for wallet {address}")

            # Be nice to APIs
            await asyncio.sleep(2)

        except Exception as e:
            print(f"Error analyzing wallet {address}: {str(e)}")
            continue

    # Save all results
    try:
        analyzer.save_analysis(results, output_dir)
        print(f"\nAnalyses saved to {output_dir}")
    except Exception as e:
        print(f"Error saving analyses: {str(e)}")


async def main():
    """Main entry point for the wallet analysis program."""

    # Configuration
    WALLET_FILE = "src/web-ui/wallet_addresses.txt"
    OUTPUT_DIR = "data/wallet_analysis"

    print("Starting Ethereum Wallet Analysis...")

    # Read wallet addresses
    addresses = await read_wallet_addresses(WALLET_FILE)
    if not addresses:
        print("No wallet addresses found. Exiting.")
        return

    print(f"Found {len(addresses)} wallet addresses to analyze")

    # Run analysis
    await analyze_wallets(addresses, OUTPUT_DIR)

    print("\nAnalysis complete!")


if __name__ == "__main__":
    asyncio.run(main())
