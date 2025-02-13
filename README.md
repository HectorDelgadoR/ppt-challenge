# Flask RESTful API

This project is a RESTful API built with Flask and Flask-RESTful. It provides endpoints for managing programs, drugs, and other related entities.

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-restful-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Copy the .env.example file to .env and add your own configuration:

   ```
   cp .env.example .env
   ```

   Edit the .env file to add your own configuration, especially for OPENAI_API_KEY:

   ```
   SECRET_KEY=your_secret_key
   DEBUG=False
   TESTING=False
   DATABASE_URI=sqlite:///app.db
   OPENAI_API_KEY=sk-your-openai-api-key
   ```

6. To init the db the first time:

   ```
   python init_db.py
   ```

## Usage

To run the application, execute the following command:
```
flask run
```

Make sure to set the `FLASK_APP` environment variable to `app` before running the command.

## Testing

To run the tests, use the following command:
```
pytest
```

## Extra

If you are testing and want to flush the db:

```
python flush_db.py
```

## How to run the ETL pipeline

The ETL is being triggered by an API sending an HTTP request with the .json file. You can do it executing the following cURL command:

```
curl --location 'http://127.0.0.1:5000/api/upload' \
--form 'file=@./dupixent.json'
```

Each program can be created just for 1 time, if you want to flush the db you can execute `python flush_db.py`

## How to run the API 

You can use cURL executing the following command:

```
curl --location 'http://127.0.0.1:5000/api/programs/11757'
```

or just opening `http://127.0.0.1:5000/api/programs/11757` in your browser

11757 is the id for the current program, you can change it if needed.

