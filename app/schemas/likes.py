from pydantic import BaseModel

class ReviewLikeResponse(BaseModel):
    id: int
    user_id: int
    review_id: int
    is_like: bool

class ReviewLikeCountResponse(BaseModel):
    review_id: int
    like_count: int

class ReviewIsLikeResponse(BaseModel):
    review_id: int
    user_id: int
    is_like: bool


class MovieReactionResponse(BaseModel):
    id: int
    user_id: int
    movie_id: int
    type: ReactionTypeEnum


class MovieReactionCountResponse(BaseModel):
    movie_id: int
    loke_count: int
    dislike_count: int