# PDF_to_TXT
This code will take .pdf -> .png -> .txt ---> formatted.txt

- Takes a list of PDF files as input
- Converts each page of each PDF file into a PNG image using Wand Image library
- Extracts the text from each PNG image using the Pytesseract library
- Formats the extracted text by removing non-alphanumeric characters and extra spaces, splitting it into sentences, and adding start and end tags to each sentence
- Saves the formatted text for each page of each PDF file as a separate text file in a specified output directory
