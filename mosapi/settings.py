from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8',
                                      case_sensitive=True)
    APP_ENV: str
    # App settings
    APP_PORT: int
    APP_TRUSTED_HOSTS: List[str]
    APP_ALLOWED_HOSTS: List[str]

    # Pinecone API settings
    PINECONE_API_KEY: str
    PINECONE_API_REGION: str
    # Pinecone embeding settings
    PINECONE_INDEX_NAME: str
    PINECONE_INDEX_EMBEDING_DIMENSION: int
    PINECONE_INDEX_METRIC: str
    # Pinecone batch load
    PINECONE_BATCH_SIZE: int

    # HuggingFace
    HF_DATASET_NAME: str
    HF_TRANSFORMER_MODEL_NAME: str
    HF_TRANSFORMER_TOKENIZER_NAME: str


@lru_cache()
def get_settings():
    """Loads settings"""
    return Settings()
