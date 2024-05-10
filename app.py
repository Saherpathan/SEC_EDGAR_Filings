import streamlit as st
import os
import requests
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import matplotlib.pyplot as plt

# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load environment variables
load_dotenv()

# Load Google API key from environment variable
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Configure Google LLM API
import google.generativeai as genai
genai.configure(api_key=GOOGLE_API_KEY)

# Function to read text file
def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text_data = file.read()
    return text_data

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

# Function to generate visualizations
def visualize_data(insights):
    if insights:
        # Create a bar chart of top words
        words, frequencies = zip(*insights)
        plt.bar(words, frequencies)
        plt.xlabel("Words")
        plt.ylabel("Frequency")
        plt.title("Top Words in 10-K Filings")
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.write("No insights found.")

# Streamlit app
def main():
    st.title("10-K Filings Analysis App")
    st.write("Enter the company ticker below to analyze its 10-K filings:")

    # Input field for company ticker
    ticker = st.text_input("Company Ticker")

    # Button to trigger analysis
    if st.button("Analyze"):
        if ticker:
            directory_path = f"./sec-edgar-filings/{ticker}/10-K"
            insights = []
            for filename in os.listdir(directory_path):
                if filename.endswith(".txt"):
                    file_path = os.path.join(directory_path, filename)
                    text_data = read_text_file(file_path)
                    insights += text_analysis(text_data)

            # Generate visualizations
            visualize_data(insights)
        else:
            st.write("Please enter a valid company ticker.")

if __name__ == "__main__":
    main()
