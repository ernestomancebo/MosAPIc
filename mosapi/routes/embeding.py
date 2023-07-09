from typing import Annotated

from fastapi import APIRouter, Depends

from mosapi.integrations.pinecone import PineconeClient
from mosapi.schemas.embeding import EmbedingSimilaritySearch

router = APIRouter(prefix="/embeding",
                   tags=["embeding", "pinecone"],
                   responses={404: {"description": "Not found"}})


@router.get("/")
async def root():
    return {"response": "Embeding"}


@router.post("/similarity-search")
async def similarity(similarity_search: EmbedingSimilaritySearch, pinecone_client: Annotated[PineconeClient, Depends(PineconeClient)]):
    answer = pinecone_client.get_by_question(questions=[similarity_search.text],
                                             top_k=similarity_search.top_k,
                                             include_values=similarity_search.include_values)

    return answer
