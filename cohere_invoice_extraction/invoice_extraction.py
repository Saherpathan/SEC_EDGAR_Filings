import pdfplumber
import cohere
from dotenv import load_dotenv
import os
import json
import re

# Load environment variables from .env file
load_dotenv()

# Function to extract text from PDF using pdfplumber
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to use Cohere API for text extraction
def extract_invoice_details_with_cohere(text, cohere_api_key):
    co = cohere.Client(cohere_api_key)
    prompt = f"""
    Extract the following details from the given text:

    1. Customer Name
    2. Customer Address
    3. Customer Phone No
    4. Customer Email ID
    5. Products (Name, HSN, Quantity, Amount). Ensure that percentages or extra details are not included in the product names.
    6. Total Amount

    Text:
    {text}

    Please provide the details in the following JSON format without any extra characters:

    {{
        "Customer Name": "value",
        "Customer Address": "value",
        "Customer Phone No": "value",
        "Customer Email ID": "value",
        "Products": [
            {{"Name": "value", "HSN": "value", "Quantity": "value", "Amount": "value"}},
            ...
        ],
        "Total Amount": "value"
    }}
    """
    response = co.generate(
        model='command-xlarge-nightly',
        prompt=prompt,
        max_tokens=300,
        temperature=0.5,
    )

    response_text = response.generations[0].text
    try:
        json_result = json.loads(response_text)
    except json.JSONDecodeError:
        # Clean and extract JSON
        json_string = re.search(r'\{.*\}', response_text, re.DOTALL).group(0)
        json_result = json.loads(json_string)

    return json_result

# Function to clean product names
def clean_product_name(name):
    cleaned_name = re.sub(r'\s*\(\d+%\)', '', name).strip()
    return cleaned_name

# Function to format JSON data as readable text
def format_json_as_text(json_data):
    customer_name = json_data.get('Customer Name', 'N/A')
    customer_address = json_data.get('Customer Address', 'N/A')
    customer_phone = json_data.get('Customer Phone No', 'N/A')
    customer_email = json_data.get('Customer Email ID', 'N/A')
    total_amount = json_data.get('Total Amount', 'N/A')

    products = json_data.get('Products', [])

    formatted_text = (
        f"<h2 style='font-size: 24px;'>Customer Details</h2>"
        f"<p><strong>Name:</strong> {customer_name}</p>"
        f"<p><strong>Address:</strong> {customer_address}</p>"
        f"<p><strong>Phone No:</strong> {customer_phone}</p>"
        f"<p><strong>Email ID:</strong> {customer_email}</p>"
    )

    if products:
        formatted_text += "<h2 style='font-size: 24px;'>Product Details</h2>"
        for product in products:
            name = product.get('Name', 'N/A')
            hsn = product.get('HSN', 'N/A')
            quantity = product.get('Quantity', 'N/A')
            amount = product.get('Amount', 'N/A')

            formatted_text += (
                f"<p><strong>Product Name:</strong> {name}</p>"
                f"<p><strong>HSN:</strong> {hsn}</p>"
                f"<p><strong>Quantity:</strong> {quantity}</p>"
                f"<p><strong>Amount:</strong> {amount}</p>"
            )
    else:
        formatted_text += "<p>No products found.</p>"

    formatted_text += (
        f"<h2 style='font-size: 24px;'>Total Amount</h2>"
        f"<p><strong>Total Amount in INR:</strong> {total_amount}</p>"
    )

    return formatted_text



# Function to save JSON result to file
def save_json_to_file(json_data, filename):
    output_path = os.path.join('output', filename)
    with open(output_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)
