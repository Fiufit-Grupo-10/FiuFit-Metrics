from fastapi import APIRouter, HTTPException, Request, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND
