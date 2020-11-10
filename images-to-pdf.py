from PIL import Image
from PyPDF2 import PdfFileMerger, PdfFileReader
import os, sys

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
    image_extensions = ("jpeg", "jpg", "png")   # tuple containing image file extensions

    # creating a PDF object which will have the final pdf
    combined_pdf_object = PdfFileMerger()

    for content in os.listdir():
        if os.path.isdir(content) or (content.split(".")[-1] not in image_extensions):
            continue
        
        # making a pdf off the current image
        iterable_pdf = "./iterable_pdf_to_be_deleted.pdf"
        convert_to_pdf(content, iterable_pdf)

        # adding this pdf to the PDF object
        combined_pdf_object.append(PdfFileReader(iterable_pdf))
    
    combined_pdf_object.write("./final.pdf")        # writing the PDF object as a pdf file
    os.remove(iterable_pdf)     # removing the tempoarary pdf


if __name__ == "__main__":
    main()