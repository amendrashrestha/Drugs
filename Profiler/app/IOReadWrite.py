import traceback
from io import StringIO

import docx
import unidecode
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage


def get_data_from_file(textfile, file_type):
    try:
        if file_type in ".txt":
            raw_text = textfile.read()

            try:
                text = raw_text.decode("utf-8")
                text = unidecode.unidecode(text)
            except Exception:
                text = raw_text.decode("ISO-8859-4")

        elif file_type in ".pdf":
            text = ""
            rsrcmgr = PDFResourceManager()
            retstr = StringIO()
            laparams = LAParams()
            device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=laparams)

            interpreter = PDFPageInterpreter(rsrcmgr, device)
            maxpages = 0
            pagenos = set()

            for page in PDFPage.get_pages(textfile, pagenos, maxpages=maxpages):
                interpreter.process_page(page)
            text = retstr.getvalue()

            device.close()
            retstr.close()

        elif file_type in ".docx":
            doc_text = []
            document = docx.Document(textfile)

            for para in document.paragraphs:
                doc_text.append(para.text)

            text = ''.join(doc_text)

    except Exception:
        traceback.print_exc()

    return text
