# Original Quote Generator
This is a simple quote generator written in python/flask that generates original quotes using ChatGPT and a random background for the quote using [Pexels API](https://www.pexels.com/api/documentation/).
## Installation
1. Create a virtual environment with `python -m venv venv`
1. Activate it with `venv\scripts\activate`
1. Install required dependencies with `python -m pip install -r requirements.txt`
1. Create a `.env` file in the root directory of your project. Add the following variables:
```python
OPENAI_API_KEY='your_openai_api_key'
PEXELS_API_KEY='your_pexels_api_key'
SECRET_KEY='your_flask_secret_key'
```
5. Run server with `python app.py`
___
* To get flask's secret key, you can use command line:<br>
`python -c "import os; print(os.urandom(24).hex())"`