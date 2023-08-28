from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class TitleElement(BaseModel):
    content: str
    embedding: Optional[List[float]] = None
    title_id = int 

class NotionBlock(BaseModel):
    block_type: str
    text_content: str
    embedding: Optional[List[float]] = None
    block_id : Optional[int] = None 

class NotionPage(BaseModel):
    title: TitleElement
    blocks: List[NotionBlock]
    url: Optional[HttpUrl]
    indexed : bool = False