#!/usr/bin/env python3

import argparse
import os
import sys
import traceback

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

    traceback.print_exc()
    sys.exit()


def _get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--source_dir",
        required=True,
        dest="source_dir",
        help="Path of the source directory where the images are present",
    )

    parser.add_argument(
        "-d",
        "--dest_path",
        dest="dest_path",
        help=(
            "Path of the directory where the pdf is to be dumped. "
            "Default is $SOURCE_DIR/final.pdf. "
            "E.g. /u/username/images-to-pdf/screenshots.pdf."
        ),
    )

    args = parser.parse_args()
    args = _postprocess_args(args)
    return args


def _postprocess_args(args):
    args.source_dir = os.path.abspath(args.source_dir)

    if not args.dest_path:
        args.dest_path = os.path.join(args.source_dir, "final.pdf")

    return args


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
    args = _get_args()

    # Get the source directory
    source_path = args.source_dir
    dest_path = args.dest_path

    # tuple containing image file extensions
    image_extensions = ("jpeg", "jpg", "png")

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

    # writing the PDF object as a pdf file
    combined_pdf_object.write(os.path.join(dest_path))
    os.remove(iterable_pdf)  # removing the tempoarary pdf


if __name__ == "__main__":
    main()
