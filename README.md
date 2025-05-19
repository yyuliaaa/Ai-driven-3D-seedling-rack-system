# Ai-driven-3D-seedling-rack-system
系统全称：Ai-driven parametric modeling system for three-dimensional rice seedling raising

这是基于Python的智能知识库系统，构建了多源知识库（结构规则、设计公式、环境参数）并设计规则与实例融合的AI推理引擎，实现参数自动推荐

系统创新研发模块化AI接口，无缝对接CATIA完成模型实时驱动。

作为核心开发者，本人全程主导系统架构设计、算法编码与功能实现，攻克知识逻辑表达、动态推理链生成及三维接口自动化等关键技术

研究成果为水稻立体育秧参数化建模系统exe文件，且正形成论文

AI驱动的水稻立体育苗参数化建模系统实例视频：

https://github.com/user-attachments/assets/bc2a2724-c107-4c1c-b629-c91551721c5a


## 项目结构
以下是项目的目录结构：

```plaintext
CATIA_AI_fin
│
├── AMEKB
│   ├── img
│   │   └── 育秧架.jpg
│   ├── forms
│   │   ├── init.py
│   │   ├── form_上下文知识推荐.py
│   │   ├── form_用户界面.py
│   │   ├── form_规则推荐.py
│   │   ├── form_实例推荐.py
│   │   └── catia_ai_ok.py
│   ├── helper
│   │   ├── init.py
│   │   └── sql_helper.py
├── catia_integration
│   ├── init.py
│   └── catia_operator_0_很久之前.py
└── main0.py
```


### 目录说明

- **AMEKB**：包含项目的主要功能模块（AMEKB是系统的简称）。
  - **config**：包含setting.ini用于配置的AI接口文件
  - **img**：存放项目相关的图片资源。
  - **forms**：包含各种表单相关的 Python 脚本。
  - **helper**：提供辅助功能的脚本，如数据库操作等。
- **catia_integration**：包含与 CATIA 集成相关的脚本。
- **main0.py**：项目的主入口脚本。

## 快速开始
1. 克隆项目到本地：
   ```bash
   git clone https://github.com/your-username/CATIA_AI_fin.git
   ```
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行项目：
   ```bash
   python main0.py
   ```


