from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

def get_abjad_output():
    filename = "dca_ps.pdf"
    image = convert_from_path(filename, fmt="png", single_file=True, output_file="dca_ps")
