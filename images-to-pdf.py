#!/usr/bin/env python3

import os, sys

# importing third-party modules
try:
    from PIL import Image
    from PyPDF2 import PdfMerger, PdfReader
except ImportError:
    print(
        """##################################
    Dependencies are not installed, please install the dependencies by using
    
    'pip install -r requirements.txt'"""
    )

    sys.exit()


def convert_to_pdf(read_from, write_to):
    """converts an image to pdf

    Args:
        read_from (str): path of image file to be converted
        write_to (str): path where pdf is to be saved
    """

    # reading the image as binary
    image_file = Image.open(read_from)

    # converting to RGB if image in RGBA format
    if image_file.mode == "RGBA":
        image_file = image_file.convert("RGB")

    # saving the image as pdf
    image_file.save(write_to, "PDF")

    # closing the image file
    image_file.close()


def main():
    # Get the source directory
    if len(sys.argv) != 2:
        sys.exit("Please pass exactly one argument.")

    source_path = sys.argv[1]

    image_extensions = ("jpeg", "jpg", "png")  # tuple containing image file extensions

    # creating a PDF object which will have the final pdf
    combined_pdf_object = PdfMerger()

    for content in os.listdir(source_path):
        if os.path.isdir(content) or (content.split(".")[-1] not in image_extensions):
            continue
        content_path = os.path.join(source_path, content)
        # making a pdf off the current image
        iterable_pdf = "./iterable_pdf_to_be_deleted.pdf"
        convert_to_pdf(content_path, iterable_pdf)

        # adding this pdf to the PDF object
        combined_pdf_object.append(PdfReader(iterable_pdf))

    combined_pdf_object.write(
        os.path.join(source_path, "final.pdf")
    )  # writing the PDF object as a pdf file
    os.remove(iterable_pdf)  # removing the tempoarary pdf


if __name__ == "__main__":
    main()
