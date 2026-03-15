import json
from typing import Dict, Any
from openai import OpenAI
from .base import BaseEngine
from ..config import get_settings


class LogicEngine(BaseEngine):
    def __init__(self, client: OpenAI = None):
        if client is None:
            settings = get_settings()
            client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL
            )
        super().__init__(client)
        self.settings = get_settings()
    
    def process(self, input_data: str) -> Dict[str, Any]:
        return self.extract_logic(input_data)
    
    def extract_logic(self, raw_text: str) -> Dict[str, Any]:
        system_prompt = """
        你是一个High-Logic/Minimalist分析器，专注于从文本中提取核心逻辑和结构。
        请分析以下文本，提取出：
        1. 核心观点和关键洞察
        2. 重要数据点和事实
        3. 论证结构和逻辑关系
        4. 结论和建议
        
        请以结构化JSON格式返回，包含以下字段：
        - key_insights: 核心洞察数组
        - data_points: 数据点字典
        - structure: 论证结构描述
        - conclusions: 结论数组
        - recommendations: 建议数组
        """
        
        response = self.client.chat.completions.create(
            model=self.settings.DEEPSEEK_MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": raw_text}
            ],
            timeout=self.settings.API_TIMEOUT,
            response_format={"type": "json_object"}
        )
        
        content = response.choices[0].message.content
        return json.loads(content)