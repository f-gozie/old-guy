from typing import Any
from datetime import date
import math
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from mangum import Mangum
from slowapi import Limiter
from slowapi.util import get_remote_address
from starlette.requests import Request
from starlette.responses import JSONResponse

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


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        dob = float(request.query_params.get("dob", ""))
        if math.isnan(dob):
            return JSONResponse(status_code=400, content={"error": "Invalid date format. Please use YYYY-MM-DD"})
        return JSONResponse(status_code=422, content=jsonable_encoder({"error": exc.errors()}))
    except ValueError:
        return JSONResponse(status_code=422, content=jsonable_encoder({"error": exc.errors()}))


@app.get("/howold/")
@limiter.limit("3/second")
def get_age(request: Request, dob: date) -> Any:
    """Get age, given a date of birth"""
    validator = DateValidator(dob)
    validated_dob = validator.validate()
    age = workers.calculate_age(validated_dob)
    return age


handler = Mangum(app)
