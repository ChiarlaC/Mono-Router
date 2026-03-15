from typing import Any, Dict
from .base import BaseOrchestrator, ContentContent
from ..engines import LogicEngine, StyleEngine


class ContentOrchestrator(BaseOrchestrator):
    def __init__(self):
        self.logic_engine = LogicEngine()
        self.style_engine = StyleEngine()
    
    def extract(self, input_data: str) -> str:
        return input_data
    
    def analyze(self, raw_text: str) -> Dict[str, Any]:
        return self.logic_engine.process(raw_text)
    
    def rewrite(self, logic_data: Dict[str, Any]) -> Dict[str, str]:
        return self.style_engine.process(logic_data)
    
    def export(self, content: ContentContent) -> Dict[str, Any]:
        return {
            "raw_text": content.raw_text,
            "logic_summary": content.logic_summary,
            "platform_content": content.rewritten_content
        }