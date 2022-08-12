from typing import Any
from datetime import date

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request

from .utils import workers
from .utils.validators import DateValidator

limiter = Limiter(key_func=get_remote_address)
origins = ["*"]
app = FastAPI()
app.state.limiter = limiter
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/howold/")
@limiter.limit("3/second")
def get_age(request: Request, dob: date) -> Any:
    """Get age, given a date of birth"""
    validator = DateValidator(dob)
    validated_dob = validator.validate()
    age = workers.calculate_age(validated_dob)
    return age


handler = Mangum(app)
