from PyPDF2 import PdfReader
import re

def extract_transactions_from_pdf(file_path) -> list:
    """
    Extracts transaction details from the uploaded PDF file.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Regex pattern to extract transactions
    pattern = re.compile(r'(\d{4}[A-Z]+\d+)\s+(\d{4})\s+(\d{4})\s+([\w\d\s]*)\s+([\d\s]*)\s+([\d\.]+[DC])')
    matches = pattern.findall(text)

    transactions = []
    is_first_row = True

    for match in matches:
        imad, time, _type, ref_number, other_acc, amount = match
        ref_number_parts = ref_number.split()

        if is_first_row:
            transactions.append({
                "IMAD": imad,
                "TIME": time,
                "TYPE": _type,
                "REF_NUMBER": ref_number_parts[0] if ref_number_parts else "",
                "OTHER_ACC": ref_number_parts[1] if len(ref_number_parts) > 1 else "",
                "AMOUNT": amount
            })
            is_first_row = False
        else:
            transactions.append({
                "IMAD": imad,
                "TIME": time,
                "TYPE": _type,
                "REF_NUMBER": "",
                "OTHER_ACC": ref_number.strip(),
                "AMOUNT": amount
            })

    return transactions
