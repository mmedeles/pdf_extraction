import tkinter as tk
from tkinter import filedialog
import os

# Import the pdf extraction program (assuming the combined code is in a separate file)
from pdf_extract import process_pdf  # Adjust the import according to where the pdf_extraction function is stored


def select_pdf_file():
    # Create a Tkinter root window (it won't show)
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window

    # Open a file dialog to select the PDF file
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )

    # Check if a file was selected
    if file_path:
        # Get the current working directory
        current_directory = os.getcwd()

        # Ask the user to specify the output file path (the file will be saved in the current working directory)
        output_file = filedialog.asksaveasfilename(
            title="Save Output As",
            initialdir=current_directory,  # Set initial directory to the current working directory
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )

        # Check if the user selected a file to save
        if output_file:
            process_pdf(file_path, output_file)
            print(f"Extraction completed. Output saved to: {output_file}")
        else:
            print("No output file selected. Exiting.")
    else:
        print("No PDF file selected. Exiting.")


if __name__ == "__main__":
    select_pdf_file()
