import asyncio
from pathlib import Path
from typing import List

from src.analyzer import EthereumWalletAnalyzer


async def read_wallet_addresses(file_path: str) -> List[str]:
    """Read wallet addresses from a file."""
    try:
        with open(file_path) as f:
            return [addr.strip() for addr in f.readlines() if addr.strip()]
    except FileNotFoundError:
        print(f"Error: Wallet addresses file not found at {file_path}")
        return []
    except Exception as e:
        print(f"Error reading wallet addresses: {e}")
        return []


async def analyze_wallets(
    addresses: List[str],
    output_dir: str = "data/wallet_analysis",
    analyze_age: bool = False,
    analyze_trend: bool = False,
):
    """Analyze multiple wallet addresses."""

    # Initialize analyzer
    data_dir = {
        (True, False): "src/browser_use/etherscan_wallet_age",
        (False, True): "src/browser_use/etherscan_wallet_trend",
        (False, False): "src/browser_use/etherscan_data",
    }.get((analyze_age, analyze_trend), "src/browser_use/etherscan_data")

    analyzer = EthereumWalletAnalyzer(data_dir=data_dir)

    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Process each wallet address
    results = {}
    for address in addresses:
        try:
            print(f"\nAnalyzing wallet: {address}")

            # Get analysis for this wallet
            data_file = Path(f"{data_dir}/{address}_etherscan_data.txt")
            data = analyzer.read_wallet_data(data_file)
            if data:
                match (analyze_age, analyze_trend):
                    case (True, False):
                        analysis = analyzer.analyze_wallets_age(data)
                    case (False, True):
                        analysis = analyzer.analyze_wallets_trend(data)
                    case (False, False):
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
    analyze_age = False
    analyze_trend = True
    WALLET_FILE = "src/browser_use/wallet_addresses.txt"
    OUTPUT_DIR = {
        (True, False): "data/wallet_age_analysis",
        (False, True): "data/wallet_trend_analysis",
        (False, False): "data/wallet_analysis",
    }.get((analyze_age, analyze_trend), "data/wallet_analysis")

    print("Starting Ethereum Wallet Analysis...")

    # Read wallet addresses
    addresses = await read_wallet_addresses(WALLET_FILE)
    if not addresses:
        print("No wallet addresses found. Exiting.")
        return

    print(f"Found {len(addresses)} wallet addresses to analyze")

    # Run analysis
    await analyze_wallets(
        addresses, OUTPUT_DIR, analyze_age=analyze_age, analyze_trend=analyze_trend
    )

    print("\nAnalysis complete!")


if __name__ == "__main__":
    asyncio.run(main())
