from sqlmodel import SQLModel, Field
from typing import Optional, List
import json

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    content: str
    summary: Optional[str] = None
    keywords: Optional[str] = None  # Store keywords as a JSON string

    def set_keywords(self, keywords: List[str]):
        self.keywords = json.dumps(keywords)

    def get_keywords(self) -> List[str]:
        if self.keywords:
            return json.loads(self.keywords)
        return []
