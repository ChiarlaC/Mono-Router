from pydantic import BaseModel, Field
from typing import Dict, Optional, Any

class ContentContent(BaseModel):
    raw_text: str = Field(..., description="原始文本输入")
    logic_summary: Dict[str, Any] = Field(default_factory=dict, description="结构化洞察")
    rewritten_content: Dict[str, str] = Field(default_factory=dict, description="平台特定输出")

class BaseOrchestrator:
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
    
    def extract(self, input_data: Any) -> str:
        """处理输入数据，提取原始文本"""
        raise NotImplementedError("子类必须实现extract方法")
    
    def analyze(self, raw_text: str) -> Dict[str, Any]:
        """分析内容，生成结构化洞察"""
        raise NotImplementedError("子类必须实现analyze方法")
    
    def rewrite(self, logic_data: Dict[str, Any]) -> Dict[str, str]:
        """根据平台要求重写内容"""
        raise NotImplementedError("子类必须实现rewrite方法")
    
    def export(self, content: ContentContent) -> Dict[str, Any]:
        """导出平台特定格式的内容"""
        raise NotImplementedError("子类必须实现export方法")
    
    def run(self, input_data: Any) -> ContentContent:
        """执行完整的工作流程"""
        # 1. 提取原始文本
        raw_text = self.extract(input_data)
        
        # 2. 分析内容
        logic_summary = self.analyze(raw_text)
        
        # 3. 重写内容
        rewritten_content = self.rewrite(logic_summary)
        
        # 4. 构建内容对象
        content = ContentContent(
            raw_text=raw_text,
            logic_summary=logic_summary,
            rewritten_content=rewritten_content
        )
        
        # 5. 导出
        self.export(content)
        
        return content