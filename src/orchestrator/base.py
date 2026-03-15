from abc import ABC, abstractmethod
from typing import Any, Dict
from pydantic import BaseModel


class ContentContent(BaseModel):
    raw_text: str
    logic_summary: Dict[str, Any]
    rewritten_content: Dict[str, str]


class BaseOrchestrator(ABC):
    @abstractmethod
    def extract(self, input_data: Any) -> str:
        pass
    
    @abstractmethod
    def analyze(self, raw_text: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def rewrite(self, logic_data: Dict[str, Any]) -> Dict[str, str]:
        pass
    
    @abstractmethod
    def export(self, content: ContentContent) -> Dict[str, Any]:
        pass
    
    def run(self, input_data: Any) -> ContentContent:
        raw_text = self.extract(input_data)
        logic_summary = self.analyze(raw_text)
        rewritten_content = self.rewrite(logic_summary)
        
        content = ContentContent(
            raw_text=raw_text,
            logic_summary=logic_summary,
            rewritten_content=rewritten_content
        )
        
        self.export(content)
        return content