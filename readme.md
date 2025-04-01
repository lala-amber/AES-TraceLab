# 🧠 AES S-box 分析与可视化工具（Web 版）

这是一个基于 Flask + HTML + JavaScript 实现的交互式 AES S-box 分析工具，支持：

✅ S-box / 逆 S-box 表格可视化  
✅ 多字节映射分析  
✅ 高亮搜索、十进制提示  
✅ AES 一轮过程可视化  
✅ S-box 逆查找模式  
✅ 动画 + 深色 UI + 导出 CSV + 十进制切换  
✅ 全部功能可容器化部署（Docker）

---

## ✨ 功能特性

| 模块 | 功能描述 |
|------|----------|
| 🔢 AES S-box & 逆 S-box | 可视化 16×16 表格，支持切换十六进制 / 十进制 |
| 🔎 高亮搜索 | 支持输入 `S-box[x]` 中的 x 进行高亮显示 |
| 🔄 十六/十进制切换 | 所有值支持一键切换显示格式 |
| 📊 字节分析 | 支持输入多个字节，分析 S-box 映射、逆映射、XOR、汉明距离等 |
| 🧩 逆查找功能 | 给定一个 S-box 输出值，反查所有对应的输入值（可用于故障分析、逆向验证） |
| 🧪 AES 一轮过程可视化 | 输入完整的 16 字节明文块，展示 SubBytes、ShiftRows、AddRoundKey 的每一步状态 |
| 📤 导出功能 | 一键导出 S-box / 逆 S-box 为 `.csv` 文件 |
| 🎨 前端美观 | 暗黑主题、动画过渡、响应式设计，适合教学 / 演示 / 安全分析 |

---


```markdown
## 📁 项目结构
aes_sbox_web/
├── app.py              # Flask 后端主逻辑
├── sbox_core.py        # 所有 AES S-box 与 AES 一轮过程核心代码
├── templates/
│   └── index.html      # 前端主界面（Bootstrap + 原生 JS）
├── static/
│   └── style.css       # 自定义炫酷暗色主题样式
├── requirements.txt    # pip 依赖（仅 flask）
├── Dockerfile          # 一键容器化部署
```

# 一键容器化部署


---

## 🚀 快速使用

### ✅ 1. 克隆仓库 & 安装依赖

```
git clone https://github.com/yourname/aes-sbox-web.git
cd aes_sbox_web
pip install -r requirements.txt
python app.py
```

###   ✅ 2. 一键容器化部署

你也可以通过 Docker 一键构建和运行该项目：

```
# 构建镜像
docker build -t aes-sbox-app .

# 运行容器并映射端口
docker run -it -p 8080:8080 aes-sbox-app
```
访问地址：http://localhost:8080

# 🧠 教学用途场景

🔐 密码学课程演示：可视化 AES 子字节转换全过程

🧪 AES 故障注入分析辅助工具

🛠 S-box 逆向、安全分析实验平台

📚 写论文、实验报告时的截图生成工具

# ✍️ 作者与鸣谢

作者：黄璇





