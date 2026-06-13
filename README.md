# 🎯 Offer 捕手 — AI 求职智能匹配体

## 项目简介

面向在校大学生的 AI 求职匹配智能体，帮助学生快速匹配合适岗位并优化简历命中率。

**核心功能：**
- 📝 **简历上传与解析** — 支持粘贴/上传，AI 自动提取技能、学历、经验等结构化信息
- 🔍 **岗位浏览与筛选** — 12个真实互联网企业校招岗位，按公司筛选
- 🎯 **智能匹配评分** — Claude AI 对简历与每个岗位进行多维度匹配打分
- ✨ **简历优化建议** — 针对目标岗位的逐项优化方案（技能、项目、格式等）

## 技术栈

| 层 | 技术 |
|------|------|
| 前端 | HTML5 + Tailwind CSS + Vanilla JS |
| 后端 | Python FastAPI |
| AI | Claude API (Sonnet 4) |
| 部署 | Render / 本地运行 |

## 本地运行

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=your_key_here   # 可选，无Key则使用Demo模式
python app.py
# 浏览器打开 http://localhost:8000
```

## 项目结构

```
offer-hunter/
├── app.py                      # FastAPI 主程序
├── services/
│   ├── claude_service.py       # Claude AI 集成
│   └── jobs_data.py            # 岗位数据（12个岗位）
├── templates/
│   └── index.html              # 前端界面
├── static/                     # 静态资源
├── requirements.txt
└── render.yaml                 # Render 部署配置
```

## License

MIT
