from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from services.pdf_data_extractor import PDFDataExtractor
from services.transaction_extractor import extract_transactions_from_pdf

# Initialize FastAPI and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home():
    """
    Renders the upload page with a form to upload a PDF.
    """
    return templates.TemplateResponse("upload.html", {"request": {}})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Handles PDF file upload and returns extracted data as JSON.
    """
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            temp_file.write(file.file.read())

        # Process the PDF file using PDFDataExtractor
        extractor = PDFDataExtractor("")  # PDF folder path can be passed if needed
        extracted_data = extractor.extract_all_data_from_pdf(temp_file_path)
        
        # Alternatively, extract transactions using PyPDF2
        transactions = extract_transactions_from_pdf(temp_file_path)

        # Combine the extracted data (you can choose which data to return)
        extracted_data["transactions"] = transactions

        # Clean up the temporary file
        os.remove(temp_file_path)

        # Return the extracted data as JSON
        return JSONResponse(content=extracted_data)

    except Exception as e:
        return JSONResponse(content={"error": str(e)})
