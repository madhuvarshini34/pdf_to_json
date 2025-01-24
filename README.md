# PDF Data Extractor

This project is designed to extract structured data from PDF files using FastAPI and `pdfplumber`. 
It allows you to process PDF files, extract relevant information using regular expressions, and return the extracted data as JSON without any nested structures.

## Features

- Extracts structured data from a PDF file.
- Uses regular expressions to identify key information.
- Returns extracted data in a flat JSON format.
- Provides an API endpoint using FastAPI to interact with the PDF extraction process.

## Requirements

- Python 3.8 or higher
- `FastAPI`
- `pdfplumber`
- `re` (built-in Python module)
- `deque` (built-in Python module)
- `Uvicorn` for running the FastAPI server

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/yourrepositoryname.git
   cd yourrepositoryname
   ```

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Run the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### `GET /extract-pdf-data/{pdf_file_name}`

This endpoint accepts the name of the PDF file and returns the extracted data as JSON.

**URL Parameters:**
- `pdf_file_name` (str): The name of the PDF file located in the specified folder.

## Approach

1. **PDF Text Extraction**: 
   - The `pdfplumber` library is used to extract text from PDF files. We iterate through all pages of the PDF to extract the textual content.

2. **Regular Expressions**:
   - Regular expressions are used to identify and extract specific fields from the PDF text. Each field is defined by a regular expression pattern that matches the relevant part of the text.
   - The regex patterns are applied to each line of the extracted text to search for key pieces of data.

3. **Data Structuring**:
   - After extracting the relevant data using regex, the information is stored in a flat dictionary (JSON format) to ensure easy consumption by the API.
   - The `Originator` and `Beneficiary` sections are parsed separately, but their data is added directly to the main dictionary, avoiding nested structures.

## Main Functions

### `safe_search(pattern, line, group=1, default="Unknown")`

This function performs a safe search using regular expressions. It attempts to match the provided pattern in the given line. If a match is found, it returns the matched group; otherwise, it returns the default value (`"Unknown"`).

**Parameters:**
- `pattern`: The regular expression pattern to match.
- `line`: The line of text to search.
- `group`: The group number to return from the match (default is 1).
- `default`: The default value to return if no match is found (default is `"Unknown"`).

**Returns:**
- The matched group or the default value.

### `extract_outgoing_data(pdf_path)`

This function is responsible for extracting all relevant data from the PDF file located at `pdf_path`. It processes the entire PDF content, applies the regular expressions to extract the desired fields, and returns a flat dictionary of extracted data.

**Parameters:**
- `pdf_path`: The path to the PDF file from which data is to be extracted.

**Returns:**
- A dictionary containing the extracted data, including fields like `Environment`, `ABA`, `Amount`, `Originator Name`, and more.

### `extract_incoming_data(pdf_path)`

This function is responsible for extracting all relevant data from the PDF file located at `pdf_path`. It processes the entire PDF content, applies the regular expressions to extract the desired fields, and returns a flat dictionary of extracted data.

**Parameters:**
- `pdf_path`: The path to the PDF file from which data is to be extracted.

**Returns:**
- A dictionary containing the extracted data, including fields like `Environment`, `ABA`, `Amount`, `Originator Name`, and more.


### `extract_statement_data(pdf_file_name: str)`

This is the FastAPI endpoint that receives the name of a PDF file, processes it using `extract_all_data_from_pdf()`, and returns the extracted data as JSON.

**Parameters:**
- `pdf_file_name`: The name of the PDF file located in the specified directory.

**Returns:**
- JSON containing the extracted data from the PDF.

## Contributing

Feel free to fork the repository, make changes, and submit pull requests. Contributions are always welcome!
