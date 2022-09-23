import datetime


class DateValidator:
    def __init__(self, date):
        self.date = date

    def validate(self):
        if self.date is None:
            return False, "Enter a valid date"
        if datetime.date.today() < self.date:
            return False, "Date of birth cannot be in the future"

        return True, self.date