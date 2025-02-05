import fitz  # PyMuPDF
import pdfplumber
import re


def extract_text_using_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text("text")

    return full_text


def extract_tables_using_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_tables.append(table)

    return all_tables


def extract_urls(pdf_path):
    doc = fitz.open(pdf_path)
    urls = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        links = page.get_links()
        for link in links:
            if link.get("uri"):
                urls.append(link["uri"])
    return urls


def write_output_to_txt(output_data, output_file):
    with open(output_file, 'w') as file:
        # Write text content
        file.write("=== EXTRACTED TEXT ===\n")
        file.write(output_data["text"])
        file.write("\n\n")

        # Write extracted URLs
        file.write("=== EXTRACTED URLS ===\n")
        for url in output_data["urls"]:
            file.write(url + "\n")
        file.write("\n")

        # Write extracted tables
        file.write("=== EXTRACTED TABLES ===\n")
        for table in output_data["tables"]:
            file.write("Table:\n")
            for row in table:
                file.write(", ".join(row) + "\n")
            file.write("\n")


# Main Function to process the PDF and output to TXT
def process_pdf(pdf_path, output_file):
    # Extract general text
    text = extract_text_using_pymupdf(pdf_path)

    # Extract tables
    tables = extract_tables_using_pdfplumber(pdf_path)

    # Extract URLs
    urls = extract_urls(pdf_path)

    # Output the structured data in dictionary format
    output_data = {
        "text": text,
        "tables": tables,
        "urls": urls
    }

    # Write the output data to a text file
    write_output_to_txt(output_data, output_file)


# Sample run
pdf_path = "F:/Transmogrifier/Apps-LVCTransmogrifierUserGuide-v1.2.0.pdf"
output_file = "extracted_data.txt"
process_pdf(pdf_path, output_file)
