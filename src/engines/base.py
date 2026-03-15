from abc import ABC, abstractmethod
from typing import Any, Dict
from openai import OpenAI


class BaseEngine(ABC):
    def __init__(self, client: OpenAI):
        self.client = client
    
    @abstractmethod
    def process(self, input_data: Any) -> Any:
        pass