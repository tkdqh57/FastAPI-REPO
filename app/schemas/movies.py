from ptdantic import BaseModel

class CreateMovieRequest(BaseModel):
    title: str
    playtime: int
    gnere: list[str]


class MovieResponse(BaseModel):
    id: int
    title: str
    playtime: int
    genre: list[str]

class MocieSearchParams(BaseModel):
    title: str | None = None
    genre: str | None = None


class MovieUpdateRequerst(BaseModel):
    title: str | None = None
    playtime: Annotated[int, Field(gt=0)] | None = None
    genre: list[str] | None = None