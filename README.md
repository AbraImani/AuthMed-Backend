# Backend for Counterfeit Medicine Detection

This project is the backend for **AuthMed**, an application designed to
detect counterfeit medicines.\
It is built with **FastAPI** and leverages **image processing** to
analyze photos of medicines and compare them against a reference
database.

## Installation

Make sure you have **Python 3.8+** installed.

### 1. Clone the repository

``` bash
git clone <your-repo-url>
cd project-directory
```

### 2. Create and activate a virtual environment

``` bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies (including OpenCV and Pillow)

``` bash
pip install -r requirements.txt
```

## Running the Application

From the project root directory, start the server with Uvicorn:

``` bash
uvicorn app.main:app --reload
```

-   API will be available at: <http://127.0.0.1:8000>\
-   Interactive API documentation (Swagger UI):
    <http://127.0.0.1:8000/docs>

On the first run, a database file `counterfeit_detection.db` will be
created, along with two tables:\
- **medicaments**\
- **logs**

The `medicaments` table will be automatically populated with two test
entries.

## Testing the API

The main endpoint is:

    POST /scan

It accepts an **image** in `multipart/form-data`.

### Example Test with cURL

1.  Prepare a test image (JPG or PNG), e.g. `test_image.jpg`\
2.  Send it to the `/scan` endpoint:

``` bash
curl -X POST "http://127.0.0.1:8000/scan"   -H "accept: application/json"   -F "file=@test_image.jpg;type=image/jpeg"
```

*(Replace `test_image.jpg` and `image/jpeg` with your file name and MIME
type if needed)*

### Expected Response

The current mock analysis module simulates reading a barcode
`"8901234123457"`, which matches `"Paracetamol 500mg"` in the test
database.\
Regardless of the image you send, you should receive:

``` json
{
  "status": "Authentic",
  "message": "Medicine identified as 'Paracetamol 500mg'. Match found in the reference database.",
  "log_id": 1,
  "matched_medicament": {
    "name": "Paracetamol 500mg",
    "barcode": "8901234123457",
    "logo_path": null,
    "qr_code_data": "SN:123;EXP:2026-12",
    "id": 1
  }
}
```

If you modify the simulated barcode in `app/analysis_module.py` to a
value not present in the database, the response status will be
`"Suspect"`.

## Next Steps

-   **Integrate a real OCR/QR Code model**\
    Replace the mock logic in `app/analysis_module.py` with libraries
    such as `pytesseract` or `pyzbar`.
-   **Integrate a computer vision model**\
    Use TensorFlow or PyTorch in `analysis_module.py` to detect visual
    anomalies.
-   **Connect to an external database/API**\
    Update `app/crud.py` to query an external API instead of the local
    SQLite database (sqlalchemy to Postgresql if possible but while we want to make the application in production) .
