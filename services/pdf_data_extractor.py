import os
import re
import pdfplumber
from collections import deque

class PDFDataExtractor:
    def __init__(self, pdf_folder_path: str):
        self.pdf_folder_path = pdf_folder_path

    @staticmethod
    def safe_search(pattern, line, group=1, default="Unknown"):
        match = re.search(pattern, line)
        return match.group(group) if match else default

    def extract_all_data_from_pdf(self, pdf_file_name: str):
        pdf_path = os.path.join(self.pdf_folder_path, pdf_file_name)

        # Check if the file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"File '{pdf_file_name}' not found in the folder.")

        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        lines = deque(text.splitlines())

        # Regular expressions for fields
        fields = {
            "Environment": r"Environment:\s+([\w\-]+)",
            "ABA": r"ABA:\s+(\d+)",
            "Mode": r"Mode:\s+([\w\-]+)",
            "Service Unit": r"Service Unit:\s+(\d+)",
            "Cycle Date": r"Cycle Date:\s+([\d/]+)",
            "System Date/Time": r"System Date/Time:\s+([\d/: ]+)",
            "Status": r"Status:\s+([\w\-]+)",
            "Message Type": r"Message Type:\s+([\w\-]+)",
            "Create Time": r"Create Time:\s+([\d/: ]+)",
            "Test/Prod": r"Test/Prod:\s+([\w\-]+)",
            "IMAD": r"IMAD:\s+([\w\d ]+)",
            "OMAD": r"OMAD:\s+([\w\d ]+)",
            "Sender ABA": r"Sender ABA \{\d+\}:\s+(\d+)",
            "Sender Name": r"Sender ABA \{\d+\}:\s+\d+\s+([\w &]+)",
            "Receiver ABA": r"Receiver ABA \{\d+\}:\s+(\d+)",
            "Receiver Name": r"Receiver ABA \{\d+\}:\s+\d+\s+([\w &]+)",
            "Amount": r"Amount \{\d+\}:\s+([\d.]+)",
            "Type/Subtype Code": r"Type/Subtype Code \{\d+\}:\s+([\w \-]+)",
            "Business Function": r"Business Function \{\d+\}:\s+([\w \-]+)",
        }

        originator_fields = {
            "Originator ID Code": r"ID Code[:\s]+([\w \-]+)",
            "Originator Identifier": r"Identifier[:\s]+([\w\d]+)",
            "Originator Name": r"Name[:\s]+([\w ]+)",
            "Originator Address": r"Address[:\s]+([^\n]+)",
        }

        beneficiary_fields = {
            "Beneficiary ID Code": r"ID Code[:\s]+([\w \-]+)",
            "Beneficiary Identifier": r"Identifier[:\s]+([\w\d]+)",
            "Beneficiary Name": r"Name[:\s]+([\w ]+)",
            "Beneficiary Address": r"Address[:\s]+([^\n]+)",
        }

        extracted_data = {}
        current_group = None

        while lines:
            line = lines.popleft().strip()

            # Detect section markers
            if "Originator" in line:
                current_group = "Originator"
                continue
            elif "Beneficiary" in line:
                current_group = "Beneficiary"
                continue

            # General fields
            for field_name, pattern in fields.items():
                value = self.safe_search(pattern, line)
                if value != "Unknown":
                    extracted_data[field_name] = value

            # Originator fields
            if current_group == "Originator":
                for field_name, pattern in originator_fields.items():
                    value = self.safe_search(pattern, line)
                    if value != "Unknown":
                        extracted_data[field_name] = value
                        break

            # Beneficiary fields
            elif current_group == "Beneficiary":
                for field_name, pattern in beneficiary_fields.items():
                    value = self.safe_search(pattern, line)
                    if value != "Unknown":
                        extracted_data[field_name] = value
                        break

        return extracted_data
