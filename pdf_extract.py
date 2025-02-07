"""
Extracting Text and Tables:

The program extracts general text and tables from the PDF. The tables are particularly important for extracting configuration parameters (e.g., emEndpoints, logDir) that are likely to be attributes in UML.
Semantic Tagging:

Classes: The program uses a regex pattern to detect class names (e.g., class LVCTransmogrifier).
Attributes: Configuration data from tables is identified as attributes (e.g., emEndpoints = ${COMPUTERNAM E}:55100).
Methods: Certain patterns like start.bat or install() are identified as methods.
Relationships: Relationships between components (e.g., LVC Entity => Platform) are detected as associations or dependencies in UML.
Formatted Output:

The program writes the extracted and tagged information into a TXT file, which clearly identifies classes, attributes, methods, and relationships. This is ready to be used by the UML generation pipeline.


Next Steps:
Enhance NLP Processing: For more advanced semantic understanding, consider integrating an NLP library to better understand context and relationships within the text.
"""
import fitz  # PyMuPDF
import pdfplumber
import re

# Extract text from the PDF using PyMuPDF (fitz)
def extract_text_using_pymupdf(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text("text")

    return full_text

# Extract tables using PDF Plumber
def extract_tables_using_pdfplumber(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_tables.append(table)

    return all_tables

# Extract URLs from the document
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

# Semantic tagging of the extracted content
def semantic_tagging(text, tables):
    classes = []
    relationships = []
    methods = []
    attributes = []

    # Detect and tag classes (based on certain keywords or patterns)
    class_pattern = r'(class\s+[\w]+)'  # Example pattern for class names
    classes = re.findall(class_pattern, text)

    # Tag attributes (e.g., emEndpoints, listenEndpoints from the config tables)
    for table in tables:
        for row in table:
            if len(row) >= 2 and row[0].isidentifier():  # Check if it's a valid attribute
                attributes.append({"name": row[0], "value": row[1]})

    # Detect methods or commands (e.g., start.bat, installation commands)
    method_pattern = r'(start\.[a-z]+|install\([^\)]*\))'  # Example for methods or function names
    methods = re.findall(method_pattern, text)

    # Detect relationships (Associations, Dependencies, etc.)
    # This can be a more complex process that would need further NLP processing or keyword-based detection
    relationship_pattern = r'(\w+)\s*=>\s*(\w+)'  # Example pattern for relationships like "Entity => Platform"
    relationships = re.findall(relationship_pattern, text)

    return {
        "classes": classes,
        "attributes": attributes,
        "methods": methods,
        "relationships": relationships
    }

# Write the output to a structured TXT file for UML diagram generation
def write_output_to_txt(output_data, output_file):
    with open(output_file, 'w') as file:
        # Write general text
        file.write("=== EXTRACTED TEXT ===\n")
        file.write(output_data["text"])
        file.write("\n" + "="*40 + "\n")

        # Write extracted URLs
        file.write("=== EXTRACTED URLS ===\n")
        for url in output_data["urls"]:
            file.write(url + "\n")
        file.write("\n" + "="*40 + "\n")

        # Write extracted tables
        file.write("=== EXTRACTED TABLES ===\n")
        for table in output_data["tables"]:
            file.write("Table:\n")
            for row in table:
                file.write(", ".join(row) + "\n")
            file.write("\n" + "="*40 + "\n")

        # Write semantic analysis: Classes, Attributes, Methods, and Relationships
        file.write("=== CLASSES ===\n")
        for cls in output_data["classes"]:
            file.write(f"Class: {cls}\n")
        file.write("\n" + "="*40 + "\n")

        file.write("=== ATTRIBUTES ===\n")
        for attr in output_data["attributes"]:
            file.write(f"Attribute: {attr['name']} = {attr['value']}\n")
        file.write("\n" + "="*40 + "\n")

        file.write("=== METHODS ===\n")
        for method in output_data["methods"]:
            file.write(f"Method: {method}\n")
        file.write("\n" + "="*40 + "\n")

        file.write("=== RELATIONSHIPS ===\n")
        for relationship in output_data["relationships"]:
            file.write(f"Relationship: {relationship[0]} => {relationship[1]}\n")
        file.write("\n" + "="*40 + "\n")

# Main function to process the PDF and output structured data for UML diagrams
def process_pdf(pdf_path, output_file):
    # Extract general text, tables, and URLs
    text = extract_text_using_pymupdf(pdf_path)
    tables = extract_tables_using_pdfplumber(pdf_path)
    urls = extract_urls(pdf_path)

    # Perform semantic tagging
    tagged_data = semantic_tagging(text, tables)

    # Combine all extracted and tagged data
    output_data = {
        "text": text,
        "tables": tables,
        "urls": urls,
        "classes": tagged_data["classes"],
        "attributes": tagged_data["attributes"],
        "methods": tagged_data["methods"],
        "relationships": tagged_data["relationships"]
    }

    # Write the structured output to a TXT file
    write_output_to_txt(output_data, output_file)

# Sample run
pdf_path = "F:/Transmogrifier/Apps-LVCTransmogrifierUserGuide-v1.2.0.pdf"
output_file = "structured_output_for_uml.txt"
process_pdf(pdf_path, output_file)