import tkinter as tk
from tkinter import filedialog
import os
from pdf_extract import process_pdf

GREEN = '\033[32m'  # Green text for success
RED = '\033[31m'  # Red text for errors
RESET = '\033[0m'  # Reset to default color


def print_success(message):
    """Prints success messages in green"""
    print(f"{GREEN}{message}{RESET}")


def print_error(message):
    """Prints error messages in red"""
    print(f"{RED}{message}{RESET}")


def select_pdf_file():
    """Prompts the user to select a PDF file and a location to save the output."""
    # Tkinter root window (it won't show)
    root = tk.Tk()
    root.withdraw()  # Hide the Tkinter root window

    # Open file dialog to select the PDF file
    file_path = filedialog.askopenfilename(
        title="Select PDF File",
        filetypes=(("PDF Files", "*.pdf"), ("All Files", "*.*"))
    )

    # Checking if file was selected
    if file_path:
        # Get current working directory
        current_directory = os.getcwd()

        # Ask the user to specify the output file path (the file will be saved in the current working directory by default)
        output_file = filedialog.asksaveasfilename(
            title="Save Output As",
            initialdir=current_directory,  # default dir ==> current working directory
            defaultextension=".txt",
            filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
        )

        # Check if the user selected a file to save
        if output_file:
            try:
                # PDF extraction
                process_pdf(file_path, output_file)
                print_success(f"Extraction completed. Output saved to: {output_file}")
            except Exception as e:
                print_error(f"Error: {e}")
        else:
            print_error("No output file selected. Exiting.")
    else:
        print_error("No PDF file selected. Exiting.")


if __name__ == "__main__":
    select_pdf_file()
