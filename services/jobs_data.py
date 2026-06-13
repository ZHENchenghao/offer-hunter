"""模拟岗位数据 — 真实互联网企业校招/实习岗位"""

JOBS = [
    {
        "id": 1,
        "company": "腾讯",
        "title": "AI应用开发工程师（校招）",
        "department": "CSIG云与智慧产业事业群",
        "location": "深圳",
        "salary": "25-40K·16薪",
        "tags": ["Python", "LLM", "RAG", "Agent", "FastAPI"],
        "desc": "负责腾讯云AI产品的应用层开发，包括大模型Agent框架、RAG检索增强生成系统、多模态应用等。参与从0到1的AI产品孵化。",
        "requirements": [
            "计算机相关专业本科及以上学历",
            "精通Python，熟悉FastAPI/Flask等Web框架",
            "了解LLM原理，有Prompt Engineering经验",
            "熟悉向量数据库（Milvus/Pinecone/Chroma）优先",
            "有AI应用项目经验者优先"
        ],
        "match_weight": {"skills": 0.4, "experience": 0.3, "education": 0.15, "projects": 0.15}
    },
    {
        "id": 2,
        "company": "字节跳动",
        "title": "后端开发工程师-抖音电商",
        "department": "电商业务",
        "location": "北京",
        "salary": "30-50K·15薪",
        "tags": ["Go", "微服务", "MySQL", "Redis", "Kafka"],
        "desc": "负责抖音电商核心交易链路的后端开发，包括商品、订单、支付、物流等核心域。参与高并发系统设计与性能优化。",
        "requirements": [
            "计算机相关专业，本科及以上学历",
            "精通Go或Java，熟悉微服务架构",
            "熟悉MySQL、Redis等常用存储",
            "有高并发系统经验优先",
            "热爱技术，有较强的学习能力"
        ],
        "match_weight": {"skills": 0.35, "experience": 0.35, "education": 0.1, "projects": 0.2}
    },
    {
        "id": 3,
        "company": "阿里巴巴",
        "title": "数据科学家-淘宝推荐",
        "department": "淘天集团",
        "location": "杭州",
        "salary": "28-45K·16薪",
        "tags": ["Python", "SQL", "机器学习", "推荐系统", "Spark"],
        "desc": "负责淘宝首页推荐算法的数据分析与特征工程，通过A/B实验驱动推荐策略优化，提升用户转化率和GMV。",
        "requirements": [
            "统计学/数学/计算机相关专业硕士及以上",
            "精通Python和SQL",
            "熟悉常用机器学习算法",
            "有推荐系统或广告系统经验优先",
            "具备良好的数据敏感度"
        ],
        "match_weight": {"skills": 0.35, "experience": 0.3, "education": 0.2, "projects": 0.15}
    },
    {
        "id": 4,
        "company": "小红书",
        "title": "前端开发工程师-社区",
        "department": "社区技术部",
        "location": "上海",
        "salary": "25-40K·15薪",
        "tags": ["React", "TypeScript", "Next.js", "Node.js", "CSS"],
        "desc": "负责小红书社区前端开发，包括笔记发布、信息流、搜索等核心功能。参与前端基础设施建设与性能优化。",
        "requirements": [
            "计算机相关专业本科及以上",
            "精通React和TypeScript",
            "熟悉Next.js/Vite等构建工具",
            "有移动端开发经验优先",
            "对UI/UX有追求"
        ],
        "match_weight": {"skills": 0.4, "experience": 0.3, "education": 0.1, "projects": 0.2}
    },
    {
        "id": 5,
        "company": "美团",
        "title": "算法工程师-到店推荐",
        "department": "到店事业群",
        "location": "北京",
        "salary": "30-45K·15薪",
        "tags": ["深度学习", "推荐算法", "Python", "TensorFlow", "PyTorch"],
        "desc": "负责美团到店业务的推荐算法研发，包括POI推荐、搜索排序、用户画像等方向。",
        "requirements": [
            "计算机/AI相关专业硕士及以上",
            "精通深度学习框架（PyTorch/TensorFlow）",
            "有推荐/搜索/广告方向研究或实习经验",
            "在顶会发表论文者优先",
            "coding能力强"
        ],
        "match_weight": {"skills": 0.3, "experience": 0.35, "education": 0.2, "projects": 0.15}
    },
    {
        "id": 6,
        "company": "华为",
        "title": "云计算开发工程师",
        "department": "华为云BU",
        "location": "深圳",
        "salary": "22-35K·14薪",
        "tags": ["Java", "Kubernetes", "Docker", "微服务", "Linux"],
        "desc": "负责华为云PaaS平台开发，参与云原生技术栈建设，包括容器编排、服务网格、Serverless等方向。",
        "requirements": [
            "计算机相关专业本科及以上",
            "扎实的Java编程基础",
            "熟悉Docker/Kubernetes生态",
            "了解Linux内核原理优先",
            "有开源贡献者优先"
        ],
        "match_weight": {"skills": 0.35, "experience": 0.3, "education": 0.15, "projects": 0.2}
    },
    {
        "id": 7,
        "company": "腾讯",
        "title": "产品经理培训生-微信",
        "department": "WXG微信事业群",
        "location": "广州",
        "salary": "20-30K·16薪",
        "tags": ["产品设计", "用户研究", "数据分析", "Axure", "SQL"],
        "desc": "微信产品经理培训生项目，轮岗参与微信支付、视频号、小程序等核心产品策划与迭代。",
        "requirements": [
            "不限专业，本科及以上学历",
            "有较强的逻辑思维和用户洞察力",
            "有产品实习经验或创业经历优先",
            "数据分析能力强者加分",
            "对社交产品有热情"
        ],
        "match_weight": {"skills": 0.25, "experience": 0.3, "education": 0.2, "projects": 0.25}
    },
    {
        "id": 8,
        "company": "百度",
        "title": "NLP算法工程师-文心一言",
        "department": "百度AI",
        "location": "北京",
        "salary": "30-45K·16薪",
        "tags": ["NLP", "Transformer", "PyTorch", "Python", "大模型"],
        "desc": "参与文心一言大模型的研发与优化，包括SFT、RLHF、模型评估、推理加速等方向。",
        "requirements": [
            "AI/计算机相关专业硕士及以上",
            "深入理解Transformer架构",
            "有大模型训练/微调经验",
            "熟悉分布式训练框架",
            "有ACL/EMNLP等顶会论文优先"
        ],
        "match_weight": {"skills": 0.3, "experience": 0.35, "education": 0.2, "projects": 0.15}
    },
    {
        "id": 9,
        "company": "拼多多",
        "title": "全栈开发工程师-Temu",
        "department": "Temu国际业务",
        "location": "上海",
        "salary": "28-45K·16薪",
        "tags": ["Java", "React", "Spring Boot", "MySQL", "微服务"],
        "desc": "负责Temu海外电商平台的全栈开发，参与从供应链到用户端全链路系统建设。",
        "requirements": [
            "计算机相关专业本科及以上",
            "Java和React都有实际项目经验",
            "熟悉Spring Boot全家桶",
            "英语读写能力良好",
            "有电商项目经验优先"
        ],
        "match_weight": {"skills": 0.35, "experience": 0.3, "education": 0.15, "projects": 0.2}
    },
    {
        "id": 10,
        "company": "京东",
        "title": "测试开发工程师",
        "department": "零售技术",
        "location": "北京",
        "salary": "20-35K·16薪",
        "tags": ["Python", "自动化测试", "Selenium", "CI/CD", "Linux"],
        "desc": "负责京东零售核心链路的测试开发，建设自动化测试框架和持续集成流水线。",
        "requirements": [
            "计算机相关专业本科及以上",
            "精通至少一门编程语言（Python/Java）",
            "了解自动化测试框架",
            "有CI/CD实践经验优先",
            "细心且有质量意识"
        ],
        "match_weight": {"skills": 0.3, "experience": 0.3, "education": 0.15, "projects": 0.25}
    },
    {
        "id": 11,
        "company": "蔚来",
        "title": "智能座舱AI产品经理",
        "department": "数字座舱部",
        "location": "上海",
        "salary": "25-40K·14薪",
        "tags": ["AI产品", "车载交互", "语音助手", "用户研究", "PRD"],
        "desc": "负责蔚来智能座舱AI助手的产品设计与迭代，定义车载场景下的人机交互体验。",
        "requirements": [
            "本科及以上学历，不限专业",
            "对AI产品有深入理解",
            "有车载或IoT产品经验优先",
            "优秀的跨部门沟通能力",
            "热爱汽车和科技"
        ],
        "match_weight": {"skills": 0.25, "experience": 0.3, "education": 0.2, "projects": 0.25}
    },
    {
        "id": 12,
        "company": "网易",
        "title": "游戏AI工程师",
        "department": "网易互娱",
        "location": "广州",
        "salary": "25-40K·16薪",
        "tags": ["强化学习", "Python", "游戏AI", "Unity", "C++"],
        "desc": "负责网易游戏AI研发，包括NPC行为树、强化学习Boss AI、游戏内容自动生成等方向。",
        "requirements": [
            "计算机/AI相关专业硕士及以上",
            "熟悉强化学习或行为树算法",
            "有Unity/Unreal使用经验",
            "热爱游戏",
            "有Game AI项目经验优先"
        ],
        "match_weight": {"skills": 0.3, "experience": 0.3, "education": 0.2, "projects": 0.2}
    }
]
