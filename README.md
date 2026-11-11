# Assignment Submission Portal

A simple web-based Assignment Submission Portal developed using Python and Flask for the DevOps Lab Mid assignment.

## Features

- Student name, registration number, assignment title, and submission URL fields.
- Validation for required fields.
- Validation for submission URLs.
- Saves valid submissions in an SQLite database.
- Displays saved submissions on the portal.

## Technologies Used

- Python
- Flask
- SQLite
- HTML and CSS
- Pytest
- Git and GitHub

## Project Structure

```text
Assignment-Submission-Portal/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
└── tests/
    └── test_app.py
```

## Setup Instructions

1. Clone the repository:

```bash
git clone https://github.com/hadiashehzad933-code/assignment-submission-portal.git
```

2. Open the project folder:

```bash
cd assignment-submission-portal
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

5. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

```bash
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

## Run Tests

```bash
python -m pytest -v
```

## Automated Testing

The project includes three tests:

1. Valid submission is saved and displayed.
2. Missing registration number is rejected.
3. Invalid submission URL is rejected.

GitHub Actions CI pipeline and automatic local test report receiver will be added as part of the DevOps implementation.
