import nltk
# Download the required tokenizer models (run once)
nltk.download('punkt','punkt_tab') 
'''
If system is not successfully downloading 'punkt_tab', please download it manually 
via python shell to your local nltk directory such as "~/nltk_data/tokenizers/"

'''
from nltk.tokenize import word_tokenize, sent_tokenize

def tokenize_text(text):
    '''
    Tokenizes text into sentences and words.
    
    :param text: The input text string.
    :return: A tuple of (sentences, words)
    '''
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    return sentences, words

def main():
    # Prompt user for input and output file names
    input_file = input("Enter the name of the input file to tokenize (e.g., cleaned.txt): ")
    output_file = input("Enter the name for the output tokens file (e.g., tokens.txt): ")

    try:
        with open(input_file, "r", encoding="utf-8") as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
        return

    # Tokenize the text
    sentences, words = tokenize_text(text)

    # Write the tokens to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("Tokenized Sentences:\n")
        for sentence in sentences:
            f.write(sentence + "\n")
        f.write("\nTokenized Words:\n")
        f.write(" ".join(words))
    
    print(f"Tokenization complete. Tokens saved to '{output_file}'.")

if __name__ == "__main__":
    main()

