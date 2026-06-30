
from pydantic import BaseModel, Field


class TrendingTerm(BaseModel):
    term: str = Field(description="The search term")
    score: int | None = Field(description="Interest score (0-100, may be null)")
    rank: int = Field(description="Rank position for the week")


class RisingTerm(BaseModel):
    term: str = Field(description="The search term")
    percent_gain: int = Field(description="Percentage increase in interest")
    score: int | None = Field(description="Current interest score (0-100, may be null)")


class TermComparison(BaseModel):
    week: str = Field(description="Week date (YYYY-MM-DD)")
    term: str = Field(description="The search term")
    score: int | None = Field(description="Interest score for that week, may be null")
    rank: int = Field(description="Rank position for that week")
