import tkinter as tk
from tkinter import ttk, messagebox

from AMEKB.forms.form_上下文知识推荐 import FormDeviceKnowledge
from AMEKB.helper.sql_helper import SQLHelper
#from form_上下文知识推荐 import FormDeviceKnowledge
from AMEKB.forms.form_实例推荐 import FormShiLiChaXun
#from ..helper.sql_helper import SQLHelper  # 确保你有这个SQLHelper类的实现

class FormDeviceFormula:
    def __init__(self, root):
        self.root = root
        self.root.title("农业机械装备知识库系统")
        self.root.geometry("1300x680")  # 调整窗口大小以容纳侧边栏
        self.root.minsize(1200, 680)  # 设置最小窗口大小
        self.sql_helper = SQLHelper()
        self.current_tooltip = None

        # 设置样式
        style = ttk.Style()
        style.theme_use("clam")  # 使用更现代的主题

        # 配置颜色
        style.configure("TFrame", background="#f5f5f5")
        style.configure("Header.TLabel", background="#2c3e50", foreground="white", font=("Microsoft YaHei", 16, "bold"))
        style.configure("Header.TFrame", background="#2c3e50")
        style.configure("Title.TLabel", background="#34495e", foreground="white", font=("Microsoft YaHei", 14, "bold"))
        style.configure("Sidebar.TFrame", background="#34495e")
        style.configure("Sidebar.Treeview", background="#2c3e50", fieldbackground="#2c3e50", foreground="white")
        style.configure("Main.Treeview", background="#ecf0f1", fieldbackground="#ecf0f1")
        style.configure("Main.TFrame", background="#ecf0f1")
        style.configure("TButton", font=("Microsoft YaHei", 12), padding=10)
        style.configure("TLabel", font=("Microsoft YaHei", 12))
        style.configure("TCombobox", font=("Microsoft YaHei", 12))
        style.map("TButton", background=[("active", "#3498db")])

        # 创建主框架
        main_container = ttk.Frame(root)
        main_container.pack(fill=tk.BOTH, expand=True)

        # 左侧知识库谱系结构
        sidebar_frame = ttk.Frame(main_container, width=300, style="Sidebar.TFrame")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # 知识库谱系结构标题
        sidebar_title = ttk.Label(sidebar_frame, text="知识库谱系结构", style="Title.TLabel")
        sidebar_title.pack(pady=15, padx=10, anchor="w")

        # 知识库树形结构
        self.knowledge_tree = ttk.Treeview(sidebar_frame, style="Sidebar.Treeview", show="tree")
        self.knowledge_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 设置列宽
        self.knowledge_tree.column("#0", width=200, minwidth=160, stretch=tk.YES)
        self.knowledge_tree.heading("#0", text="")

        # 填充知识库结构内容
        self.populate_knowledge_tree()

        # 右侧内容区域
        content_frame = ttk.Frame(main_container, style="Main.TFrame")
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 创建 Notebook 组件
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建每个页面
        self.create_notebook_pages()

    def create_notebook_pages(self):
        # 创建页面内容
        pages = [
            ("几何尺寸类参数知识", self.create_default_page),
            ("结构配置类参数知识", self.create_default_page),
            ("约束与校验类公式", self.create_default_page),
            ("结构安全类规则", self.create_default_page),
            ("功能配置类规则", self.create_default_page),
            ("参数联动与派生规则", self.create_default_page),
            ("模块调用类规则", self.create_default_page),
            ("异常处理与预警规则", self.create_default_page),
            ("设计公式", self.create_default_page),
            ("设计实例", self.load_design_instance_page),
            ("场景上下文", self.load_context_knowledge_page),
        ]

        for page_name, page_function in pages:
            frame = page_function()
            self.notebook.add(frame, text=page_name)

    def create_default_page(self):
        frame = ttk.Frame(self.notebook)
        label = ttk.Label(frame, text="这是一个默认页面", font=("Microsoft YaHei", 14))
        label.pack(pady=50)
        return frame

    def load_design_instance_page(self):
        frame = ttk.Frame(self.notebook)
        FormShiLiChaXun(frame)
        return frame

    def load_context_knowledge_page(self):
        frame = ttk.Frame(self.notebook)
        FormDeviceKnowledge(frame)
        return frame

    def populate_knowledge_tree(self):
        # 添加根节点
        root_node = self.knowledge_tree.insert("", "end", text="知识库", open=True)

        # 添加二级节点：结构参数
        structure_param_node = self.knowledge_tree.insert(root_node, "end", text="结构参数", open=True)
        # 添加三级节点
        self.knowledge_tree.insert(structure_param_node, "end", text="几何尺寸类参数知识")
        self.knowledge_tree.insert(structure_param_node, "end", text="结构配置类参数知识")
        self.knowledge_tree.insert(structure_param_node, "end", text="约束与校验类公式")
        self.knowledge_tree.insert(structure_param_node, "end", text="模型驱动参数绑定")

        # 添加二级节点：设计规则
        design_rule_node = self.knowledge_tree.insert(root_node, "end", text="设计规则", open=True)
        # 添加三级节点
        self.knowledge_tree.insert(design_rule_node, "end", text="结构安全类规则")
        self.knowledge_tree.insert(design_rule_node, "end", text="功能配置类规则")
        self.knowledge_tree.insert(design_rule_node, "end", text="参数联动与派生规则")
        self.knowledge_tree.insert(design_rule_node, "end", text="模块调用类规则")
        self.knowledge_tree.insert(design_rule_node, "end", text="异常处理与预警规则")

        # 添加二级节点：设计公式
        self.knowledge_tree.insert(root_node, "end", text="设计公式", open=True)

        # 添加二级节点：设计实例
        self.knowledge_tree.insert(root_node, "end", text="设计实例", open=True)

        # 添加二级节点：场景上下文
        self.knowledge_tree.insert(root_node, "end", text="场景上下文", open=True)

        # 绑定点击事件
        self.knowledge_tree.bind("<Double-1>", self.on_tree_item_click)

    def on_tree_item_click(self, event):
        # 处理树形结构项点击事件
        selected_item = self.knowledge_tree.selection()[0]
        item_text = self.knowledge_tree.item(selected_item, "text")
        print(f"Selected item: {item_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormDeviceFormula(root)
    root.mainloop()