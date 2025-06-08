# Loyverse API

Python wrapper for interacting with Loyverse API endpoints.

## Setup

Clone this repository to your local machine:
```sh
git clone https://github.com/dagsdags212/loyverse-api.git
cd loyvese-api
```

Install dependencies:
```sh
pip install .
```

Create a `.env` file and import your Loyverse API key. It should be stored under the `LOYVERSE_API_KEY` variable.

```
// .env
LOYVERSE_API_KEY=your-api-key-here
```

## Endpoints

A GET request for all endpoints can be sent using the `.get` method. This recursively fetches data by following a cursor (given by the response) and returns a JSON object containing the payload.

CRUD operations can be performed for all endpoints using the `.create`, `.update`, and `.delete` methods.

## Usage

To get started, import the Loyverse object from the `api` module:

```python
from loyverse.api import Loyverse
```

This allows the user to interface with all endpoints thru the `Loyverse` object.

### Customers

Fetch data for all customers:

```python
customers = Loyverse.customers.get()
```

Retrieve a customer that matches a given email:
```python
c = Loyverse.customers.from_email('customer@email.com')
```

Retrieve a set of customer created before or after a given date:

```python
from datetime import datetime, timedelta

# A datetime object must be passed
start_date = datetime(2025, 6, 1)
end_date = start_date + timedelta(days=3)

# Customers created before or on June 1, 2025
c = Loyverse.customers.created_at_max(start_date)

# Customers created on or after June 4, 2025
c = Loyverse.customers.created_at_min(end_date)

# Customer created within a given range
c = Loyverse.customers.created_within(start_date, end_date)
```

## Schemas

Data schemas are provded in the `loyverse.schemas` module. This makes data processing easier for the user. It also provide a field validators to ensure data integrity.

Currently available schemas include:

- Employee
- Customer
- Variant
- Item
- Receipt

As an example, let us fetch our employee list and load it as a data schema.

```python
# Fetch employee data in JSON format
employee_data = Loyverse.employees.get()

# Load as a pydantic model
employees = [Employee.model_validate(e) for e in employee_data]

# Access object attributes
for e in employees:
    print(f"Please contact {e.name} thru his/her phone number at {e.phone_number}")
```