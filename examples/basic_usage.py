import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import ContentOrchestrator


def main():
    print("开始执行Content Orchestrator...")
    
    orchestrator = ContentOrchestrator()
    
    input_text = """
    人工智能正在深刻改变我们的生活方式。
    从智能手机到自动驾驶汽车，AI技术已经渗透到日常生活的方方面面。
    根据最新研究，到2030年，AI将为全球经济贡献超过15万亿美元。
    然而，AI的发展也带来了伦理和就业方面的挑战。
    我们需要在推动技术进步的同时，确保AI的发展符合人类的价值观和利益。
    """
    
    print(f"输入文本长度: {len(input_text)} 字符")
    
    try:
        print("开始执行工作流程...")
        content = orchestrator.run(input_text)
        print("工作流程执行完成")
        
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