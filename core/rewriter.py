import json
import concurrent.futures
from typing import Dict, Any, Optional
from openai import OpenAI
from utils.prompts import PROMPTS
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

class StyleRewriter:
    def __init__(self, api_key: str, endpoint: str = None, timeout: int = 30):
        # 使用环境变量中的API端点，如果没有提供
        if endpoint is None:
            endpoint = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        
        self.api_key = api_key
        self.endpoint = endpoint
        self.timeout = timeout
        
        # 创建OpenAI客户端实例，配置为DeepSeek API
        self.client = OpenAI(
            api_key=api_key,
            base_url=endpoint
        )
    
    def _rewrite_single(self, platform: str, logic_data: Dict[str, Any]) -> str:
        """为单个平台重写内容"""
        if platform not in PROMPTS:
            raise ValueError(f"不支持的平台: {platform}")
        
        system_prompt = PROMPTS[platform]
        
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat", 
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": json.dumps(logic_data, ensure_ascii=False)}
                ],
                timeout=self.timeout
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"为{platform}重写内容时发生错误: {str(e)}")
    
    def parallel_rewrite(self, logic_data: Dict[str, Any]) -> Dict[str, str]:
        """并行为所有平台重写内容"""
        # 输入验证
        if not isinstance(logic_data, dict):
            raise ValueError("logic_data必须是字典类型")
        
        platforms = ["zhihu", "xhs", "wechat"]
        results = {}
        
        # 使用线程池并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # 提交所有任务
            future_to_platform = {
                executor.submit(self._rewrite_single, platform, logic_data): platform
                for platform in platforms
            }
            
            # 收集结果
            for future in concurrent.futures.as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    results[platform] = future.result()
                except Exception as e:
                    # 处理部分失败的情况
                    results[platform] = f"错误: {str(e)}"
        
        return results