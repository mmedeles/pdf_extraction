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


"""

import fitz  # PyMuPDF
import pdfplumber
import re

def extract_text_using_pymupdf(pdf_path):
    """Extract txt and other elements (fitz)"""
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        full_text += page.get_text("text")

    return full_text

def extract_tables_using_pdfplumber(pdf_path):
    """Extract tables (plumber)"""
    with pdfplumber.open(pdf_path) as pdf:
        all_tables = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                all_tables.append(table)

    return all_tables

def extract_urls(pdf_path):
    """Extract URLs"""
    doc = fitz.open(pdf_path)
    urls = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        links = page.get_links()
        for link in links:
            if link.get("uri"):
                urls.append(link["uri"])
    return urls

def semantic_tagging(text, tables):
    """Semantic Tagging from the extracted content"""
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

def write_output_to_txt(output_data, output_file):
    """Write output to a TXT File"""
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

def process_pdf(pdf_path, output_file):
    """process the PDF and output structured data for UML diagrams"""
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

    #Write the structured output to a TXT file
    write_output_to_txt(output_data, output_file)