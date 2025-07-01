# make-qr

## 项目概述
基于FastAPI的多媒体二维码生成系统，支持批量上传图片/视频并生成可扫描查看的二维码。

## 技术栈
- 后端: FastAPI + Uvicorn
- 前端: 
  - Jinja2模板
  - Tailwind CSS (UI框架)
  - Alpine.js (交互逻辑)
- 二维码: qrcode库
- 文件处理: python-multipart

## 部署运行

### 本地运行
```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn main:app --reload
```

### Docker运行
```bash
# 构建镜像
docker-compose build

# 启动服务
docker-compose up

# 访问地址
http://localhost:8000
```

