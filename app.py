import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from src import ContentOrchestrator


def generate_content(raw_text, progress=gr.Progress()):
    """生成多平台内容，带进度显示"""
    if not raw_text.strip():
        return "请输入内容", "请输入内容", "请输入内容", "请输入内容"
    
    try:
        progress(0, desc="正在初始化...")
        orchestrator = ContentOrchestrator()
        
        progress(0.2, desc="正在提取逻辑结构...")
        logic_data = orchestrator.analyze(raw_text)
        
        progress(0.4, desc="正在生成知乎版本...")
        zhihu_content = orchestrator.style_engine._rewrite_single("zhihu", logic_data)
        
        progress(0.6, desc="正在生成小红书版本...")
        xhs_content = orchestrator.style_engine._rewrite_single("xhs", logic_data)
        
        progress(0.8, desc="正在生成公众号版本...")
        wechat_html = orchestrator.style_engine._rewrite_single("wechat", logic_data)
        
        progress(1.0, desc="完成!")
        
        return zhihu_content, xhs_content, wechat_html, wechat_html
    except Exception as e:
        error_msg = f"处理过程中发生错误: {str(e)}"
        return error_msg, error_msg, error_msg, error_msg


def create_ui():
    """创建Gradio界面"""
    with gr.Blocks(title="Content Orchestrator - 多平台内容生成器") as demo:
        gr.Markdown("# Content Orchestrator")
        gr.Markdown("将您的文本转换为知乎、小红书和公众号的内容格式")
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 输入")
                input_text = gr.Textbox(
                    label="原始文本",
                    placeholder="在此粘贴您的文章、视频转录文本或其他内容...",
                    lines=10
                )
                generate_btn = gr.Button("生成多平台内容", variant="primary")
                
                gr.Markdown("---")
                gr.Markdown("💡 **提示**:")
                gr.Markdown("- 处理时间约1-3分钟")
                gr.Markdown("- 确保在.env文件中配置了DEEPSEEK_API_KEY")
            
            with gr.Column(scale=2):
                gr.Markdown("### 输出")
                with gr.Tabs():
                    with gr.TabItem("知乎"):
                        zhihu_output = gr.Textbox(
                            label="知乎版本",
                            lines=15,
                            max_lines=30,
                            interactive=False,
                            autoscroll=False
                        )
                    with gr.TabItem("小红书"):
                        xhs_output = gr.Textbox(
                            label="小红书版本",
                            lines=15,
                            max_lines=30,
                            interactive=False,
                            autoscroll=False
                        )
                    with gr.TabItem("公众号"):
                        with gr.Row():
                            gr.Markdown("**公众号版本（HTML格式）- 直接复制到公众号编辑器**")
                        wechat_html_output = gr.Code(
                            label="HTML代码（点击复制按钮一键复制）",
                            language="html",
                            lines=15
                        )
                        with gr.Row():
                            gr.Markdown("**预览效果**")
                        wechat_preview = gr.HTML(label="预览")
        
        # 绑定按钮点击事件
        generate_btn.click(
            fn=generate_content,
            inputs=input_text,
            outputs=[zhihu_output, xhs_output, wechat_html_output, wechat_preview]
        )
    
    return demo


if __name__ == "__main__":
    demo = create_ui()
    demo.launch(share=False, inbrowser=True)
