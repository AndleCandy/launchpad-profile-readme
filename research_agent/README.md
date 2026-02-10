# Research Agent (自主研究智能体)

一个基于 LangGraph 的自主研究智能体，能够自动规划、搜索、引用来源，并输出带引用的完整报告。

An autonomous research agent built with LangGraph that can plan, search, cite sources, and generate comprehensive reports with citations.

## 功能特性 (Features)

- **自主规划 (Autonomous Planning)**: 根据研究主题自动生成研究计划
- **多工具搜索 (Multi-Tool Search)**: 使用多种工具搜索和收集信息
- **引用追踪 (Citation Tracking)**: 自动追踪和管理所有信息来源
- **报告生成 (Report Generation)**: 生成带完整引用的研究报告
- **工作流编排 (Workflow Orchestration)**: 使用 LangGraph 进行状态管理和流程控制

## 核心技术栈 (Tech Stack)

- **LangGraph**: 工作流编排和状态管理
- **LangChain**: 工具调用和集成
- **Python 3.9+**: 主要开发语言
- **Pydantic**: 数据验证和类型定义

## 架构设计 (Architecture)

```
研究查询 (Research Query)
    ↓
规划节点 (Planning Node)
    ↓
搜索节点 (Search Node) ←---┐
    ↓                      |
决策 (Decision)             |
    ├→ 继续搜索 ───────────┘
    ↓
合成节点 (Synthesis Node)
    ↓
最终报告 (Final Report)
```

### 工作流程 (Workflow)

1. **Planning Node**: 分析研究查询并创建详细的研究计划
2. **Search Node**: 执行搜索、收集信息、追踪引用（可重复）
3. **Synthesis Node**: 整合所有信息生成带引用的完整报告

## 安装 (Installation)

```bash
# 克隆仓库
git clone <repository-url>
cd launchpad-profile-readme

# 安装依赖
pip install -r requirements.txt

# 或使用 pyproject.toml
pip install -e .
```

## 使用方法 (Usage)

### 基础用法 (Basic Usage)

```python
from research_agent.agent import create_research_agent

# 创建研究智能体
agent = create_research_agent()

# 执行研究
results = agent.research("What is LangGraph and how does it work?")

# 获取报告
print(results["report"])

# 查看引用
for citation in results["citations"]:
    print(f"{citation['source_id']} {citation['title']}")
```

### 运行示例 (Run Example)

```bash
# 运行基础示例
python examples/basic_usage.py
```

## 项目结构 (Project Structure)

```
research_agent/
├── __init__.py           # 包初始化
├── agent.py              # 主研究智能体和 LangGraph 工作流
├── state.py              # 状态定义
├── nodes.py              # 工作流节点函数
├── tools/                # 研究工具
│   ├── __init__.py
│   └── research_tools.py # Web 搜索、文档阅读等工具
└── utils/                # 实用工具
    ├── __init__.py
    └── citation.py       # 引用管理

examples/
└── basic_usage.py        # 使用示例
```

## 核心组件 (Core Components)

### 1. 状态管理 (State Management)

使用 `ResearchState` TypedDict 管理整个研究流程的状态：

```python
class ResearchState(TypedDict):
    query: str                    # 研究查询
    plan: List[str]               # 研究计划
    current_step: int             # 当前步骤
    messages: List[Dict]          # 消息历史
    collected_info: List[str]     # 收集的信息
    citations: List[Citation]     # 引用列表
    report: str                   # 最终报告
    is_complete: bool             # 是否完成
```

### 2. 研究工具 (Research Tools)

- **WebSearchTool**: 网络搜索工具
- **DocumentReaderTool**: 文档阅读工具
- **WikipediaTool**: Wikipedia 搜索工具

### 3. 引用管理 (Citation Management)

`CitationManager` 类负责：
- 添加新引用
- 生成引用 ID
- 格式化引用列表
- 追踪所有来源

### 4. 工作流节点 (Workflow Nodes)

- **planning_node**: 创建研究计划
- **search_node**: 执行搜索和信息收集
- **synthesis_node**: 合成最终报告
- **should_continue**: 决策函数

## 扩展功能 (Extensions)

### 添加新工具 (Adding New Tools)

在 `research_agent/tools/research_tools.py` 中添加新工具：

```python
class CustomTool:
    def __init__(self):
        self.name = "custom_tool"
        self.description = "Description of what this tool does"
    
    def execute(self, *args, **kwargs):
        # Tool implementation
        pass
```

### 自定义节点 (Custom Nodes)

在 `research_agent/nodes.py` 中添加自定义节点：

```python
def custom_node(state: ResearchState) -> ResearchState:
    # Node implementation
    return state
```

然后在 `agent.py` 中集成到工作流。

## 配置 (Configuration)

### 环境变量 (Environment Variables)

创建 `.env` 文件：

```bash
# OpenAI API (如果使用 LLM 增强功能)
OPENAI_API_KEY=your-api-key-here

# 搜索 API (如果使用真实搜索)
SEARCH_API_KEY=your-search-api-key
```

## 最佳实践 (Best Practices)

1. **模块化设计**: 每个工具和节点都是独立的，易于测试和维护
2. **状态不可变**: 使用 TypedDict 确保状态结构清晰
3. **引用追踪**: 所有信息都关联到来源
4. **错误处理**: 每个节点都应该处理潜在错误
5. **异步支持**: 提供异步接口以支持高并发场景

## 未来计划 (Roadmap)

- [ ] 集成真实的搜索 API (Google, Bing, Tavily)
- [ ] 添加 LLM 增强的规划和合成
- [ ] 支持多语言研究
- [ ] 添加可视化界面
- [ ] 实现缓存机制
- [ ] 支持流式输出
- [ ] 添加更多研究工具

## 参考资料 (References)

- [LangGraph Documentation](https://python.langchain.com/docs/langgraph)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [@langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)

## 许可证 (License)

CC-BY-4.0 License

## 贡献 (Contributing)

欢迎提交 Issue 和 Pull Request！

## 联系方式 (Contact)

如有问题，请通过 GitHub Issues 联系。
