import json
import concurrent.futures
import time
from typing import Dict, Any
from openai import OpenAI
from .base import BaseEngine
from ..config import get_settings
from ..prompts import PROMPTS


class StyleEngine(BaseEngine):
    def __init__(self, client: OpenAI = None):
        if client is None:
            settings = get_settings()
            client = OpenAI(
                api_key=settings.DEEPSEEK_API_KEY,
                base_url=settings.DEEPSEEK_BASE_URL
            )
        super().__init__(client)
        self.settings = get_settings()
    
    def process(self, input_data: Dict[str, Any]) -> Dict[str, str]:
        return self.parallel_rewrite(input_data)
    
    def parallel_rewrite(self, logic_data: Dict[str, Any]) -> Dict[str, str]:
        platforms = ["zhihu", "xhs", "wechat"]
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            future_to_platform = {
                executor.submit(self._rewrite_single, platform, logic_data): platform
                for platform in platforms
            }
            
            for future in concurrent.futures.as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    results[platform] = future.result()
                except Exception as e:
                    results[platform] = f"错误: {str(e)}"
        
        return results
    
    def _rewrite_single(self, platform: str, logic_data: Dict[str, Any]) -> str:
        if platform not in PROMPTS:
            raise ValueError(f"不支持的平台: {platform}")
        
        system_prompt = PROMPTS[platform]
        max_retries = self.settings.API_MAX_RETRIES
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = self.client.chat.completions.create(
                    model=self.settings.DEEPSEEK_MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": json.dumps(logic_data, ensure_ascii=False)}
                    ],
                    timeout=self.settings.API_TIMEOUT
                )
                
                return response.choices[0].message.content
            except Exception as e:
                retry_count += 1
                if retry_count >= max_retries:
                    raise Exception(f"为{platform}重写内容时发生错误: {str(e)}")
                time.sleep(2 ** retry_count)  # 指数退避