import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sys
# sys.path.append('D:/BachelorD/AR/CATIA_AI_fin/AMEKB/helper')
# from sql_helper import SQLHelper
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建到 helper 目录的相对路径
helper_path = os.path.join(current_dir, '..', 'helper')

# 将 helper 目录路径添加到 sys.path
sys.path.append(helper_path)

# 导入 SQLHelper
from sql_helper import SQLHelper
#from ..helper.sql_helper import SQLHelper
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
class FormShiLiChaXun:
    def __init__(self, parent):
        self.parent = parent
        self.sql_helper = SQLHelper()
        self.create_widgets()
        self.load_data()  # 确保在创建界面后加载数据

    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 创建表格框架
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 创建表格标题
        tree_label = ttk.Label(tree_frame, text="示例数据片段展示表", font=("Arial", 12, "bold"))
        tree_label.pack(fill=tk.X, pady=(0, 10))

        # 创建 Treeview
        self.treeview = ttk.Treeview(tree_frame, columns=(
        "id", "layers", "rows", "air_channel", "ventilation", "rail", "total_height", "remarks"), show="headings")
        self.treeview.heading("id", text="实例编号")
        self.treeview.heading("layers", text="层数")
        self.treeview.heading("rows", text="行数")
        self.treeview.heading("air_channel", text="风道类型")
        self.treeview.heading("ventilation", text="通风要求")
        self.treeview.heading("rail", text="滑轨")
        self.treeview.heading("total_height", text="总高(mm)")
        self.treeview.heading("remarks", text="备注说明")

        # 设置列宽
        self.treeview.column("id", width=90)
        self.treeview.column("layers", width=50)
        self.treeview.column("rows", width=50)
        self.treeview.column("air_channel", width=140)
        self.treeview.column("ventilation", width=80)
        self.treeview.column("rail", width=120)
        self.treeview.column("total_height", width=80)
        self.treeview.column("remarks", width=250)

        self.treeview.pack(fill=tk.BOTH, expand=True)

        # 创建操作按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # 创建添加数据按钮
        self.button_add = ttk.Button(button_frame, text="添加数据", command=self.add_data)
        self.button_add.pack(fill=tk.X, pady=5)

        # 创建删除选中数据按钮
        self.button_delete = ttk.Button(button_frame, text="删除选中数据", command=self.delete_selected_data)
        self.button_delete.pack(fill=tk.X, pady=5)

        # 创建推理条件和推荐结果框架
        controls_and_recommendation_frame = ttk.Frame(main_frame)
        controls_and_recommendation_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # 创建推理条件框架
        controls_frame = ttk.Frame(controls_and_recommendation_frame)
        controls_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # 创建推理条件标题
        controls_label = ttk.Label(controls_frame, text="推理条件", font=("Arial", 12, "bold"))
        controls_label.pack(fill=tk.X, pady=(0, 10))

        # 创建推理条件输入框
        ttk.Label(controls_frame, text="层数").pack(fill=tk.X)
        self.txt_layers = ttk.Entry(controls_frame, width=20)
        self.txt_layers.pack(fill=tk.X)

        ttk.Label(controls_frame, text="行数").pack(fill=tk.X)
        self.txt_rows = ttk.Entry(controls_frame, width=20)
        self.txt_rows.pack(fill=tk.X)

        ttk.Label(controls_frame, text="风道类型").pack(fill=tk.X)
        self.cmb_air_channel = ttk.Combobox(controls_frame, values=["单侧", "无", "双风道"], width=17)
        self.cmb_air_channel.pack(fill=tk.X)

        ttk.Label(controls_frame, text="通风要求").pack(fill=tk.X)
        self.cmb_ventilation = ttk.Combobox(controls_frame, values=["强", "中", "弱"], width=17)
        self.cmb_ventilation.pack(fill=tk.X)

        ttk.Label(controls_frame, text="滑轨").pack(fill=tk.X)
        self.cmb_rail = ttk.Combobox(controls_frame, values=["有", "无"], width=17)
        self.cmb_rail.pack(fill=tk.X)

        # 创建按钮
        self.button_recommend = ttk.Button(controls_frame, text="实例知识推荐", command=self.button_recommend_click)
        self.button_recommend.pack(fill=tk.X, pady=10)

        # 创建推荐结果框架
        recommendation_frame = ttk.Frame(controls_and_recommendation_frame)
        recommendation_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # 创建推荐标题
        recommendation_label = ttk.Label(recommendation_frame, text="基于相似度的实例知识推荐",
                                         font=("Arial", 12, "bold"))
        recommendation_label.pack(fill=tk.X, pady=(0, 10))

        # 创建推荐结果显示框
        self.recommendation_text = tk.Text(recommendation_frame, height=5, width=50)
        self.recommendation_text.pack(fill=tk.BOTH, expand=True)

    def add_data(self):
        # 弹出对话框，让用户输入数据
        instance_id = simpledialog.askstring("输入", "实例编号:", parent=self.parent)
        if not instance_id:
            return

        layers = simpledialog.askstring("输入", "层数:", parent=self.parent)
        if not layers:
            return

        rows = simpledialog.askstring("输入", "行数:", parent=self.parent)
        if not rows:
            return

        air_channel = simpledialog.askstring("输入", "风道类型 (单侧风道/无风道/双风道):", parent=self.parent)
        if not air_channel:
            return

        ventilation = simpledialog.askstring("输入", "通风要求 (强/中/弱):", parent=self.parent)
        if not ventilation:
            return

        rail = simpledialog.askstring("输入", "滑轨 (有/无):", parent=self.parent)
        if not rail:
            return

        total_height = simpledialog.askstring("输入", "总高 (mm):", parent=self.parent)
        if not total_height:
            return

        remarks = simpledialog.askstring("输入", "备注说明:", parent=self.parent)
        if not remarks:
            remarks = ""

        # 插入到数据库
        insert_sql = """
        INSERT INTO 示例数据片段表 (实例编号, 层数, 行数, 风道类型, 通风要求, 滑轨, 总高, 备注说明)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            self.sql_helper.execute_query(insert_sql, (
            instance_id, layers, rows, air_channel, ventilation, rail, total_height, remarks))
            # 刷新表格
            self.load_data()
        except Exception as e:
            messagebox.showerror("错误", f"添加数据失败: {e}")

    def delete_selected_data(self):
        # 获取选中的行
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择要删除的行！")
            return

        # 获取实例编号
        instance_id = self.treeview.item(selected_item, "values")[0]

        # 从数据库中删除
        delete_sql = "DELETE FROM 示例数据片段表 WHERE 实例编号 = ?"
        self.sql_helper.execute_query(delete_sql, (instance_id,))

        # 从表格中删除
        self.treeview.delete(selected_item)

    def load_data(self):
        # 清空表格
        for i in self.treeview.get_children():
            self.treeview.delete(i)

        # 查询数据并插入到表格
        fsql = """
        SELECT 实例编号, 层数, 行数, 风道类型, 通风要求, 滑轨, 总高, 备注说明
        FROM 示例数据片段表
        """
        rows = self.sql_helper.fetch_data(fsql)
        for row in rows:
            self.treeview.insert("", "end", values=row)

    def button_recommend_click(self):
        # 获取推理条件输入值
        layers = self.txt_layers.get().strip()
        rows = self.txt_rows.get().strip()
        air_channel = self.cmb_air_channel.get().strip()
        ventilation = self.cmb_ventilation.get().strip()
        rail = self.cmb_rail.get().strip()

        # 校验层数和行数
        error_message = ""
        if not layers.isdigit() or not rows.isdigit():
            error_message = "层数和行数必须是正整数。"
        else:
            layers = int(layers)
            rows = int(rows)
            if layers > 30 or layers % 2 != 0:
                error_message = "层数不能超过30，且必须是偶数。"
            if rows <= 0:
                error_message = "行数必须是正整数。"

        if error_message:
            # 输出错误信息到推荐结果框
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, error_message)
            return  # 退出函数，不再继续执行后续逻辑

        # 如果没有错误，继续执行推荐逻辑
        conditions = {
            "层数": str(layers),
            "行数": str(rows),
            "风道类型": air_channel,
            "通风要求": ventilation,
            "滑轨": rail
        }

        # 查询示例数据片段
        fsql = """
        SELECT 实例编号, 层数, 行数, 风道类型, 通风要求, 滑轨, 总高, 备注说明
        FROM 示例数据片段表
        """
        rows = self.sql_helper.fetch_data(fsql)

        # 初始化最大相似度和对应的实例
        max_similarity = 0
        max_similarity_instance = None

        # 遍历每个示例数据，计算相似度
        for row in rows:
            match_count = 0  # 重置匹配计数器

            # 检查每个条件是否匹配
            if str(row[1]) == conditions["层数"]:  # 确保类型一致
                match_count += 1
            if str(row[2]) == conditions["行数"]:  # 确保类型一致
                match_count += 1
            if row[3] == conditions["风道类型"]:  # 字符串比较
                match_count += 1
            if row[4] == conditions["通风要求"]:  # 字符串比较
                match_count += 1
            if row[5] == conditions["滑轨"]:  # 字符串比较
                match_count += 1

            # 计算相似度，分母固定为5
            similarity = match_count / 5

            # 更新最大相似度和对应的实例
            if similarity > max_similarity:
                max_similarity = similarity
                max_similarity_instance = row

        # 输出用户输入的字段
        print("用户输入的字段：")
        for key, value in conditions.items():
            print(f"{key}: {value}")

        # 输出示例数据的字段
        print("\n示例数据的字段：")
        for row in rows:
            print(row)

        # 输出匹配成功的示例数据的字段
        if max_similarity_instance:
            print("\n匹配成功的示例数据的字段：")
            print(max_similarity_instance)
            print(f"匹配个数：{match_count}")
            print(f"分母：5")
            print(f"分子：{match_count}")
        else:
            print("\n未找到匹配的实例")

        # 输出相似度
        if max_similarity_instance:
            print(f"\n相似度：{max_similarity:.2f}")
        else:
            print("\n相似度：未找到匹配的实例")

        # 显示推荐结果
        if max_similarity_instance:
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, "推荐结果：\n")

            # 实例说明
            self.recommendation_text.insert(tk.END, f"我们为您推荐实例编号：{max_similarity_instance[0]}\n")
            self.recommendation_text.insert(tk.END, f"相似度：{max_similarity:.2f}\n\n")

            # 详细解释
            if max_similarity == 1.0:
                self.recommendation_text.insert(tk.END, "这个实例与您的需求完全匹配！\n")
                self.recommendation_text.insert(tk.END, "所有条件都完全符合您的设定。\n")
                self.recommendation_text.insert(tk.END, "您可以直接参考这个实例进行育秧架的设计和配置。")
            elif max_similarity > 0.75:
                self.recommendation_text.insert(tk.END, "这个实例与您的需求非常接近！\n")
                self.recommendation_text.insert(tk.END, "大部分条件都符合您的设定，只有少部分小差异。\n")
                self.recommendation_text.insert(tk.END, "您可以参考这个实例，稍作调整即可满足您的需求。")
            elif max_similarity > 0.5:
                self.recommendation_text.insert(tk.END, "这个实例与您的需求较为接近。\n")
                self.recommendation_text.insert(tk.END, "一半以上的条件都符合您的设定。\n")
                self.recommendation_text.insert(tk.END, "您可以参考这个实例，结合实际情况进行较大调整。")
            elif max_similarity > 0.25:
                self.recommendation_text.insert(tk.END, "这个实例与您的需求有一定相似性。\n")
                self.recommendation_text.insert(tk.END, "少部分条件符合您的设定。\n")
                self.recommendation_text.insert(tk.END, "您可以参考这个实例作为基础，进行大量调整以满足您的需求。")
            else:
                self.recommendation_text.insert(tk.END, "这个实例与您的需求相似度较低。\n")
                self.recommendation_text.insert(tk.END, "只有极少数条件符合您的设定。\n")
                self.recommendation_text.insert(tk.END,
                                                "您可以参考这个实例的基本结构，但需要重新设计大部分参数以满足您的需求。")

            # 添加实例的详细信息
            self.recommendation_text.insert(tk.END, "\n\n推荐实例的详细信息：\n")
            self.recommendation_text.insert(tk.END, f"层数：{max_similarity_instance[1]}层\n")
            self.recommendation_text.insert(tk.END, f"行数：{max_similarity_instance[2]}行\n")
            self.recommendation_text.insert(tk.END, f"风道类型：{max_similarity_instance[3]}\n")
            self.recommendation_text.insert(tk.END, f"通风要求：{max_similarity_instance[4]}\n")
            self.recommendation_text.insert(tk.END, f"滑轨：{max_similarity_instance[5]}\n")
            self.recommendation_text.insert(tk.END, f"总高：{max_similarity_instance[6]}mm\n")
            self.recommendation_text.insert(tk.END, f"备注说明：{max_similarity_instance[7]}\n")

            # 显示相似度的计算方式
            self.recommendation_text.insert(tk.END, "\n相似度计算说明：\n")
            self.recommendation_text.insert(tk.END,
                                            f"相似度 = (匹配条件数 / 5) = {max_similarity:.2f}\n")
            self.recommendation_text.insert(tk.END, "匹配条件包括：层数、行数、风道类型、通风要求、滑轨")
        else:
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, "未找到匹配的实例\n")
            self.recommendation_text.insert(tk.END, "根据您的条件，目前数据库中没有完全匹配的实例。\n")
            self.recommendation_text.insert(tk.END, "建议您尝试调整一些条件，或者添加新的实例数据用于参考。")


if __name__ == "__main__":
    root = tk.Tk()
    app = FormShiLiChaXun(root)
    root.mainloop()