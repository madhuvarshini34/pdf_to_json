from PyPDF2 import PdfReader
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from services.pdf_outgoing_data_extractor import OutgoingPDFData
from services.pdf_incoming_data_extractor import IncomingPDFData
from services.transaction_extractor import extract_statement_pdf

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

def identifier_for_pdf(file_path: str) -> str:
    """
    Extracts a unique identifier from the provided PDF and identifies its type.
    Checks for keywords such as 'STATEMENT', 'IMAD', and 'OMAD' to classify the PDF type.

    Args:
        file_path (str): The path to the uploaded PDF file.

    Returns:
        str: The identifier (e.g., "STATEMENT", "WIRE OUTGOING", etc.)
    """
    try:
        # Open the PDF file and extract text using PdfReader
        with open(file_path, "rb") as file:
            reader = PdfReader(file)  # Use PdfReader directly
            pdf_text = ""
            for page in reader.pages:
                pdf_text += page.extract_text()

        # Check for specific keywords in the extracted text
        if "STATEMENT" in pdf_text:
            return "STATEMENT"
        elif "IMAD" in pdf_text and "OMAD" in pdf_text:
            return "WIRE INCOMING"
        elif "IMAD" in pdf_text and "OMAD" in pdf_text:
            return "WIRE OUTGOING"
        else:
            return "UNKNOWN"
    except Exception as e:
        raise ValueError(f"Error extracting identifier: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Renders the upload page with a form to upload a PDF.
    """
    return templates.TemplateResponse("upload.html", {"request": {}})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles PDF file upload and returns extracted transactions as a plain list.
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())

        # Extract identifier
        identifier = identifier_for_pdf(temp_file_path)

        # Initialize appropriate extraction logic based on the identifier
        if identifier == "WIRE OUTGOING":
            extractor = OutgoingPDFData("")  # Assuming "" is for default path, adjust if needed
            extracted_data = extractor.extract_outgoing_pdf(temp_file_path)
        elif identifier == "WIRE INCOMING":
            extractor = IncomingPDFData("")
            extracted_data = extractor.extract_incoming_pdf(temp_file_path)
        elif identifier == "STATEMENT":
            extracted_data = extract_statement_pdf(temp_file_path)
        else:
            extracted_data = {"error": "Unknown PDF type"}

        # Clean up the temporary file
        os.remove(temp_file_path)

        # Return the extracted data (including transactions) as a JSON response
        return extracted_data

    except Exception as e:
        return JSONResponse(content={"error": str(e)})
