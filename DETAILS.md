
# Age Tracker

An API service that calculates the age of a person based on their date of birth.

## API Reference


#### Get age

```
  GET /howold/
```

| Parameter | Type   | Description                                 |
|:----------|:-------|:--------------------------------------------|
| `dob`     | `date` | **Required**. The date to calculate against |


## Authors

- [@f-gozie](https://www.github.com/f-gozie)


## Demo

https://age-tracker.herokuapp.com/

## Run Locally (Without Docker)

Clone the project

```bash
  git clone https://github.com/f-gozie/old-guy
```

Go to the project directory

```bash
  cd old-guy
```

Activate preferred virtual environment (after creation)

```bash
  conda activate old-guy
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  uvicorn my-age-is.main:app --reload
```


## Overview


This is a very simple API service that calculates the age of a person based on their date of birth. It has one exposed endpoint `GET /howold/` which takes a query param `dob` and returns the age of the person. The first point of contact is with the rate limiter [slow-api](https://slowapi.readthedocs.io/) which is used to prevent excessive usage of the API.
It limits the number of requests per second to 3 per client, per second. Assuming it doesn't trigger an exception `(429)`, it then goes through the provided validation by fastapi which checks the format of the date. Assuming the format is correct, it then goes through our custom `DateValidator` which checks if the date provided is in the future. If it is, it returns a 400 error.
Otherwise, it returns the age of the person.