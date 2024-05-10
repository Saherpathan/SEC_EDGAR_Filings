import os
import requests
import nltk
from dotenv import load_dotenv
import google.generativeai as genai
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

# Load environment variables from .env file
load_dotenv()

# Load Google API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Google LLM API
genai.configure(api_key=GOOGLE_API_KEY)

# Function to perform text analysis
def text_analysis(data):
    # Tokenize text
    tokens = word_tokenize(data)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Calculate word frequencies
    freq_dist = FreqDist(filtered_tokens)
    top_words = freq_dist.most_common(10)  # Get top 10 words

    return top_words

# Function to visualize data
def visualize_data(insights):
    # Create a bar chart of top words
    words, frequencies = zip(*insights)
    plt.bar(words, frequencies)
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Top Words in 10-K Filings")
    plt.savefig('fig.png')

# Define function to analyze 10-K filings using LLM API
def analyze_10k_filings(filing_texts):
    insights = []

    for text in filing_texts:
        # Perform LLM inference on each 10-K filing
        analysis_result = genai.analyze(text)

        # Extract relevant insights from the analysis result
        # For simplicity, let's extract the top entities mentioned in the text
        top_entities = analysis_result.get('entities', [])[:0]
        insights.append(top_entities)

    return insights

# Function to download 10-K filings for a given company
def download_10k_filings(company_ticker):
    # Define SEC EDGAR URL for the company
    base_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={company_ticker}&type=10-K"

    # Make a GET request to the SEC EDGAR website
    response = requests.get(base_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract filing URLs from the response (you may need to parse the HTML)
        filing_urls = [...]  # Placeholder for actual parsing of filing URLs

        # Download filing texts from the extracted URLs
        filing_texts = []
        for url in filing_urls:
            filing_text = download_filing_text(url)
            filing_texts.append(filing_text)

        return filing_texts
    else:
        print("Error:", response.status_code)
        return []

# Function to download filing text from a given URL
def download_filing_text(url):
    # Make a GET request to the filing URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract text from the response (you may need to parse the HTML)
        filing_text = response.text  # Placeholder for actual text extraction
        return filing_text
    else:
        print("Error:", response.status_code)
        return ""

# Main function
def main():
    # Define the company ticker
    company_ticker = "AAPL"

    # Download 10-K filings for the given company
    filing_texts = download_10k_filings(company_ticker)

    # Analyze 10-K filings using LLM API
    insights = analyze_10k_filings(filing_texts)

    # Generate visualizations from insights
    visualize_data(insights)

if __name__ == "__main__":
    main()
