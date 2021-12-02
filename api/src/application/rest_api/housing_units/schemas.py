from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class DataIngestionPostRequestBody:
    dataset_id: Optional[str] = 'hg8x-zxpr'
    reset_table: Optional[bool] = True
