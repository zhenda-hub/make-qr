from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
import json
import uuid
import qrcode
from io import BytesIO
import base64
from datetime import datetime


app = FastAPI()


# 配置静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


# 初始化模板
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/qr-form")
async def qr_form(request: Request):
    return templates.TemplateResponse("qr_form.html", {"request": request})


# 确保目录存在
os.makedirs("uploads", exist_ok=True)
os.makedirs("generated_pages", exist_ok=True)
os.makedirs("generated_qrcodes", exist_ok=True)

class PageRequest(BaseModel):
    title: str
    content: str
    qrColor: str
    qrSize: int

class QRRequest(BaseModel):
    url: str
    color: str
    size: int

@app.post("/generate-page")
async def generate_page(request: PageRequest):
    """生成二维码页面"""
    page_id = str(uuid.uuid4())
    page_data = {
        "title": request.title,
        "content": request.content,
        "created_at": datetime.now().isoformat()
    }
    
    # 保存页面数据
    page_file = f"generated_pages/{page_id}.json"
    with open(page_file, "w") as f:
        json.dump(page_data, f)
    
    return {"pageUrl": f"/page/{page_id}"}

@app.get("/page/{page_id}")
async def show_page(page_id: str, request: Request):
    """展示生成的页面"""
    page_file = f"generated_pages/{page_id}.json"
    if not os.path.exists(page_file):
        return {"error": "Page not found"}, 404
    
    with open(page_file) as f:
        page_data = json.load(f)
    
    return templates.TemplateResponse("qr_page.html", {
        "request": request,
        "title": page_data["title"],
        "content": page_data["content"]
    })

@app.post("/generate-qrcode")
async def generate_qrcode(request: QRRequest):
    """生成二维码图片"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(request.url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=request.color, back_color="white")
    buffer = BytesIO()
    img.save(buffer, "PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return {"qrImage": f"data:image/png;base64,{img_str}"}

# 确保上传目录存在
os.makedirs("uploads", exist_ok=True)
