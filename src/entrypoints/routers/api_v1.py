from fastapi import APIRouter

from src.dtos.dtos import CompanyDetails
from src.entrypoints.controllers.v1_scrapper import scrape

api_v1 = APIRouter(prefix="/v1")

api_v1.add_api_route(
    path="/scrape",
    endpoint=scrape,
    methods=["GET"],
    response_model=list[CompanyDetails],
)
