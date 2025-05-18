import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from helper.sql_helper import SQLHelper


class FormDeviceInfo:
    def __init__(self, root):
        self.root = root
        self.root.title("设备信息库")
        self.root.geometry("1200x700")  # 设置窗口大小
        self.root.minsize(1200, 700)  # 设置最小窗口大小
        self.sql_helper = SQLHelper()

        # 设置样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TCombobox", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text="设备信息库",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)

        # 查询区域框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(pady=10, fill=tk.X)

        # 机械用途分类下拉框
        ttk.Label(search_frame, text="机械用途分类:").pack(side=tk.LEFT, padx=10)
        self.combobox1 = ttk.Combobox(search_frame, width=20)
        self.combobox1.pack(side=tk.LEFT, padx=10)
        self.combobox1['values'] = ("全部", "机械用途分类1", "机械用途分类2")  # 假设的分类名称
        self.combobox1.current(0)  # 默认选择“全部”
        self.combobox1.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # 查询按钮
        self.btn_query = ttk.Button(
            search_frame,
            text="查询",
            command=self.query_data,
            width=15
        )
        self.btn_query.pack(side=tk.LEFT, padx=20)

        # 查询全部按钮
        self.btn_query_all = ttk.Button(
            search_frame,
            text="查询全部",
            command=self.fetch_all_data,
            width=15
        )
        self.btn_query_all.pack(side=tk.LEFT)

        # 操作按钮框架
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(pady=20, fill=tk.X)

        # 添加数据按钮
        self.btn_add = ttk.Button(
            action_frame,
            text="添加设备信息",
            command=self.add_device_info,
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
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # 树视图
        self.treeview = ttk.Treeview(
            tree_frame,
            columns=(
                "ID", "机械用途分类", "机械类型", "机械名称", "发动机额定功率",
                "长", "宽", "高", "插秧行数", "质量", "图片", "知识描述"
            ),
            show="headings"
        )
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("机械用途分类", text="机械用途分类")
        self.treeview.heading("机械类型", text="机械类型")
        self.treeview.heading("机械名称", text="机械名称")
        self.treeview.heading("发动机额定功率", text="发动机额定功率")
        self.treeview.heading("长", text="长")
        self.treeview.heading("宽", text="宽")
        self.treeview.heading("高", text="高")
        self.treeview.heading("插秧行数", text="插秧行数")
        self.treeview.heading("质量", text="质量")
        self.treeview.heading("图片", text="图片")
        self.treeview.heading("知识描述", text="知识描述")

        # 设置列宽
        self.treeview.column("ID", width=50)
        self.treeview.column("机械用途分类", width=120)
        self.treeview.column("机械类型", width=120)
        self.treeview.column("机械名称", width=120)
        self.treeview.column("发动机额定功率", width=120)
        self.treeview.column("长", width=80)
        self.treeview.column("宽", width=80)
        self.treeview.column("高", width=80)
        self.treeview.column("插秧行数", width=100)
        self.treeview.column("质量", width=80)
        self.treeview.column("图片", width=100)
        self.treeview.column("知识描述", width=200)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # 初始加载所有数据
        self.fetch_all_data()

    def on_combobox_select(self, event):
        # 处理组合框选择事件
        pass

    def query_data(self):
        try:
            sql = "SELECT * FROM 设备信息库"
            if self.combobox1.get() != "全部":
                sql += f" WHERE 机械用途分类 = '{self.combobox1.get()}'"

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
            sql = "SELECT * FROM 设备信息库"
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

    def add_device_info(self):
        # 添加设备信息
        dialog = tk.Toplevel(self.root)
        dialog.title("添加设备信息")
        dialog.geometry("800x600")
        dialog.minsize(800, 600)

        # 设置样式
        style = ttk.Style(dialog)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TEntry", font=("Arial", 12))
        style.configure("TCombobox", font=("Arial", 12))
        style.configure("TButton", font=("Arial", 12), padding=10)

        # 创建表单框架
        form_frame = ttk.Frame(dialog, padding="20")
        form_frame.pack(fill=tk.BOTH, expand=True)

        # 表单字段
        fields = [
            ("机械用途分类", "text"),
            ("机械类型", "text"),
            ("机械名称", "text"),
            ("发动机额定功率", "text"),
            ("长", "text"),
            ("宽", "text"),
            ("高", "text"),
            ("插秧行数", "text"),
            ("质量", "text"),
            ("图片", "text"),
            ("知识描述", "text")
        ]

        # 创建表单控件
        entries = {}
        for i, (label, field_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            if field_type == "text":
                entry = ttk.Entry(form_frame, width=50)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky=tk.W)
                entries[label] = entry

        # 提交按钮
        def submit():
            try:
                values = [entry.get() for entry in entries.values()]
                if not all(values):
                    messagebox.showwarning("警告", "请填写所有字段")
                    return

                sql = "INSERT INTO 设备信息库 (机械用途分类, 机械类型, 机械名称, 发动机额定功率, 长, 宽, 高, 插秧行数, 质量, 图片, 知识描述) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                self.sql_helper.execute_query(sql, values)
                messagebox.showinfo("成功", "设备信息已成功添加")
                dialog.destroy()
                self.fetch_all_data()  # 刷新数据

            except Exception as e:
                messagebox.showerror("错误", f"添加设备信息时发生错误: {e}")

        submit_button = ttk.Button(form_frame, text="提交", command=submit)
        submit_button.grid(row=len(fields), column=0, columnspan=2, pady=20)

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
                sql = "DELETE FROM 设备信息库 WHERE ID = ?"
                self.sql_helper.execute_query(sql, (item_id,))

            messagebox.showinfo("成功", "选中的数据已成功删除")
            self.fetch_all_data()  # 刷新数据

        except Exception as e:
            messagebox.showerror("错误", f"删除数据时发生错误: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormDeviceInfo(root)
    root.mainloop()