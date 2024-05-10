from sec_edgar_downloader import Downloader
import os


def download_10k_filings(companies):
    # Initialize downloader
    dl = Downloader(company_name="Company Name", email_address="email@example.com")

    for company in companies:
        # Define the directory to save the filings
        save_dir = f"./{company}_10k_filings"


        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        # Download filings for each year from 1995 through 2023
        for year in range(1995, 2024):
            try:
                dl.get("10-K", company)
                print(f"Downloaded 10-K filing for {company} for the year {year}")
            except Exception as e:
                print(f"Failed to download filing for {company} for the year {year}: {e}")


if __name__ == "__main__":
    companies = ["AAPL", "GOOGL", "MSFT"]  # Example companies
    download_10k_filings(companies)
