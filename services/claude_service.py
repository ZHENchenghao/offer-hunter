"""Claude API 服务 — 简历匹配 + 优化建议"""

import json
import os
from typing import Optional

# 尝试导入 anthropic SDK
try:
    from anthropic import Anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def _get_client() -> Optional[object]:
    """获取 Claude 客户端"""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key or not HAS_ANTHROPIC:
        return None
    return Anthropic(api_key=api_key)


def _call_claude(system_prompt: str, user_message: str, max_tokens: int = 2000) -> Optional[str]:
    """通用 Claude 调用"""
    client = _get_client()
    if client is None:
        return None
    try:
        msg = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        return msg.content[0].text
    except Exception as e:
        print(f"[ClaudeService] API 调用失败: {e}")
        return None


def match_resume_to_jobs(resume_text: str, jobs: list) -> dict:
    """将简历与所有岗位进行匹配打分"""
    client = _get_client()
    if client is None:
        return _demo_match(resume_text, jobs)

    jobs_desc = "\n\n".join([
        f"[岗位{j['id']}] {j['company']} - {j['title']}\n"
        f"标签: {', '.join(j['tags'])}\n"
        f"描述: {j['desc']}\n"
        f"要求: {'; '.join(j['requirements'])}"
        for j in jobs
    ])

    system_prompt = """你是一个资深HR和职业规划师。你的任务是根据候选人简历，评估其与多个岗位的匹配度。

返回纯JSON格式（不要markdown代码块）:
{
  "matches": [
    {
      "job_id": 1,
      "score": 85,
      "skill_match": "技能匹配分析（50字内）",
      "gap_analysis": "差距分析（50字内）",
      "highlights": ["亮点1", "亮点2"],
      "missing": ["缺失项1"]
    }
  ],
  "overall_advice": "整体求职建议（100字内）",
  "best_role": "最适合的岗位类型"
}

打分规则：
- 90-100: 高度匹配，简历可直接投递
- 75-89: 较好匹配，小幅优化后可投
- 60-74: 部分匹配，需要针对性优化
- 40-59: 匹配度一般，建议补充相关经验
- 低于40: 匹配度较低
"""

    user_message = f"候选人简历:\n{resume_text}\n\n---\n\n待匹配岗位:\n{jobs_desc}\n\n请为每个岗位返回匹配分析。只返回JSON。"

    result = _call_claude(system_prompt, user_message, max_tokens=3000)
    if result is None:
        return _demo_match(resume_text, jobs)

    try:
        # 清理可能的 markdown 标记
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1]
            if result.endswith("```"):
                result = result[:-3]
        return json.loads(result)
    except json.JSONDecodeError:
        return _demo_match(resume_text, jobs)


def optimize_resume_for_job(resume_text: str, job: dict) -> dict:
    """针对特定岗位给出简历优化建议"""
    client = _get_client()
    if client is None:
        return _demo_optimize(resume_text, job)

    system_prompt = """你是一个资深简历优化顾问，帮助候选人针对特定岗位优化简历。

返回纯JSON格式（不要markdown代码块）:
{
  "match_score": 75,
  "overall_assessment": "整体评价（50字）",
  "optimizations": [
    {
      "section": "简历模块名（如：技能、项目经历、实习经历）",
      "current_issue": "当前问题",
      "suggestion": "具体优化建议",
      "example": "优化后的示例写法（30字内）"
    }
  ],
  "keyword_suggestions": ["应添加的关键词1", "关键词2"],
  "format_tips": ["简历格式建议1"],
  "cover_letter_hint": "求职信一句话亮点建议"
}
"""

    job_desc = f"{job['company']} - {job['title']}\n标签: {', '.join(job['tags'])}\n描述: {job['desc']}\n要求: {'; '.join(job['requirements'])}"

    user_message = f"候选人简历:\n{resume_text}\n\n---\n\n目标岗位:\n{job_desc}\n\n请输出简历优化建议。只返回JSON。"

    result = _call_claude(system_prompt, user_message, max_tokens=2500)
    if result is None:
        return _demo_optimize(resume_text, job)

    try:
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1]
            if result.endswith("```"):
                result = result[:-3]
        return json.loads(result)
    except json.JSONDecodeError:
        return _demo_optimize(resume_text, job)


