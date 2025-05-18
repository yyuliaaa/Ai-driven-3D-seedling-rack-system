import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from AMEKB.helper.sql_helper import SQLHelper


#from helper.sql_helper import SQLHelper  # 确保你有这个SQLHelper类的实现


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)  # 绑定鼠标离开事件

    def show(self, event):
        "Display text in tooltip window"
        self.x = event.x + self.widget.winfo_rootx() + 20
        self.y = event.y + self.widget.winfo_rooty() + 20
        if self.tipwindow or not self.text:
            return
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (self.x, self.y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"), wraplength=300)  # 设置多行显示
        label.pack(ipadx=4)

    def hide(self, event):
        if self.tipwindow:
            self.tipwindow.destroy()
            self.tipwindow = None


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

        # 左侧知识库系统结构
        sidebar_frame = ttk.Frame(main_container, width=400, style="Sidebar.TFrame")
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        # 知识库系统结构标题
        sidebar_title = ttk.Label(sidebar_frame, text="知识库系统结构", style="Title.TLabel")
        sidebar_title.pack(pady=15, padx=10, anchor="w")

        # 知识库树形结构
        self.knowledge_tree = ttk.Treeview(sidebar_frame, style="Sidebar.Treeview", show="tree")
        self.knowledge_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 设置列宽
        self.knowledge_tree.column("#0", width=230, minwidth=160, stretch=tk.YES)
        self.knowledge_tree.heading("#0", text="")

        # 填充知识库结构内容
        self.populate_knowledge_tree()

        # 右侧内容区域
        content_frame = ttk.Frame(main_container, style="Main.TFrame")
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 标题区域
        header_frame = ttk.Frame(content_frame, style="Header.TFrame")
        header_frame.pack(fill=tk.X, pady=(20, 10))

        title_label = ttk.Label(header_frame, text="设备公式库", style="Header.TLabel")
        title_label.pack(pady=15)

        # 查询区域框架
        search_frame = ttk.Frame(content_frame)
        search_frame.pack(pady=10, fill=tk.X, padx=20)

        # 装置分类下拉框
        ttk.Label(search_frame, text="装置分类:").pack(side=tk.LEFT, padx=10)
        self.combobox1 = ttk.Combobox(search_frame, width=25)
        self.combobox1.pack(side=tk.LEFT, padx=10)
        self.combobox1['values'] = ("全部", "水稻插秧机送秧装置", "水稻插秧机行走装置",
                                    "水稻插秧机秧箱装置", "水稻插秧机分插装置",
                                    "水稻插秧机移盘装置", "水稻插秧机传动装置")
        self.combobox1.current(0)  # 默认选择“全部”
        self.combobox1.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # 查询按钮
        self.btn_query = ttk.Button(
            search_frame,
            text="查询",
            command=self.query_data,
            width=12
        )
        self.btn_query.pack(side=tk.LEFT, padx=20)

        # 查询全部按钮
        self.btn_query_all = ttk.Button(
            search_frame,
            text="查询全部",
            command=self.fetch_all_data,
            width=12
        )
        self.btn_query_all.pack(side=tk.LEFT)

        # 操作按钮框架
        action_frame = ttk.Frame(content_frame)
        action_frame.pack(pady=20, fill=tk.X, padx=20)

        # 添加数据按钮
        self.btn_add = ttk.Button(
            action_frame,
            text="添加公式",
            command=self.add_formula,
            width=20
        )
        self.btn_add.pack(side=tk.LEFT, padx=10)

        # 删除选中数据按钮
        self.btn_delete = ttk.Button(
            action_frame,
            text="删除选中数据",
            command=self.delete_selected_data,
            width=20
        )
        self.btn_delete.pack(side=tk.LEFT, padx=10)

        # 树视图框架
        tree_frame = ttk.Frame(content_frame)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)

        # 树视图
        self.treeview = ttk.Treeview(
            tree_frame,
            columns=("ID", "装置分类", "装置名称", "公式名称", "推理公式", "公式单位解释"),
            show="headings",
            style="Main.Treeview"
        )
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("装置分类", text="装置分类")
        self.treeview.heading("装置名称", text="装置名称")
        self.treeview.heading("公式名称", text="公式名称")
        self.treeview.heading("推理公式", text="推理公式")
        self.treeview.heading("公式单位解释", text="公式单位解释")

        # 设置列宽
        self.treeview.column("ID", width=50)
        self.treeview.column("装置分类", width=150)
        self.treeview.column("装置名称", width=150)
        self.treeview.column("公式名称", width=150)
        self.treeview.column("推理公式", width=250)
        self.treeview.column("公式单位解释", width=300)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # 添加水平分割线
        ttk.Separator(content_frame, orient="horizontal").pack(fill=tk.X, pady=10, padx=20)

        # 初始加载所有数据
        self.fetch_all_data()

        # 为公式单位解释列添加 Tooltip
        self.treeview.bind("<Motion>", self.on_treeview_motion)

    def on_treeview_motion(self, event):
        region = self.treeview.identify("region", event.x, event.y)
        column = self.treeview.identify("column", event.x, event.y)
        item = self.treeview.identify("row", event.x, event.y)

        if region == "cell" and column == "#6" and item:  # 判断是否在公式单位解释列
            cell_value = self.treeview.item(item, "values")[5]  # 获取单元格内容
            if self.current_tooltip:
                self.current_tooltip.hide(event)  # 销毁当前的 Tooltip
            self.current_tooltip = ToolTip(self.treeview, cell_value)  # 创建新的 Tooltip
            self.current_tooltip.show(event)

    def show_tooltip(self, event, text):
        tooltip = ToolTip(self.treeview, text)
        tooltip.show(event)


    def populate_knowledge_tree(self):
        # 添加根节点
        root_node = self.knowledge_tree.insert("", "end", text="农业机械装备知识库系统", open=True)

        # 添加子节点
        nodes = {
            "水稻插秧机送秧装置": [
                "送秧机构参考型内容"
            ],
            "水稻插秧机行走装置": [
                "机动插秧机参考型内容",
                "驱动轮变量型内容",
                "锥形摩擦离合器变量型内容"
            ],
            "水稻插秧机秧箱装置": [
                "秧箱底板变量型内容",
                "秧箱公式型内容"
            ],
            "水稻插秧机分插装置": [
                "国产插秧机分插机构参考型内容",
                "曲柄连杆式分插机构变量型内容",
                "人力插秧机分插机构变量型内容",
                "梳式秧爪装置变量型内容",
                "梳式秧爪装置公式型内容",
                "行星齿轮式分插机构变量型内容"
            ],
            "水稻插秧机移盘装置": [
                "国产插秧机分插机构参考型内容",
                "曲柄连杆式分插机构变量型内容",
                "人力插秧机分插机构变量型内容",
                "梳式秧爪装置变量型内容",
                "梳式秧爪装置公式型内容",
                "行星齿轮式分插机构变量型内容"
            ],
            "水稻插秧机传动装置": [
                "棘爪齿条式公式型内容",
                "凸轮移盘式参考型内容",
                "转盘齿条式公式型内容"
            ],
            "水稻插秧机示例型内容": [
                "水稻插秧机示例型内容"
            ]
        }

        for category, items in nodes.items():
            category_node = self.knowledge_tree.insert(root_node, "end", text=category, open=True)
            for item in items:
                self.knowledge_tree.insert(category_node, "end", text=item)

        # 绑定点击事件
        self.knowledge_tree.bind("<Double-1>", self.on_tree_item_click)

    def on_combobox_select(self, event):
        # 处理组合框选择事件
        selected_value = self.combobox1.get()
        print(f"Selected value: {selected_value}")
        # 这里可以根据选择的值进行相应的操作

    def query_data(self):
        try:
            sql = "SELECT * FROM 设备公式库"
            if self.combobox1.get() != "全部":
                sql += f" WHERE 装置分类 = '{self.combobox1.get()}'"

            rows = self.sql_helper.fetch_data(sql)
            print(f"查询结果: {rows}")  # 打印查询结果

            # 清空树视图
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # 插入数据
            for row in rows:
                self.treeview.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("错误", f"查询时发生错误: {e}")

    def fetch_all_data(self):
        try:
            sql = "SELECT * FROM 设备公式库"
            rows = self.sql_helper.fetch_data(sql)
            print(f"查询结果: {rows}")  # 打印查询结果

            # 清空树视图
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # 插入数据
            for row in rows:
                self.treeview.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("错误", f"查询时发生错误: {e}")

    def add_formula(self):
        # 添加公式
        dialog = tk.Toplevel(self.root)
        dialog.title("添加公式")
        dialog.geometry("800x600")
        dialog.minsize(800, 600)

        # 设置样式
        style = ttk.Style(dialog)
        style.configure("TLabel", font=("Microsoft YaHei", 12))
        style.configure("TEntry", font=("Microsoft YaHei", 12))
        style.configure("TCombobox", font=("Microsoft YaHei", 12))
        style.configure("TButton", font=("Microsoft YaHei", 12), padding=10)

        # 创建表单框架
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 表单字段
        fields = [
            ("装置分类", "text"),
            ("装置名称", "text"),
            ("公式名称", "text"),
            ("推理公式", "text"),
            ("公式单位解释", "text")
        ]

        # 创建表单控件
        entries = {}
        for i, (label, field_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=15, sticky=tk.W)
            if field_type == "text":
                entry = ttk.Entry(form_frame, width=50)
                entry.grid(row=i, column=1, padx=10, pady=15, sticky=tk.W)
                entries[label] = entry

        # 提交按钮
        def submit():
            try:
                values = [entry.get() for entry in entries.values()]
                if not all(values):
                    messagebox.showwarning("警告", "请填写所有字段")
                    return

                sql = "INSERT INTO 设备公式库 (装置分类, 装置名称, 公式名称, 推理公式, 公式单位解释) VALUES (?, ?, ?, ?, ?)"
                self.sql_helper.execute_query(sql, values)
                messagebox.showinfo("成功", "公式已成功添加")
                dialog.destroy()
                self.fetch_all_data()  # 刷新数据

            except Exception as e:
                messagebox.showerror("错误", f"添加公式时发生错误: {e}")

        submit_button = ttk.Button(form_frame, text="提交", command=submit)
        submit_button.grid(row=len(fields), column=0, columnspan=2, pady=30)

    def delete_selected_data(self):
        # 删除选中数据
        selected_items = self.treeview.selection()
        if not selected_items:
            messagebox.showwarning("警告", "请先选择要删除的数据")
            return

        confirm = messagebox.askyesno("确认", "确定要删除选中的数据吗？")
        if not confirm:
            return

        try:
            for item in selected_items:
                item_id = self.treeview.item(item, "values")[0]
                # 确保 item_id 只包含数字
                item_id = ''.join(filter(str.isdigit, item_id))
                sql = "DELETE FROM 设备公式库 WHERE ID = ?"
                self.sql_helper.execute_query(sql, (item_id,))

            messagebox.showinfo("成功", "选中的数据已成功删除")
            self.fetch_all_data()  # 刷新数据

        except Exception as e:
            messagebox.showerror("错误", f"删除数据时发生错误: {e}")

    def on_tree_item_click(self, event):
        # 处理树形结构项点击事件
        selected_item = self.knowledge_tree.selection()[0]
        item_text = self.knowledge_tree.item(selected_item, "text")

        # 这里可以根据点击的项进行相应的操作，例如查询相关数据
        print(f"Selected item: {item_text}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormDeviceFormula(root)
    root.mainloop()