# Flask RESTful API

This project is a RESTful API built with Flask and Flask-RESTful. It provides endpoints for managing programs, drugs, and other related entities.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/HectorDelgadoR/ppt-challenge.git
   cd ppt-challenge
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

### Sample success API response

```
{
    "message": "File successfully parsed"
}
```

### Sample failure API response:

```
{
    "message": "Program already exists"
}
```

## How to run the API (programs by id)

You can use cURL executing the following command:

```
curl --location 'http://127.0.0.1:5000/api/programs/11757'
```

or just opening `http://127.0.0.1:5000/api/programs/11757` in your browser

11757 is the id for the current program, you can change it if needed.

### Sample success API response:

```
{
    "benefits": [
        {
            "name": "max_annual_savings",
            "value": "13000.0"
        },
        {
            "name": "min_out_of_pocket",
            "value": "0.0"
        }
    ],
    "coverage_eligibilities": [
        "Commercially insured"
    ],
    "details": [
        {
            "eligibility": "Patient must have commercial insurance, including health insurance exchanges, federal employee plans, or state employee plans",
            "income": "Not required",
            "program_detail": "Eligible patients may pay as little as $0 for every month of Dupixent",
            "renewal": "Patient will be automatically re-enrolled every January 1st provided that their card has been used within 18 months"
        }
    ],
    "drugs": [
        {
            "name": "Dupixent"
        },
        {
            "name": "Dupixent Pen"
        }
    ],
    "expiration_date": "\"\"",
    "forms": [
        {
            "link": "https://www.dupixent.com/support-savings/copay-card",
            "name": "Enrollment Form"
        }
    ],
    "free_trial_offer": "false",
    "funding": {
        "current_funding_level": "Data Not Available",
        "evergreen": "true"
    },
    "help_line": "844-387-4936",
    "id": 11757,
    "last_updated": "01/07/2025",
    "program_name": "Dupixent MyWay Copay Card",
    "program_type": "Coupon",
    "requirements": [
        {
            "name": "minimum_age",
            "value": "18"
        },
        {
            "name": "insurance_coverage",
            "value": "true"
        },
        {
            "name": "us_residency",
            "value": "true"
        },
        {
            "name": "eligibility_length",
            "value": "12m"
        }
    ]
}
```

### Sample not found API response:

```
{
    "error": "Program with ID 11756 not found"
}
```

## How to run the API (programs by query params)

You can use the following cURL:

```
curl --location 'http://127.0.0.1:5000/api/programs?program_type=Coupon&coverage_eligibilities=Commercially%20insured'
```

You can filter by `program_type` and `coverage_eligibilities`.

### Sample success API response with elements:

```
[
    {
        "benefits": [
            {
                "name": "max_annual_savings",
                "value": "13000.0"
            },
            {
                "name": "min_out_of_pocket",
                "value": "0.0"
            }
        ],
        "coverage_eligibilities": [
            "Commercially insured"
        ],
        "details": [
            {
                "eligibility": "Patient must have commercial insurance, including health insurance exchanges, federal employee plans, or state employee plans",
                "income": "Not required",
                "program_detail": "Eligible patients may pay as little as $0 for every month of Dupixent",
                "renewal": "Patient will be automatically re-enrolled every January 1st provided that their card has been used within 18 months"
            }
        ],
        "drugs": [
            {
                "name": "Dupixent"
            },
            {
                "name": "Dupixent Pen"
            }
        ],
        "expiration_date": "\"\"",
        "forms": [
            {
                "link": "https://www.dupixent.com/support-savings/copay-card",
                "name": "Enrollment Form"
            }
        ],
        "free_trial_offer": "false",
        "funding": {
            "current_funding_level": "Data Not Available",
            "evergreen": "true"
        },
        "help_line": "844-387-4936",
        "id": 11757,
        "last_updated": "01/07/2025",
        "program_name": "Dupixent MyWay Copay Card",
        "program_type": "Coupon",
        "requirements": [
            {
                "name": "minimum_age",
                "value": "18"
            },
            {
                "name": "insurance_coverage",
                "value": "true"
            },
            {
                "name": "us_residency",
                "value": "true"
            },
            {
                "name": "eligibility_length",
                "value": "12m"
            }
        ]
    }
]
```

### Sample success API response empty list:

```
[]
```