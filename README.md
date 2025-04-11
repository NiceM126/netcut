# 在线剪贴板

> 🎯 本项目由 [Cursor](https://cursor.sh/) - 基于 AI 的新一代 IDE 开发。
> 项目原作者 [zxcv0221](https://github.com/zxcv0221/netcut)

一个简单、安全、高效的在线文本分享平台。支持密码保护、阅后即焚、自定义过期时间等功能。

![home](/img/home.png)

![paste](/img/paste.png)

![paste](/img/contact.png)


## 功能特点

- 🔒 密码保护：设置访问密码，保护敏感内容
- ⏰ 过期时间：支持1分钟、1小时、1天、7天、30天的过期设置
- 🔥 阅后即焚：查看一次后自动销毁内容
- ⏰ 实时显示剪贴板已查看次数，底部显示过期时间
- 📱 响应式设计：完美支持移动端访问
- ⚡ 快速响应：毫秒级的访问速度
- 🎨 美观界面：现代化的UI设计

## 技术栈

- 后端：Python + Flask
- 数据库：Redis
- 前端：HTML5 + CSS3 + JavaScript
- 部署：Docker + Nginx

## 项目架构
```
netcut/
├── app/                        # 应用主目录
│   ├── api/                   # API路由
│   │   ├── page_routes.py     # 页面路由
│   │   └── paste_routes.py    # 剪贴板相关路由
│   ├── services/              # 业务逻辑层
│   │   ├── paste_service.py   # 剪贴板服务
│   │   └── mail_service.py    # 邮件服务
│   ├── static/                # 静态资源
│   │   ├── images/           # 图片资源
│   │   │   ├── favicon.svg   # 网站图标
│   │   │   └── logo.svg      # 网站Logo
│   ├── templates/             # 模板文件
│   │   ├── pages/            # 静态页面模板
│   │   │   ├── about.html    # 关于页面
│   │   │   ├── help.html     # 帮助页面
│   │   │   ├── terms.html    # 服务条款
│   │   │   └── privacy.html  # 隐私政策
│   │   ├── base.html         # 基础模板
│   │   ├── edit.html         # 编辑页面
│   │   ├── error.html        # 错误页面
│   │   ├── index.html        # 首页
│   │   └── password.html     # 密码验证页面
│   ├── utils/                 # 工具函数
│   │   ├── encryption.py     # 加密工具
│   │   └── password.py       # 密码处理
│   ├── extensions.py         # Flask扩展
│   └── __init__.py           # 应用初始化
├── docker/                    # Docker相关文件
├── .env                      # 环境变量
├── config.py                 # 配置文件
├── docker-compose.yml        # Docker编排配置
├── Dockerfile                # Docker构建文件
├── nginx.conf                # Nginx参考配置
├── redis.conf                # redis参考配置
├── requirements.txt          # Python依赖
├── run.py                    # 应用入口
└── README.md                 # 项目说明
```

## 快速开始

### 环境要求

- Docker
- Docker Compose
- Redis 6.0+ (使用 Docker 部署时会自动安装)
- Python 3.9+ (本地开发)

> 💡 注意：如果使用 Docker 部署，Redis 会自动在容器中安装。如果是本地开发，需要自行安装 Redis 服务器。

### 部署步骤（推荐使用Docker）

1. 克隆项目
```bash
git clone https://github.com/your-username/netcut.git
cd netcut
```
2. 检查Nginx配置
```bash
/usr/local/nginx/sbin/nginx -t
# 修改nginx后
/usr/local/nginx/sbin/nginx -s reload
```
3. 启动服务
```bash
# 构建并启动所有服务
docker-compose up -d
```
## 查看服务状态
```bash
docker ps -a
```
## 查看日志
```bash
docker logs -f
```

## 本地开发

1. 安装 Redis
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install redis-server

# CentOS/RHEL
sudo yum install redis

# macOS
brew install redis

# Windows
# 从 https://github.com/microsoftarchive/redis/releases 下载安装包
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置 Redis
```bash
# 启动 Redis 服务
# Linux/macOS
sudo service redis start  # 或 sudo systemctl start redis

# Windows
redis-server

# 验证 Redis 是否正常运行
redis-cli ping  # 应该返回 PONG
```

4. 启动开发服务器
```bash
flask run
```

## 使用说明

1. 创建剪贴板
   - 输入或粘贴文本内容
   - 可选择设置密码保护、过期时间、阅后即焚
   - 点击"保存内容"按钮

2. 分享内容
   - 复制生成的链接
   - 如果设置了密码，需要填写密码才能通过链接访问内容

3. 安全提示
   - 重要内容建议使用密码保护
   - 敏感信息推荐使用阅后即焚
   - 定期清理不再需要的内容

## 配置说明

### 环境变量

- `SECRET_KEY`：Flask密钥
- `FLASK_ENV`：运行环境（development/production）
- `REDIS_HOST`：Redis服务器地址
- `REDIS_PORT`：Redis端口
- `ENCRYPTION_KEY`：内容加密密钥

