from pydantic import BaseModel


class EmbedingSimilaritySearch(BaseModel):
    text: str
    top_k: int
    include_values: bool

    class Config:
        orm_mode = False
