from docx import Document
from odf import text, teletype
from odf.opendocument import load
from striprtf.striprtf import rtf_to_text
import markdown

def extract_text(file_path: str) -> str:
    """
    Extracts raw text from a file.
    """
    file_ext = file_path.split(".")[-1].lower()
    if file_ext == "docx":
        return extract_text_from_docx(file_path)
    elif file_ext == "odt":
        return extract_text_from_odt(file_path)
    elif file_ext == "rtf":
        return extract_text_from_rtf(file_path)
    elif file_ext == "md":
        return extract_text_from_md(file_path)
    elif file_ext == "txt":
        return extract_text_from_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

def extract_text_from_docx(file_path: str) -> str:
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_odt(file_path: str) -> str:
    textdoc = load(file_path)
    all_paras = textdoc.getElementsByType(text.P)
    return "\n".join([teletype.extractText(para) for para in all_paras])

def extract_text_from_rtf(file_path: str) -> str:
    with open(file_path, "r") as f:
        rtf_content = f.read()
    return rtf_to_text(rtf_content)

def extract_text_from_md(file_path: str) -> str:
    with open(file_path, "r") as f:
        md_content = f.read()
    return markdown.markdown(md_content)

def extract_text_from_txt(file_path: str) -> str:
    with open(file_path, "r") as f:
        return f.read()
