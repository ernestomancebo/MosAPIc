import itertools
from typing import List, Tuple

import pinecone
from pandas import DataFrame

from mosapi.integrations.transformers import SentenceTransformerWrapper
from mosapi.settings import get_settings


class PineconeClient:

    def __init__(self):
        settings = get_settings()
        pinecone.init(api_key=settings.PINECONE_API_KEY,
                      environment=settings.PINECONE_API_REGION)
        if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
            pinecone.create_index(settings.PINECONE_INDEX_NAME,
                                  dimension=settings.PINECONE_INDEX_EMBEDING_DIMENSION,
                                  metric=settings.PINECONE_INDEX_METRIC)
        self.index = pinecone.Index(index_name=settings.PINECONE_INDEX_NAME)
        self.encoder = SentenceTransformerWrapper()

    def df_as_chunk(self, df: DataFrame, batch_size=100):
        it = iter(df)
        chunk = tuple(itertools.islice(it, batch_size))

        while chunk:
            yield chunk
            chunk = tuple(itertools.islice(it, batch_size))

    def batch_upsert(self, df: DataFrame, id_column: str, vector_column: str, batch_size=100):
        for batch in self.df_as_chunk([(str(t), v) for t, v in zip(df[id_column], df[vector_column])]):
            self.index.upsert(vectors=batch)

    def get_by_id(self, ids: List[int | str]):
        embedings = self.index.getch(ids)
        return embedings

    def get_by_question(self, questions: List[str], top_k: int = 5, include_values=False):
        query_vector = [self.encoder.encode_text(q) for q in questions]
        query_result = self.index.query(queries=query_vector,
                                        top_k=top_k,
                                        include_values=include_values)

        return query_result
    # TODO: other ways to query

    def do_upsert(self, vectors: Tuple):
        self.index.upsert(vectors=vectors)

    def delete_by_id(self, ids: List[int | str]):
        self.index.delete(ids=ids)

    def truncate_index(self, dry_run: bool = False):
        if dry_run:
            return

        self.index.delete(deleteAll='true')
