"""Offer 捕手 — Gradio 版本（72小时公网链接）"""
import gradio as gr
from services.jobs_data import JOBS
from services.claude_service import match_resume_to_jobs, optimize_resume_for_job, extract_skills

JOBS_DICT = {f"{j['company']} — {j['title']} ({j['location']})": j for j in JOBS}
JOB_CHOICES = list(JOBS_DICT.keys())


def do_extract(resume):
    if not resume or len(resume.strip()) < 20:
        return "⚠️ 简历内容太少，请至少输入20字"
    r = extract_skills(resume.strip())
    return f"""## 🤖 AI 解析结果

| 维度 | 内容 |
|------|------|
| 👤 姓名 | {r.get('name', '未识别')} |
| 🎓 学历 | {r.get('education', {}).get('level', '')} · {r.get('education', {}).get('school', '')} · {r.get('education', {}).get('major', '')} |
| 🎯 目标方向 | {r.get('target_role', '')} · {r.get('years_of_experience', 0)}年经验 |
| 💪 技能 | {', '.join(r.get('skills', []))} |
| ✅ 优势 | {', '.join(r.get('strengths', []))} |
| ⚠️ 待提升 | {', '.join(r.get('weaknesses', []))} |
"""


def do_match(resume):
    if not resume or len(resume.strip()) < 20:
        return "⚠️ 请先填写简历（至少20字）"
    data = match_resume_to_jobs(resume.strip(), JOBS)
    matches = sorted(data.get('matches', []), key=lambda x: x['score'], reverse=True)

    lines = [f"## 🎯 智能匹配结果", f"", f"**AI 建议：** {data.get('overall_advice', '')}", f"**最佳方向：** 🏆 {data.get('best_role', '')}", f"", "---", ""]

    for i, m in enumerate(matches):
        emoji = "🟢" if m['score'] >= 80 else "🟡" if m['score'] >= 60 else "🔴"
        job = next((j for j in JOBS if j['id'] == m['job_id']), None)
        if not job:
            continue
        lines.append(f"### {emoji} #{i+1} [{m['score']}分] {job['company']} — {job['title']}")
        lines.append(f"📍 {job['location']} · 💰 {job['salary']}")
        lines.append(f"🔍 **技能匹配：** {m.get('skill_match', '')}")
        lines.append(f"📉 **差距分析：** {m.get('gap_analysis', '')}")
        lines.append(f"✅ 亮点：{'、'.join(m.get('highlights', []))}")
        lines.append(f"⚠️ 缺失：{'、'.join(m.get('missing', []))}")
        lines.append("")

    return '\n'.join(lines)


def do_optimize(resume, job_choice):
    if not resume or len(resume.strip()) < 20:
        return "⚠️ 请先填写简历（至少20字）"
    if not job_choice:
        return "⚠️ 请选择目标岗位"
    job = JOBS_DICT.get(job_choice)
    if not job:
        return "⚠️ 岗位不存在"
    data = optimize_resume_for_job(resume.strip(), job)

    lines = [
        f"## ✨ 简历优化建议",
        f"",
        f"| 维度 | 内容 |",
        f"|------|------|",
        f"| 🎯 匹配度 | **{data.get('match_score', '?')}/100** |",
        f"| 📝 整体评价 | {data.get('overall_assessment', '')} |",
        f"",
        f"### 逐项优化",
        f"",
    ]
    for i, opt in enumerate(data.get('optimizations', [])):
        lines.append(f"**{i+1}. {opt.get('section', '')}**")
        lines.append(f"- ❌ 当前问题：{opt.get('current_issue', '')}")
        lines.append(f"- 💡 优化建议：{opt.get('suggestion', '')}")
        lines.append(f"- ✨ 示例：*\"{opt.get('example', '')}\"*")
        lines.append("")

    lines.append("### 🏷️ 关键词建议")
    lines.append(' | '.join(data.get('keyword_suggestions', [])))
    lines.append("")
    lines.append("### 📐 格式建议")
    for t in data.get('format_tips', []):
        lines.append(f"- {t}")
    lines.append(f"")
    lines.append(f"### 💌 求职信建议")
    lines.append(f"> {data.get('cover_letter_hint', '')}")

    return '\n'.join(lines)


# ===== 构建 Gradio UI =====
with gr.Blocks(title="Offer 捕手 — AI 求职智能匹配体") as demo:
    gr.Markdown("""
    # 🎯 Offer 捕手 — AI 求职智能匹配体
    ### 上传简历 → AI秒级分析 → 精准岗位匹配 + 简历优化建议
    """)

    with gr.Tabs():
        # Tab 1: 简历上传 + 解析
        with gr.TabItem("📝 上传简历"):
            gr.Markdown("粘贴简历文本，AI 自动提取关键信息")
            resume_input = gr.Textbox(
                label="简历内容",
                placeholder="粘贴你的简历...\n\n姓名：张同学\n学校：XX大学 计算机 硕士\n技能：Python, PyTorch, FastAPI...",
                lines=12,
            )
            with gr.Row():
                btn_extract = gr.Button("🤖 AI 解析简历", variant="primary")
                btn_match_from_resume = gr.Button("🎯 一键匹配岗位", variant="secondary")
            extract_output = gr.Markdown(label="解析结果")

            btn_extract.click(fn=do_extract, inputs=resume_input, outputs=extract_output)

        # Tab 2: 岗位浏览
        with gr.TabItem("🔍 岗位浏览"):
            gr.Markdown("### 12大厂真实校招岗位")
            gr.Dataframe(
                headers=["公司", "岗位", "地点", "薪资", "标签"],
                value=[[j['company'], j['title'], j['location'], j['salary'], ', '.join(j['tags'][:4])] for j in JOBS],
                interactive=False,
                row_count=12,
            )

        # Tab 3: 智能匹配
        with gr.TabItem("🎯 智能匹配"):
            gr.Markdown("AI 逐岗位打分，输出匹配报告")
            resume_match = gr.Textbox(label="简历内容", lines=8, placeholder="粘贴简历...")
            btn_match = gr.Button("🎯 开始匹配", variant="primary", size="lg")
            match_output = gr.Markdown(label="匹配报告")
            btn_match.click(fn=do_match, inputs=resume_match, outputs=match_output)
            btn_match_from_resume.click(fn=do_match, inputs=resume_input, outputs=match_output)

        # Tab 4: 简历优化
        with gr.TabItem("✨ 简历优化"):
            gr.Markdown("针对目标岗位的逐项优化建议")
            resume_opt = gr.Textbox(label="简历内容", lines=8, placeholder="粘贴简历...")
            job_select = gr.Dropdown(label="选择目标岗位", choices=JOB_CHOICES, interactive=True)
            btn_optimize = gr.Button("✨ 获取优化建议", variant="primary", size="lg")
            opt_output = gr.Markdown(label="优化方案")
            btn_optimize.click(fn=do_optimize, inputs=[resume_opt, job_select], outputs=opt_output)

    gr.Markdown("---\n*🤖 由 Claude AI 驱动 · Offer 捕手 v1.0 · 2026*")


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=9999,
        share=True,
        theme=gr.themes.Soft(primary_hue="purple", secondary_hue="blue"),
        css="""
        .gradio-container { max-width: 1000px !important; margin: 0 auto; }
        footer { display: none !important; }
        """
    )
