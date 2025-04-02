# 🔐 AES-TraceLab - AES 可视化分析平台

> 一个集成了 AES 加密全过程可视化、S-box 映射分析、动态交互的开源教学平台。
<img width="1792" alt="image" src="https://github.com/user-attachments/assets/e1ee36e7-2b1c-489c-af42-88e2bdf1924d" />
<img width="1792" alt="image" src="https://github.com/user-attachments/assets/65f0a9b6-3708-4f63-aee5-cd2fd952c4ff" />
<img width="1792" alt="image" src="https://github.com/user-attachments/assets/9e929c4c-eb36-4b13-9687-ce805135f2ff" />
<img width="1792" alt="image" src="https://github.com/user-attachments/assets/82ab9135-e829-46a3-8887-816fc79fbc08" />
<img width="1792" alt="image" src="https://github.com/user-attachments/assets/b7c85cd5-d6a1-4720-99d6-3691b7deecb6" />
##  ✨ 功能亮点

| 功能模块                 | 说明                                                                 |
|--------------------------|----------------------------------------------------------------------|
| 🔳 **S-box & 逆 S-box 可视化**   | 表格方式展示，支持搜索、高亮、导出、悬停动画等交互                       |
| 🔁 **逆查找映射**         | 输入 S-box 输出值，自动查找匹配的输入值                                 |
| 🔐 **AES 全轮加密可视化** | 显示每轮 SubBytes / ShiftRows / MixColumns / AddRoundKey 的状态变化 |
| 🎨 **粒子动画背景**       | 随鼠标交互的酷炫粒子效果                                               |
| 👁 **多字节分析**         | 支持多输入字节批量展示 S-box 映射、XOR、汉明距离、逆查验证等分析        |
| 📊 **实时访客展示**       | 显示访问者 IP、设备信息、地理位置、访问趋势折线图等                       |
| 📤 **状态导出功能**       | AES 每轮状态支持导出为 CSV / JSON / PNG（可拓展）                        |
| 📱 **移动端适配**         | 样式响应式支持手机、平板查看                                            |

---

## 🛠 技术栈

- 🌐 前端：HTML + Bootstrap 5 + 原生 JavaScript
- 🔥 后端：Python 3 + Flask + gunicorn
- 🎨 粒子动画：tsParticles
- 📦 部署：支持 Docker / Render / Railway / 本地运行

---

## 📦 快速启动（本地部署）

### 1. 克隆项目

```bash
git clone git@github.com:lala-amber/AES-TraceLab.git
cd AES-TraceLab
```

### 2. 安装依赖
```
pip install -r requirements.txt
```
### 3. 启动 Flask
```
python app.py
```

访问：http://localhost:8080

## 🐳 Docker 部署
```
~ ⌚ 9:39:56
$ docker pull ainwpu/aes-sbox-app
Using default tag: latest
latest: Pulling from ainwpu/aes-sbox-app
Digest: sha256:cc955e19a136f107271e3af96db0d1ff5f37380c6ee47a8ce49af984a1ec3137
Status: Image is up to date for ainwpu/aes-sbox-app:latest
docker.io/ainwpu/aes-sbox-app:latest

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview ainwpu/aes-sbox-app
(base) 
~ ⌚ 9:40:11
$ docker images                           
REPOSITORY            TAG       IMAGE ID       CREATED         SIZE
ainwpu/aes-sbox-app   latest    077fb8ea691e   16 hours ago    150MB
aes-sbox-app          latest    077fb8ea691e   16 hours ago    150MB
hxrhkleeverilator     latest    15e1dad557d4   5 weeks ago     12.5GB
klee/klee             latest    cc49b2cfae90   13 months ago   10.5GB
(base) 
~ ⌚ 9:40:26
$ docker run -it -p 8080:8080 077fb8ea691e    
```
<img width="1780" alt="image" src="https://github.com/user-attachments/assets/fab73d9e-0113-46ee-aad5-e62af23434bb" />

## 📁 项目结构
```
├── app.py                # Flask 主程序
├── sbox_core.py          # AES 逻辑模块（S-box、加密等）
├── templates/
│   └── index.html        # 网页主模板
├── static/
│   └── style.css         # 页面样式文件
├── requirements.txt      # Python 依赖列表
├── Dockerfile            # Docker 容器部署配置
└── README.md             # 项目说明文档
```
## ✨ 展望拓展方向
✅ 支持 AES 解密过程展示

✅ 添加攻击模拟（如差分分析 / 故障注入）

✅ 整合论文图谱分析与教学评测系统

## 🧑‍💻 作者
Created by @lala-amber@huangxuan
欢迎 Issue、PR、Star 🌟！

## 📄 License
MIT License - 自由使用、传播、教学用途优先。
