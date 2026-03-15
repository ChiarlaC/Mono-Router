"""
Content Orchestrator 使用示例

本示例展示了如何使用Content Orchestrator来处理视频转录文本，
并生成适合知乎、小红书和微信三个平台的内容。
"""

from main import BaseOrchestrator, ContentContent
from core.logic_engine import LogicEngine
from core.rewriter import StyleRewriter
from typing import Dict, Any
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

class ContentOrchestrator(BaseOrchestrator):
    """内容编排器的具体实现"""
    
    def __init__(self, api_key: str, config: Dict[str, Any] = None):
        super().__init__(config)
        self.logic_engine = LogicEngine(api_key=api_key)
        self.style_rewriter = StyleRewriter(api_key=api_key)
    
    def extract(self, input_data: str) -> str:
        """提取原始文本"""
        # 这里可以处理视频转录、文档解析等
        return input_data
    
    def analyze(self, raw_text: str) -> Dict[str, Any]:
        """分析内容，提取逻辑结构"""
        return self.logic_engine.extract_logic(raw_text)
    
    def rewrite(self, logic_data: Dict[str, Any]) -> Dict[str, str]:
        """重写内容，生成多平台版本"""
        return self.style_rewriter.parallel_rewrite(logic_data)
    
    def export(self, content: ContentContent) -> Dict[str, Any]:
        """导出内容"""
        return {
            "raw_text": content.raw_text,
            "logic_summary": content.logic_summary,
            "platform_content": content.rewritten_content
        }


def main():
    """主函数：演示如何使用Content Orchestrator"""
    
    print("开始执行Content Orchestrator...")
    
    # 1. 从环境变量中获取API密钥
    print("正在加载环境变量...")
    api_key = os.getenv("DEEPSEEK_API_KEY")
    print(f"API密钥长度: {len(api_key) if api_key else 0}")
    
    if not api_key:
        raise Exception("请在.env文件中设置DEEPSEEK_API_KEY环境变量")
    
    # 2. 初始化编排器
    print("正在初始化编排器...")
    orchestrator = ContentOrchestrator(api_key=api_key)
    print("编排器初始化完成")
    
    # 3. 准备输入文本（可以是视频转录、文档内容等）
    input_text = """
    人工智能正在深刻改变我们的生活方式。
    从智能手机到自动驾驶汽车，AI技术已经渗透到日常生活的方方面面。
    根据最新研究，到2030年，AI将为全球经济贡献超过15万亿美元。
    然而，AI的发展也带来了伦理和就业方面的挑战。
    我们需要在推动技术进步的同时，确保AI的发展符合人类的价值观和利益。
    """
    
    # 3. 准备输入文本（可以是视频转录、文档内容等）
    input_text = """
    人工智能正在深刻改变我们的生活方式。
    从智能手机到自动驾驶汽车，AI技术已经渗透到日常生活的方方面面。
    根据最新研究，到2030年，AI将为全球经济贡献超过15万亿美元。
    然而，AI的发展也带来了伦理和就业方面的挑战。
    我们需要在推动技术进步的同时，确保AI的发展符合人类的价值观和利益。
    """
    print(f"输入文本长度: {len(input_text)} 字符")
    
    # 4. 运行完整的工作流程
    try:
        print("开始执行工作流程...")
        content = orchestrator.run(input_text)
        print("工作流程执行完成")
        
        # 5. 查看结果
        print("\n=== 原始文本 ===")
        print(content.raw_text[:200] + "...")
        
        print("\n=== 逻辑摘要 ===")
        print(f"核心洞察: {content.logic_summary.get('key_insights', [])}")
        print(f"数据点: {content.logic_summary.get('data_points', {})}")
        
        print("\n=== 知乎版本 ===")
        print(content.rewritten_content.get('zhihu', '生成失败')[:300] + "...")
        
        print("\n=== 小红书版本 ===")
        print(content.rewritten_content.get('xhs', '生成失败')[:300] + "...")
        
        print("\n=== 微信版本 ===")
        print(content.rewritten_content.get('wechat', '生成失败')[:300] + "...")
        
    except Exception as e:
        print(f"处理过程中发生错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
