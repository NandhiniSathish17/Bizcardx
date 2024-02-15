# Bizcardx
A Business Card Data Extraction Tool with OCR BizCardX is a Python-based tool that simplifies the process of extracting and managing information from business cards using Optical Character Recognition (OCR).





# BizCardX - Extracting Business Card Data with OCR

BizCardX is a user-friendly tool for extracting information from business cards using Optical Character Recognition (OCR) technology. This project leverages the EasyOCR library to recognize text on business cards and extracts the data into a SQL database after classification using regular expressions. The extracted information is then accessible through a GUI built using Streamlit. The BizCardX application provides an intuitive interface for users to upload business card images, extract information, and manage the data within a database.

## Project Overview

BizCardX aims to simplify the process of extracting and managing information from business cards. The tool offers the following features:

- Extraction of key information from business cards: company name, cardholder name, designation, contact details, etc.
- Storage of extracted data in a MySQL database for easy access and retrieval.
- GUI built with Streamlit for a user-friendly interface.
- User options to upload, extract, and modify business card data.

## Libraries/Modules Used

- `pandas`: Used to create DataFrames for data manipulation and storage.
- `mysql.connector`: Used to store and retrieve data from a MySQL database.
- `streamlit`: Used to create a graphical user interface for users.
- `easyocr`: Used for text extraction from business card images.

## Workflow

1. Install the required libraries using the command `pip install [Name of the library]`. Install `streamlit`, `mysql.connector`, `pandas`, and `easyocr`.
2. Execute the `BizCardX_main.py` script using the command `streamlit run BizCardX_main.py`.
3. The web application opens in a browser, presenting the user with three menu options: HOME, UPLOAD & EXTRACT, MODIFY.
4. Users can upload a business card image in the UPLOAD & EXTRACT menu.
5. The EasyOCR library extracts text from the uploaded image.
6. Extracted text is classified using regular expressions to identify key information such as company name, cardholder name, etc.
7. The classified data is displayed on the screen and can be edited by the user if needed.
8. Clicking the "Upload to Database" button stores the data in a MySQL database.
9. The MODIFY menu allows users to read, update, and delete data in the MySQL database.



