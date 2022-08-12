from typing import Any
from datetime import date

from fastapi import FastAPI
from mangum import Mangum
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from .utils import workers
from .utils.validators import DateValidator

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter


@app.get("/how-old/")
@limiter.limit("3/second")
def get_age(request: Request, dob: date) -> Any:
    """Get age, given a date of birth"""
    validator = DateValidator(dob)
    validated_dob = validator.validate()
    age = workers.calculate_age(validated_dob)
    return age


handler = Mangum(app)