def extract_skills(resume_text: str) -> dict:
    """从简历中提取结构化技能信息"""
    client = _get_client()
    if client is None:
        return _demo_extract(resume_text)

    system_prompt = """你是一个简历解析专家。从简历文本中提取结构化信息。

返回纯JSON:
{
  "name": "推断的姓名",
  "education": {"level": "本科/硕士/博士", "school": "学校名", "major": "专业"},
  "skills": ["技能1", "技能2", ...],
  "years_of_experience": 数字,
  "target_role": "目标岗位类型",
  "strengths": ["核心优势1", "优势2"],
  "weaknesses": ["待提升点1"]
}
"""

    result = _call_claude(system_prompt, f"简历内容:\n{resume_text}\n\n请提取结构化信息。只返回JSON。", max_tokens=1000)
    if result is None:
        return _demo_extract(resume_text)

    try:
        result = result.strip()
        if result.startswith("```"):
            result = result.split("\n", 1)[1]
            if result.endswith("```"):
                result = result[:-3]
        return json.loads(result)
    except json.JSONDecodeError:
        return _demo_extract(resume_text)


# ===== 演示模式（无 API Key 时的fallback）=====

def _demo_match(resume_text: str, jobs: list) -> dict:
    """演示匹配结果"""
    import random
    rng = random.Random(hash(resume_text[:100]) % 2**32)

    matches = []
    for job in jobs:
        score = rng.randint(55, 95)
        matches.append({
            "job_id": job["id"],
            "score": score,
            "skill_match": f"你的技能与{job['title']}岗位有部分重叠" if score > 70 else f"与{job['title']}匹配度偏低，建议补充相关技能",
            "gap_analysis": "项目经验方向可进一步加强" if score < 80 else "整体匹配良好，简历表达可再优化",
            "highlights": ["技术栈匹配度较高", "有相关项目经验"] if score > 70 else ["学习能力强", "基础扎实"],
            "missing": [f"缺少{job['tags'][0]}深度实战经验"] if score < 80 else ["可补充更多量化成果"]
        })

    return {
        "matches": matches,
        "overall_advice": "建议优先投递匹配度75分以上的岗位，针对每个岗位微调简历中的项目描述和技能关键词。",
        "best_role": "AI应用开发工程师"
    }


def _demo_optimize(resume_text: str, job: dict) -> dict:
    """演示优化建议"""
    return {
        "match_score": 78,
        "overall_assessment": "你的技术基础不错，但简历对目标岗位的针对性不够，部分关键技能未突出展示。",
        "optimizations": [
            {
                "section": "技能概述",
                "current_issue": "技能罗列过于泛泛，缺少与岗位的对照",
                "suggestion": f"将{job['tags'][0]}、{job['tags'][1]}等岗位核心技能放在技能区首位",
                "example": f"精通{job['tags'][0]}，{job['tags'][1]}项目经验丰富"
            },
            {
                "section": "项目经历",
                "current_issue": "项目描述偏重技术细节，缺少业务价值量化",
                "suggestion": "用STAR法则重写：情境→任务→行动→结果，加入数据指标",
                "example": "通过优化推荐算法，将点击率从3.2%提升至5.8%（+81%）"
            },
            {
                "section": "实习经历",
                "current_issue": "实习描述过于简略",
                "suggestion": "补充在实习中的具体贡献和影响力",
                "example": "独立负责XX模块开发，支撑日均100w+请求"
            }
        ],
        "keyword_suggestions": job['tags'][:4],
        "format_tips": [
            "使用PDF格式投递，避免Word格式兼容问题",
            "文件名格式：姓名_学校_岗位_电话",
            "控制在一页内，重点突出与岗位相关的经验"
        ],
        "cover_letter_hint": f"表达对{job['company']}在{job['tags'][0]}方向技术积累的认可，并关联自己的项目经验"
    }


def _demo_extract(resume_text: str) -> dict:
    """演示技能提取"""
    return {
        "name": "张同学",
        "education": {"level": "硕士", "school": "某985高校", "major": "计算机科学与技术"},
        "skills": ["Python", "PyTorch", "SQL", "机器学习", "FastAPI", "Docker"],
        "years_of_experience": 2,
        "target_role": "AI/后端开发工程师",
        "strengths": ["AI项目经验丰富", "编程基础扎实", "有论文发表"],
        "weaknesses": ["缺少大厂实习经历", "系统设计经验不足"]
    }
