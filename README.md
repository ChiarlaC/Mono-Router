# Content Orchestrator 使用指南

## 项目概述

Content Orchestrator是一个Python项目，用于将原始输入（视频转录或文档）处理成适合多个平台（知乎、小红书、微信）的内容。

## 项目结构

```
Content Orchestrator/
├── src/                    # 源代码目录
│   ├── orchestrator/       # 编排器模块
│   │   ├── base.py        # 基础编排器类
│   │   └── content.py    # 内容编排器实现
│   ├── engines/           # 引擎模块
│   │   ├── base.py       # 基础引擎类
│   │   ├── logic.py      # 逻辑提取引擎
│   │   └── style.py      # 风格变换引擎
│   ├── config/            # 配置模块
│   │   └── settings.py   # 配置管理
│   ├── prompts.py         # 提示模板
│   └── __init__.py       # 包初始化
├── examples/             # 示例代码
│   └── basic_usage.py    # 基础使用示例
├── tests/               # 测试文件
├── config/              # 配置文件目录
├── .env                # 环境变量
├── app.py              # Web UI应用
├── requirements.txt      # 依赖文件
└── README.md           # 本文件
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 方法1: 使用Web界面（推荐）

运行Web UI应用：

```bash
python app.py
```

然后打开浏览器访问 `http://localhost:7860` 即可使用图形界面。

**界面功能**:
- 左侧大文本框：粘贴原始文本
- "生成多平台内容"按钮：点击开始处理
- 右侧三个标签页：分别显示知乎、小红书、微信版本的内容

### 方法2: 编程使用

```python
from src import ContentOrchestrator

# 初始化编排器
orchestrator = ContentOrchestrator()

# 处理文本
raw_text = "你的输入文本..."
content = orchestrator.run(raw_text)

# 查看结果
print(content.logic_summary)           # 逻辑摘要
print(content.rewritten_content['zhihu'])   # 知乎版本
print(content.rewritten_content['xhs'])     # 小红书版本
print(content.rewritten_content['wechat'])  # 微信版本
```

### 方法3: 运行示例

```bash
python examples/basic_usage.py
```

## 配置说明

在 `.env` 文件中配置以下环境变量：

```
DEEPSEEK_API_KEY=your_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL_NAME=deepseek-chat
```

## 平台风格特点

### 知乎
- 深度分析，逻辑推理
- 专业术语，学术风格
- 结构清晰，语言正式

### 小红书
- 情感共鸣，简洁句子
- 高emoji密度（每50字1-2个emoji）
- 口语化语气，视觉化描述

### 微信
- 叙事结构，品牌声音
- 开头吸引，结尾有力
- 结构合理，语言流畅

## 扩展开发

### 添加新平台支持

1. 在 `src/prompts.py` 中添加新的平台提示
2. 在 `src/engines/style.py` 中更新平台列表
3. 测试新平台的内容生成效果

### 自定义引擎

```python
from src.engines import BaseEngine

class CustomEngine(BaseEngine):
    def process(self, input_data):
        # 自定义处理逻辑
        pass
```

## 注意事项

1. **API密钥**：需要有效的DeepSeek API密钥
2. **网络连接**：需要稳定的网络连接以调用API
3. **错误处理**：系统已内置重试机制和错误处理
4. **并发限制**：并行重写时会同时发起3个API请求

## 技术栈

- **数据验证**: pydantic, pydantic-settings
- **API调用**: openai (支持DeepSeek等兼容API)
- **配置管理**: python-dotenv
- **Web UI**: Gradio
- **并发处理**: concurrent.futures

## 运行测试

```bash
python -m unittest tests.test_logic_engine
```