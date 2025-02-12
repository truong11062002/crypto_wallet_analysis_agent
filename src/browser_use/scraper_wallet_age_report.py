import asyncio
import os
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContextConfig, BrowserContextWindowSize
from src.utils import utils
from prompts.prompt import WALLET_AGE

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 1. Wallet Addresses and Output Directory
wallet_addresses = open("wallet_addresses.txt", "r").read().splitlines()
output_directory = "etherscan_wallet_age"

# Create output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)


async def scrape_etherscan_wallet_age(wallet_address):
    """Scrapes Etherscan data for a single wallet address."""
    try:
        # 3. Configure LLM (adjust provider, model, temperature as needed)
        llm = utils.get_llm_model(
            provider="openai",
            model_name="gpt-4o",
            temperature=0.1,  # Lower temperature for more consistent results
            api_key=OPENAI_API_KEY,
        )

        # 4. Configure Browser and Context
        browser = Browser(
            config=BrowserConfig(
                headless=True,  # Run in headless mode for automation
                disable_security=True,  # Optional, but often helpful for scraping
            )
        )
        async with await browser.new_context(
            config=BrowserContextConfig(
                no_viewport=False,  # Keep viewport for full page screenshots if needed
                browser_window_size=BrowserContextWindowSize(
                    width=1920, height=1080
                ),  # Set window size
            )
        ) as browser_context:
            # 5. Create Agent and Run Task
            task_prompt = WALLET_AGE.format(wallet_address=wallet_address)
            agent = Agent(
                task=task_prompt,
                llm=llm,
                browser_context=browser_context,
            )
            history = await agent.run(max_steps=100)  # Adjust max_steps if needed

            # 6. Extract and Save Results
            final_result = history.final_result()
            errors = history.errors()

            output_file = os.path.join(
                output_directory, f"{wallet_address}_etherscan_data.txt"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(f"Wallet Address: {wallet_address}\n\n")
                f.write("--- Final Result ---\n")
                f.write(final_result if final_result else "No result extracted.\n")
                f.write("\n--- Errors ---\n")
                f.write(errors if errors else "No errors.\n")
                f.write("\n--- Model Actions ---\n")
                f.write(
                    str(history.model_actions())
                )  # Save model actions for debugging
                f.write("\n--- Model Thoughts ---\n")
                f.write(
                    str(history.model_thoughts())
                )  # Save model thoughts for debugging

            print(f"Data scraped and saved to: {output_file}")

    except Exception as e:
        error_message = f"Error scraping address {wallet_address}: {e}"
        print(error_message)
        error_file = os.path.join(output_directory, f"{wallet_address}_error.txt")
        with open(error_file, "w", encoding="utf-8") as f:
            f.write(error_message + "\n")
            import traceback

            f.write(traceback.format_exc())  # Save full traceback for debugging

    finally:
        if browser_context:  # Ensure browser context is closed even if errors occur
            await browser_context.close()
        if browser:  # Ensure browser is closed even if errors occur
            await browser.close()


async def main():
    """Main function to run scraping for all wallet addresses."""
    for address in wallet_addresses:
        print(f"Starting scraping for address: {address}")
        await scrape_etherscan_wallet_age(address)
        print(f"Finished scraping for address: {address}\n")
        await asyncio.sleep(
            2
        )  # Optional: Add a delay between requests to be nice to Etherscan


if __name__ == "__main__":
    asyncio.run(main())
