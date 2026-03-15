# Content Orchestrator 架构说明

## 项目结构

```
Content Orchestrator/
├── src/                    # 源代码目录
│   ├── orchestrator/        # 编排器模块
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
├── requirements.txt      # 依赖文件
└── README.md           # 项目说明
```

## 模块说明

### 1. Config模块 (src/config/)
- **settings.py**: 使用pydantic-settings管理配置，支持环境变量
- **功能**: 统一管理API密钥、超时设置等配置

### 2. Engines模块 (src/engines/)
- **base.py**: 定义基础引擎接口
- **logic.py**: 逻辑提取引擎，从文本中提取结构化信息
- **style.py**: 风格变换引擎，为不同平台生成适配内容

### 3. Orchestrator模块 (src/orchestrator/)
- **base.py**: 定义基础编排器接口和工作流程
- **content.py**: 内容编排器实现，协调各个引擎完成内容处理

### 4. Prompts模块 (src/prompts.py)
- 定义各平台的系统提示模板
- 支持知乎、小红书、微信等平台

## 设计原则

1. **模块化**: 每个模块职责单一，便于维护和扩展
2. **可扩展**: 基于接口设计，易于添加新的引擎和平台
3. **配置化**: 使用环境变量管理配置，避免硬编码
4. **类型安全**: 使用pydantic进行数据验证
5. **异步处理**: 支持并行处理多个平台的内容生成

## 使用方法

### 基础使用

```python
from src import ContentOrchestrator

orchestrator = ContentOrchestrator()
content = orchestrator.run(input_text)

print(content.logic_summary)
print(content.rewritten_content['zhihu'])
print(content.rewritten_content['xhs'])
print(content.rewritten_content['wechat'])
```

### 自定义引擎

```python
from src.engines import BaseEngine
from openai import OpenAI

class CustomEngine(BaseEngine):
    def process(self, input_data):
        # 自定义处理逻辑
        pass
```

### 自定义编排器

```python
from src.orchestrator import BaseOrchestrator

class CustomOrchestrator(BaseOrchestrator):
    def extract(self, input_data):
        # 自定义提取逻辑
        pass
    
    def analyze(self, raw_text):
        # 自定义分析逻辑
        pass
    
    def rewrite(self, logic_data):
        # 自定义重写逻辑
        pass
    
    def export(self, content):
        # 自定义导出逻辑
        pass
```

## 扩展指南

### 添加新的平台支持

1. 在 `src/prompts.py` 中添加新的平台提示
2. 在 `src/engines/style.py` 中更新平台列表
3. 测试新平台的内容生成效果

### 添加新的引擎

1. 继承 `BaseEngine` 类
2. 实现 `process` 方法
3. 在编排器中集成新引擎

### 添加新的配置项

1. 在 `src/config/settings.py` 中添加新的配置字段
2. 在 `.env` 文件中设置对应的值
3. 使用 `get_settings()` 获取配置

## 优势

1. **清晰的架构**: 模块职责明确，易于理解和维护
2. **高度可扩展**: 基于接口设计，便于添加新功能
3. **配置灵活**: 支持环境变量，便于不同环境部署
4. **类型安全**: 使用pydantic进行数据验证
5. **性能优化**: 支持并行处理，提高效率