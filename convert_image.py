from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def get_abjad_output(pdf_file, png_file, multiple_pages=False):
    png_stem = png_file[:-4]
    if not multiple_pages:
        image = convert_from_path(pdf_file, fmt="png", single_file=True, output_folder="imgs", output_file=png_stem)
    else:
        images = convert_from_path(pdf_file)
        for i, image in enumerate(images):
            filename = png_stem + str(i) + ".png"
            image.save(filename, "PNG")
        return len(images)
