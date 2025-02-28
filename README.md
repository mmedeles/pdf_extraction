# PDF Extraction Application

This Python program extracts structured data from PDF documents and performs semantic analysis to prepare the data for use in UML diagram generation. The program supports extracting tables, text, URLs, and other key components, and outputs the results in a machine-readable text file.

## Features

- **PDF Extraction**: Extracts tables, URLs, and text from PDF documents.
- **Semantic Analysis**: Identifies and tags **Classes**, **Attributes**, **Methods**, and **Relationships** for UML diagram generation.
- **Save As Option**: Allows users to select a directory and change the output file name.
- **Automatic Directory Handling**: Saves the output in the directory where the script is executed.

## Requirements

- Python 3.x
- `tkinter` for file dialogs (installed by default in most Python installations).
- `pdfplumber` for extracting tables from PDFs.
- `PyMuPDF (fitz)` for handling the layout and text extraction from PDFs.

You can install the required Python libraries using `pip`:

```bash
pip install pdfplumber PyMuPDF
```



## How to Use

1. Clone or download the repository.
2. Install the required dependencies (listed above).
3. Run the program:

   ```bash
   python main.py
   ```
4. Select the PDF to be extracted when prompted
5. Save the Output file 
   
```
The output file will contain sections such as:

EXTRACTED TEXT: All the text extracted from the PDF.
EXTRACTED URLS: All the URLs found within the document.
EXTRACTED TABLES: All tables, including attributes and their values.
CLASSES: Identified classes for UML.
ATTRIBUTES: Identified attributes for UML.
METHODS: Identified methods/functions.
RELATIONSHIPS: Identified relationships between components.
```

# To Do (Improve):
1. Clean text extract inconsistencies
   1. Adobe Pro
   2. Word
   3. Standard Text Editor
      1. Pre-process to the extraction
2. Warning/Caution bubbles??
   1. Identify
   2. Format?
   3. Output
   4. Semantic Analyzing??
3. How should the output look like to be fed into the pipeline