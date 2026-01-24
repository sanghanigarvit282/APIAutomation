## API Automation using Pytest

### Tech Stack
- Python 3.12
- Pytest
- Requests
- pytest-html

### Setup
pip install -r requirements.txt

### Run Tests
pytest


### Generate HTML Report
pytest --html=reports/report.html --self-contained-html

### Configuration
Update config/config.ini for URL or credentials

### Run with Base URL
pytest --baseurl https://restful-booker.herokuapp.com
