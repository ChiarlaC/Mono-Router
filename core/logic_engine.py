import json
import time
from typing import Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

class LogicEngine:
    def __init__(self, api_key: str, endpoint: str = None, timeout: int = 30, max_retries: int = 3):
        # 使用环境变量中的API端点，如果没有提供
        if endpoint is None:
            endpoint = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        
        self.api_key = api_key
        self.endpoint = endpoint
        self.timeout = timeout
        self.max_retries = max_retries
        
        # 创建OpenAI客户端实例，配置为DeepSeek API
        self.client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
    
    def extract_logic(self, raw_text: str) -> Dict[str, Any]:
        """从原始文本中提取逻辑结构"""
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
        
        retries = 0
        while retries < self.max_retries:
            try:
                response = self.client.chat.completions.create(
                    model="deepseek-chat", 
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": raw_text}
                    ],
                    timeout=self.timeout,
                    response_format={"type": "json_object"}
                )
                
                # 解析响应
                content = response.choices[0].message.content
                logic_data = json.loads(content)
                return logic_data
                
            except json.JSONDecodeError as e:
                raise Exception(f"API返回的响应不是有效的JSON: {str(e)}")
                
            except Exception as e:
                retries += 1
                if retries >= self.max_retries:
                    raise Exception(f"提取逻辑时发生错误: {str(e)}")
                time.sleep(2 ** retries)  # 指数退避
                continue