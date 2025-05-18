import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
#from helper.sql_helper import SQLHelper
from PIL import Image, ImageTk
import os

from AMEKB.helper.sql_helper import SQLHelper


class FormDeviceKnowledge:
    def __init__(self, root):
        self.root = root
        self.root.title("设备知识库")
        self.root.geometry("1200x800")  # 设置窗口大小
        self.root.minsize(1200, 800)    # 设置最小窗口大小
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
            text="设备知识库",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)

        # 查询区域框架
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(pady=10, fill=tk.X)

        # 装置分类下拉框
        ttk.Label(search_frame, text="装置分类:").pack(side=tk.LEFT, padx=10)
        self.combobox1 = ttk.Combobox(search_frame, width=20)
        self.combobox1.pack(side=tk.LEFT, padx=10)
        self.combobox1['values'] = ("全部", "装置分类1", "分类2")  # 假设的分类名称
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
            text="添加知识",
            command=self.add_knowledge,
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

        # 主内容框架
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # 树视图框架
        tree_frame = ttk.Frame(content_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # 树视图
        self.treeview = ttk.Treeview(
            tree_frame,
            columns=("ID", "装置分类", "装置名称", "知识内容1", "知识内容2", "知识内容3", "知识内容4"),
            show="headings"
        )
        self.treeview.heading("ID", text="ID")
        self.treeview.heading("装置分类", text="装置分类")
        self.treeview.heading("装置名称", text="装置名称")
        self.treeview.heading("知识内容1", text="知识内容1")
        self.treeview.heading("知识内容2", text="知识内容2")
        self.treeview.heading("知识内容3", text="知识内容3")
        self.treeview.heading("知识内容4", text="知识内容4")

        # 设置列宽
        self.treeview.column("ID", width=50)
        self.treeview.column("装置分类", width=120)
        self.treeview.column("装置名称", width=120)
        self.treeview.column("知识内容1", width=150)
        self.treeview.column("知识内容2", width=150)
        self.treeview.column("知识内容3", width=150)
        self.treeview.column("知识内容4", width=150)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # 图片显示框架
        image_frame = ttk.Frame(content_frame, padding="50", relief=tk.RAISED, borderwidth=4)
        image_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10)

        # 图片显示区域
        self.image_label = ttk.Label(image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)

        # 图片路径标签
        self.image_path_label = ttk.Label(image_frame, text="图片预览")
        self.image_path_label.pack(pady=10)

        # 绑定树视图选择事件
        self.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        # 初始加载所有数据
        self.fetch_all_data()

    def on_combobox_select(self, event):
        # 处理组合框选择事件
        pass

    def query_data(self):
        try:
            sql = "SELECT * FROM 设备知识库"
            if self.combobox1.get() != "全部":
                sql += f" WHERE 装置分类 = '{self.combobox1.get()}'"

            rows = self.sql_helper.fetch_data(sql)
            print(f"查询结果: {rows}")  # 打印查询结果

            # 清空树视图
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # 插入数据
            for row in rows:
                # 假设图片路径是最后一列
                self.treeview.insert("", "end", values=row[:-1])  # 不显示图片路径

        except Exception as e:
            messagebox.showerror("错误", f"查询时发生错误: {e}")

    def fetch_all_data(self):
        try:
            sql = "SELECT * FROM 设备知识库"
            rows = self.sql_helper.fetch_data(sql)
            print(f"查询结果: {rows}")  # 打印查询结果

            # 清空树视图
            for item in self.treeview.get_children():
                self.treeview.delete(item)

            # 插入数据
            for row in rows:
                # 假设图片路径是最后一列
                self.treeview.insert("", "end", values=row[:-1])  # 不显示图片路径

        except Exception as e:
            messagebox.showerror("错误", f"查询时发生错误: {e}")

    def add_knowledge(self):
        # 添加知识
        dialog = tk.Toplevel(self.root)
        dialog.title("添加知识")
        dialog.geometry("1000x800")
        dialog.minsize(1000, 800)

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
            ("装置分类", "text"),
            ("装置名称", "text"),
            ("知识内容1", "text"),
            ("知识内容2", "text"),
            ("知识内容3", "text"),
            ("知识内容4", "text"),
            ("图片路径", "text")
        ]

        # 创建表单控件
        entries = {}
        for i, (label, field_type) in enumerate(fields):
            ttk.Label(form_frame, text=label).grid(row=i, column=0, padx=10, pady=10, sticky=tk.W)
            if field_type == "text":
                entry = ttk.Entry(form_frame, width=80)
                entry.grid(row=i, column=1, padx=10, pady=10, sticky=tk.W)
                entries[label] = entry

        # 提交按钮
        def submit():
            try:
                values = [entry.get() for entry in entries.values()]
                if not all(values):
                    messagebox.showwarning("警告", "请填写所有字段")
                    return

                sql = "INSERT INTO 设备知识库 (装置分类, 装置名称, 知识内容1, 知识内容2, 知识内容3, 知识内容4, 图片路径) VALUES (?, ?, ?, ?, ?, ?, ?)"
                self.sql_helper.execute_query(sql, values)
                messagebox.showinfo("成功", "知识已成功添加")
                dialog.destroy()
                self.fetch_all_data()  # 刷新数据

            except Exception as e:
                messagebox.showerror("错误", f"添加知识时发生错误: {e}")

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
            # 获取选中行的ID
            item = selected_items[0]
            values = self.treeview.item(item, "values")
            item_id = values[0]

            sql = "DELETE FROM 设备知识库 WHERE ID = ?"
            self.sql_helper.execute_query(sql, (item_id,))

            messagebox.showinfo("成功", "选中的数据已成功删除")
            self.fetch_all_data()  # 刷新数据

        except Exception as e:
            messagebox.showerror("错误", f"删除数据时发生错误: {e}")

    def on_treeview_select(self, event):
        # 处理树视图选择事件，显示图片
        selected_items = self.treeview.selection()
        if not selected_items:
            return

        # 获取选中的行的数据
        item = selected_items[0]
        values = self.treeview.item(item, "values")
        item_id = values[0]

        # 查询完整的数据行，包括图片路径
        try:
            sql = "SELECT * FROM 设备知识库 WHERE ID = ?"
            row = self.sql_helper.fetch_data(sql, (item_id,))
            if row:
                image_path = row[0][-1]  # 获取图片路径

                # 更新图片路径标签
                self.image_path_label.config(text=f"图片路径: {image_path}")

                # 显示图片
                self.show_image(image_path)

        except Exception as e:
            messagebox.showerror("错误", f"显示图片时发生错误: {e}")

    def show_image(self, image_path):
        try:
            # 打开图片
            img = Image.open(image_path)
            # 调整图片大小以适应显示区域
            img = img.resize((400, 300), Image.LANCZOS)
            # 转换为PhotoImage
            photo = ImageTk.PhotoImage(img)
            # 更新标签
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 保持引用，防止被垃圾回收

        except Exception as e:
            messagebox.showerror("错误", f"显示图片时发生错误: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FormDeviceKnowledge(root)
    root.mainloop()