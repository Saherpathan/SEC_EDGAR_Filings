# SEC 10-K Filings Data

This Python script lets you download SEC 10-K filings for specified companies from the SEC website using the `sec-edgar-downloader` package.

## Requirements

- Python 3.x
- `sec-edgar-downloader` package (install using `pip install sec-edgar-downloader`)
- LLM API Key



## Task 1.1: Fetch the data

1. Clone this repository to your local machine using
    ```bash
    git clone https://github.com/Saherpathan/FinTech.git

3. Open a terminal or command prompt and navigate to the directory containing the script.

4. Run the script using:
   ```bash
   python fetch_data.py

## Notes

- Please ensure you have proper permissions and internet connectivity to access the SEC website for downloading filings.
- Make sure to handle any errors during the download process.
- You can customize the list of companies/tickers and the time range as per the requirement.


## Task 1.2: Text Analysis

- Used LLM API from `google-generativeai` to perform text analysis on the downloaded 10-K filings.
- Conducted natural language processing tasks such as tokenization, stop words removal, and frequency distribution calculation using `nltk`.
- Generated visualizations using `matplotlib`.
  

## Task 2: Construct and Deploy Simple App

- Created a simple app using `streamlit` that takes a company ticker as input and displays relevant visualizations.
- `streamlit` was chosen for its simplicity and ease of hosting web apps, allowing for quick deployment.
- Run the application using:
  ```bash
   streamlit run app.py
