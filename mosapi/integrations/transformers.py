from typing import List

from pandas import DataFrame
from sentence_transformer import SentenceTransformer
from transformers import TapasForQuestionAnswering, TapasTokenizer, pipeline

from mosapi.settings import get_settings


class SentenceTransformerWrapper:
    def __init__(self):
        settings = get_settings()
        self.model = SentenceTransformer(settings.HF_TRANSFORMER_MODEL_NAME)

    def encode_df_text(self, df: Dataframe, column_name: str):
        encoded_series = df[column_name].apply(
            lambda x: self.encode_text(str(x)))
        return encoded_series

    def encode_text(self, text: str) -> List[float]:
        encoded_text = self.model.encode(text)
        return encoded_text.toList()


class TapasTransfomerWrapper:

    def __init__(self):
        settings = get_settings()
        self.tokenizer = TapasTokenizer.from_pretrained(
            settings.HF_TRANSFORMER_TOKENIZER_NAME)
        self.model = TapasForQuestionAnswering.from_pretrained(settings.HF_TRANSFORMER_TOKENIZER_NAME,
                                                               local_files_only=False)
        # TODO: Verify device id
        self.device = 0
        self.pipe = pipeline('table-question-answering',
                             model=self.model,
                             tokenizer=self.tokenizer,
                             device=self.device)

    def query_table(self, table: DataFrame, query: str):
        self.pipe(table=table[''],
                  query=query,
                  device=self.device)
