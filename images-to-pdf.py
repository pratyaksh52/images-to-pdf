#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from typing import List

from PIL import Image
from PyPDF2 import PdfMerger, PdfReader

# tuple containing image file extensions
IMAGE_EXTENSIONS = (".jpeg", ".jpg", ".png")


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
        type=Path,
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
    args.source_dir = Path(os.path.abspath(args.source_dir))

    if not args.source_dir.exists():
        raise FileNotFoundError("Source path does not exist")

    if not args.dest_path:
        args.dest_path = Path(args.source_dir, "final.pdf")
    elif args.dest_path.is_dir():
        raise ValueError("Please pass full dest path including filename")
    else:
        args.dest_path = Path(os.path.abspath(args.dest_path))

    if not args.dest_path.parent.exists():
        os.makedirs(args.dest_path.parent, exist_ok=True)
        print(f"Creating {args.dest_path.parent} as it does not exist")

    return args


def filter_images_from_filepath(path: Path) -> List[Path]:
    """Filter out all files from a path that is not an image

    Args:
        path (List[Path]): Path where the filtering needs to be done.

    Returns:
        List[Path: List of pathlib objects containing image paths
    """
    images_filepath = []
    for x in path.iterdir():
        if x.is_dir() or x.suffix not in IMAGE_EXTENSIONS:
            continue
        images_filepath.append(x)
    return sorted(images_filepath)


def convert_image_to_pdf(read_from: Path, write_to: Path):
    """Converts an image to pdf.

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


def convert_images_to_pdf(image_path_list: List[Path]) -> PdfMerger:
    """Converts a list of image paths to a single PdfMerger object

    Args:
        image_path_list (List[Path]): List of Path objects of images

    Returns:
        PdfMerger: Object containing all images
    """
    # creating a PDF object which will have the final pdf
    combined_pdf_object = PdfMerger()
    iterable_pdf_path = Path(image_path_list[0].parent, "./iterable_pdf_to_be_deleted.pdf")
    for image_path in image_path_list:
        # making a pdf off the current image
        convert_image_to_pdf(image_path, iterable_pdf_path)

        # adding this pdf to the PDF object
        combined_pdf_object.append(PdfReader(iterable_pdf_path))

    os.remove(iterable_pdf_path)
    return combined_pdf_object


def main():
    args = _get_args()

    # Get the source directory
    source_path = args.source_dir
    dest_path = args.dest_path

    print(f"Converting {source_path} to {dest_path}")
    image_paths = filter_images_from_filepath(source_path)

    if len(image_paths) == 0:
        print(f"No images found at {source_path}")
        return

    combined_pdf_object = convert_images_to_pdf(image_paths)

    # writing the PDF object as a pdf file
    combined_pdf_object.write(os.path.join(dest_path))


if __name__ == "__main__":
    main()
