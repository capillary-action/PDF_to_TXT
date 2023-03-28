from PIL import Image as PILImage
import pytesseract
from wand.image import Image as WandImage
import re
import os

# Set the path to the PDF directory
pdf_dir = "pdf/"

# Set the path to the image output directory
img_output_dir = "output_images/"

# Set the path to the text output directory
text_output_dir = "output_text/"

# Create the image output directory if it doesn't already exist
if not os.path.exists(img_output_dir):
    os.makedirs(img_output_dir)

# Create the text output directory if it doesn't already exist
if not os.path.exists(text_output_dir):
    os.makedirs(text_output_dir)

# Get a list of all PDF files in the directory
pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith(".pdf")]

for pdf_file in pdf_files:

    # Open the PDF file
    with WandImage(filename=os.path.join(pdf_dir, pdf_file), resolution=300) as img:

        # Convert each page of the PDF to a JPG image
        with img.convert('jpg') as converted:

            # Save each page as a separate JPG image
            for i, page in enumerate(converted.sequence):
                with WandImage(page) as single_page:
                    img_filename = f'{pdf_file[:-4]}_page_{i}.png'
                    img_path = os.path.join(img_output_dir, img_filename)
                    single_page.save(filename=img_path)

                    # Load the saved PNG image
                    img = PILImage.open(img_path)

                    # Convert the image to text using pytesseract
                    text = pytesseract.image_to_string(img, lang='eng')

                    # Format the extracted text for training with the Stanford Alpaca 7B model
                    formatted_text = ""

                    # Remove any non-alphanumeric characters and extra spaces
                    text = re.sub(r'[^\w\s]', '', text)
                    text = re.sub(r'\s+', ' ', text)

                    # Split the text into sentences and add tags to each sentence
                    sentences = text.split('.')
                    for sentence in sentences:
                        if sentence.strip():
                            formatted_text += "<S> " + sentence.strip() + " </S>\n"

                    # Save the formatted text to a text file
                    text_filename = f'{pdf_file[:-4]}_page_{i}.txt'
                    text_path = os.path.join(text_output_dir, text_filename)
                    with open(text_path, mode='w') as file:
                        file.write(formatted_text)
