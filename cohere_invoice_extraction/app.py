import streamlit as st
import os
from invoice_extraction import extract_text_from_pdf, extract_invoice_details_with_cohere, format_json_as_text, save_json_to_file
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Streamlit app
st.title("Invoice Data Extraction with Cohere")

# Load Cohere API key from environment variable
cohere_api_key = os.getenv("COHERE_API_KEY")

if not cohere_api_key:
    st.error("API Key not found. Please ensure it's set in the .env file.")

# File upload
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and cohere_api_key:

    with st.spinner('Extracting text from the PDF...'):
        text = extract_text_from_pdf(uploaded_file)

    # Extract details using Cohere API
    with st.spinner('Extracting invoice details using Cohere API...'):
        invoice_details = extract_invoice_details_with_cohere(text, cohere_api_key)

    # Save the JSON result to the 'output' folder
    output_filename = f'invoice_details_{uploaded_file.name}.json'
    save_json_to_file(invoice_details, output_filename)

    # Format the JSON data as readable text
    formatted_text = format_json_as_text(invoice_details)


    st.header("Extracted Invoice Details")
    st.markdown(formatted_text, unsafe_allow_html=True)

    st.success(f"Invoice details saved to {output_filename} and displayed successfully.")


if not os.path.exists('output'):
    os.makedirs('output')
