import re

def clean_text(text):
    # Remove page numbers that appear on a line by themselves (only digits)
    text = re.sub(r'(?m)^\s*\d+\s*$', '', text)
    
    # Format headers: convert lines with three or more '=' signs on both ends to a Markdown header
    text = re.sub(r'(?m)^={3,}\s*(.*?)\s*={3,}$', r'## \1', text)
    
    # Process each line individually to collapse extra spaces while preserving newlines
    lines = text.splitlines()
    clean_lines = [re.sub(r' +', ' ', line).strip() for line in lines if line.strip()]
    
    # Join the cleaned lines with newline characters
    return "\n".join(clean_lines)

def main():
    input_file = input("Enter the name of the input text file to clean (e.g., input.txt): ")
    output_file = input("Enter the desired name for the cleaned output file (e.g., cleaned.txt): ")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return

    # Clean the text
    cleaned_text = clean_text(raw_text)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    
    print(f"Data cleansing complete. Cleaned text saved to '{output_file}'.")

if __name__ == "__main__":
    main()

