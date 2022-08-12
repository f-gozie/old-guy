import datetime

from fastapi import HTTPException


class DateValidator:
    def __init__(self, date):
        self.date = date

    def validate(self):
        if datetime.date.today() < self.date:
            raise HTTPException(status_code=400, detail="Date of birth cannot be in the future")

        return self.date
