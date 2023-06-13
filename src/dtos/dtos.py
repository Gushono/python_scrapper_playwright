from typing import Optional

from pydantic import BaseModel


class CompanyPercentageStarReviews(BaseModel):
    star: str
    percentage: str


class CompanyDetails(BaseModel):
    description: Optional[str]
    url: str
    rating: Optional[str]
    percentage_of_all_star_reviews: Optional[list[CompanyPercentageStarReviews]]
