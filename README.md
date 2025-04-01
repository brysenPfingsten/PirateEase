# PirateEase Chatbot

Pirate-themed chatbot able to interactively handle user queries by dynamically fetching information and responding to the user.

## Installation Instructions

### 1. Clone the Repository
```
git clone https://github.com/brysenPfingsten/OOP2/tree/main/ChatBot
```

### 2. Set Up a Virtual Environment

### macOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```
### Windows:
```
python -m venv venv
venv\Scripts\activate
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Install Package in Editable Mode
```
pip install -e .
```

## Running the Application

### Start the Chatbot
```
cd PirateEase
python main.py
```

### Run Tests with Coverage
```
pytest --cov=PirateEase --cov-config=.coveragerc --cov-report=html
```

After running the tests, open the generated htmlcov/index.html file in your browser.

You should see coverage results similar to this:

![test_coverage](https://github.com/user-attachments/assets/5f52471a-0cb2-4762-89e4-852cba6c28e4)

## Report and Class Diagram

A detailed report of this project can be found [here](Report/report.pdf).

A class diagram can be found[here](Report/diagram.png).
