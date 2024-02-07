import fitz  # з
import os

def pdf_to_images_mupdf(pdf_path, output_folder=".", first=1, last=-1,step =1, dpi=200):
    """
    Convert each page of a PDF file into separate images using PyMuPDF.

    :param pdf_path: Path to the PDF file.
    :param output_folder: Folder to save the output images.
    :param dpi: Resolution of the output images, as dots per inch (DPI).
    """
    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Ensure output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    #get pdf pages
    if last == -1:
        last = len(doc)
    tt = list(range(len(doc)))
    tt = tt[first - 1:last:step]

    # Iterate through each page
    for page_num in tt:
        page = doc.load_page(page_num)  # number of page
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        output_image_path = os.path.join(output_folder, f"page_{page_num + 1}.png")
        pix.save(output_image_path)

    # Close the document
    doc.close()



# Пример использования функции
#pdf_file_path = "create_pdf_1.pdf"

# Example usage
#pdf_to_images_mupdf(pdf_file_path)