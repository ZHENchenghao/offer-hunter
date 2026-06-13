"""Offer 捕手 — AI 求职智能匹配体
FastAPI 后端 + Claude API 集成
"""

import os
from fastapi import FastAPI, Form, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from services.jobs_data import JOBS
from services.claude_service import (
    match_resume_to_jobs,
    optimize_resume_for_job,
    extract_skills,
)

app = FastAPI(title="Offer捕手", version="1.0.0")

# 静态文件 & 模板
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "jobs": JOBS})


@app.get("/api/jobs")
async def get_jobs():
    return JSONResponse({"jobs": JOBS, "total": len(JOBS)})


@app.get("/api/jobs/{job_id}")
async def get_job(job_id: int):
    job = next((j for j in JOBS if j["id"] == job_id), None)
    if job is None:
        return JSONResponse({"error": "岗位不存在"}, status_code=404)
    return JSONResponse(job)


@app.post("/api/match")
async def match_resume(resume: str = Form(...)):
    """匹配简历与岗位"""
    if not resume.strip() or len(resume.strip()) < 20:
        return JSONResponse({"error": "简历内容太少，请至少输入20字"}, status_code=400)

    result = match_resume_to_jobs(resume, JOBS)
    return JSONResponse(result)


@app.post("/api/optimize")
async def optimize_resume(resume: str = Form(...), job_id: int = Form(...)):
    """优化简历"""
    if not resume.strip() or len(resume.strip()) < 20:
        return JSONResponse({"error": "简历内容太少"}, status_code=400)

    job = next((j for j in JOBS if j["id"] == job_id), None)
    if job is None:
        return JSONResponse({"error": "岗位不存在"}, status_code=404)

    result = optimize_resume_for_job(resume, job)
    return JSONResponse(result)


@app.post("/api/extract")
async def extract(resume: str = Form(...)):
    """提取技能"""
    if not resume.strip():
        return JSONResponse({"error": "请提供简历内容"}, status_code=400)

    result = extract_skills(resume)
    return JSONResponse(result)


@app.post("/api/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    """上传简历文件并提取文本"""
    try:
        content = await file.read()
        text = content.decode("utf-8")
        # 简单清洗
        text = text.strip()
        if len(text) < 20:
            return JSONResponse({"error": "文件内容太少"}, status_code=400)
        return JSONResponse({"filename": file.filename, "text": text, "length": len(text)})
    except UnicodeDecodeError:
        return JSONResponse({"error": "文件编码不支持，请使用UTF-8编码的TXT文件"}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": f"文件读取失败: {str(e)}"}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
