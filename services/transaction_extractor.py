from PyPDF2 import PdfReader
import re

def extract_statement_pdf(file_path) -> list:
    """
    Extracts transaction details from the uploaded PDF file.
    """
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()

    # Regex pattern to extract transactions
    pattern = re.compile(r'(\d+[A-Z]+\d+)\s+(\d+)\s+(\d+)\s+([\w\d\s]*)\s+([\d\s]*)\s+([\d\.]+[DC])')
    matches = pattern.findall(text)

    transactions = []
    is_ref_number = True

    for match in matches:
        imad, time, _type, ref_number, other_acc, amount = match
        ref_number_parts = ref_number.split()

        # Check for 'D' or 'C' to set the debit_credit field
        debit_credit = "D" if amount[-1] == "D" else "C" if amount[-1] == "C" else "UNKNOWN"

        # Remove the 'D' or 'C' from the amount and convert to float
        amount = float(amount[:-1].strip())  # Strip 'D' or 'C' and convert to float
        
        if is_ref_number:
            transactions.append({
                "imad": imad,
                "time": time,
                "type": _type,
                "ref_number": ref_number_parts[0] if ref_number_parts else "",
                "other_acc": ref_number_parts[1] if len(ref_number_parts) > 1 else "",
                "amount": amount,
                "debit_credit": debit_credit
            })
            is_ref_number = False
        else:
            transactions.append({
                "imad": imad,
                "time": time,
                "type": _type,
                "ref_number": None,
                "other_acc": ref_number.strip(),
                "amount": amount,
                "debit_credit": debit_credit
            })

    return transactions

