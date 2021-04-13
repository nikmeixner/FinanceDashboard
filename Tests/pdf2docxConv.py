from pdf2docx import parse

pdf_file = r"C:\Users\nikme\Downloads\Vorlage.pdf"
docx_file = r"C:\Users\nikme\Downloads\Vorlage.docx"

# convert pdf to docx
parse(pdf_file, docx_file, start=0, end=None)

