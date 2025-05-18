import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
# 推理引擎逻辑
def inference_engine(user_inputs):
    recommendations = []

    # 使用场所
    if user_inputs["使用场所"] == "玻璃温室":
        recommendations.append("推荐不锈钢横梁 + 透明顶风道")
    elif user_inputs["使用场所"] == "现代育苗工厂":
        recommendations.append("推荐自动化灌溉系统和环境控制系统")
    elif user_inputs["使用场所"] == "简易遮阳棚":
        recommendations.append("推荐轻便型可拆卸结构")

    # 管理方式
    if user_inputs["管理方式"] == "手动搬运":
        recommendations.append("不推荐使用滑轨；增加托盘留手孔")

    # 作业周期
    if user_inputs["作业周期"] == "高频育秧轮作":
        recommendations.append("推荐可拆卸模块化结构，缩短更换时间")
        if user_inputs["空间布局"].get("层数", 0) >= 6:
            recommendations.append("推荐模块化滑轨结构")

    # 空间布局
    if user_inputs["空间布局"].get("通道数量", 0) == 1:
        recommendations.append("推荐单侧进苗方向，避免风道与进苗冲突")

    # 环境等级
    if user_inputs["环境等级"] == "潮湿高腐蚀":
        recommendations.append("推荐防腐蚀涂层或不锈钢部件")
        recommendations.append("推荐所有钢结构切换为 304 不锈钢模板")
    elif user_inputs["环境等级"] == "低温霜冻":
        recommendations.append("推荐增加保温材料和加热系统")
    elif user_inputs["环境等级"] == "高温炎热":
        recommendations.append("推荐增加遮阳设施和通风系统")

    return recommendations

# 用户输入转换为字典关系
def convert_inputs_to_dict(inputs):
    input_dict = {
        "使用场所": inputs["使用场所"].get(),
        "安装方式": inputs["安装方式"].get(),
        "作业周期": inputs["作业周期"].get(),
        "通风条件": inputs["通风条件"].get(),
        "管理方式": inputs["管理方式"].get(),
        "环境等级": inputs["环境等级"].get(),
        "空间布局": {
            "进出口方向": inputs["空间布局_进出口方向"].get(),
            "棚室宽高": inputs["空间布局_棚室宽高"].get(),
            "通道数量": int(inputs["空间布局_通道数量"].get()),
            "层数": int(inputs["空间布局_层数"].get())
        }
    }
    return input_dict

class FormDeviceKnowledge:
    def __init__(self, parent):
        self.parent = parent

        # 设置样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", font=("Arial", 12))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TCombobox", font=("Arial", 12))
        style.configure("Treeview", font=("Arial", 11), rowheight=15)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

        # 创建主框架
        main_frame = ttk.Frame(self.parent, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # # 标题
        # title_label = ttk.Label(
        #     main_frame,
        #     text="育秧架知识推荐系统",
        #     font=("Arial", 16, "bold")
        # )
        # title_label.pack(pady=20)

        # 表格区域
        table_frame = ttk.Frame(main_frame, padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True)

        # 表格内容
        self.treeview = ttk.Treeview(
            table_frame,
            columns=("变量名称", "类型", "含义示例"),
            show="headings",
            style="Main.Treeview"
        )
        self.treeview.heading("变量名称", text="变量名称")
        self.treeview.heading("类型", text="类型")
        self.treeview.heading("含义示例", text="含义示例")

        # 设置列宽
        self.treeview.column("变量名称", width=130)
        self.treeview.column("类型", width=100)
        self.treeview.column("含义示例", width=500)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # 插入表格数据
        table_data = [
            ("使用场所", "枚举型", "温室大棚、现代育苗工厂、简易遮阳棚、露天场地、塑料大棚、智能温室、玻璃温室"),
            ("安装方式", "枚举型", "固定式、可拆卸式、可移动轮式"),
            ("作业周期", "文字说明", "短期集中出苗、高频育秧轮作、低频长苗期"),
            ("通风条件", "枚举型", "自然通风、侧窗送风、风道强制送风"),
            ("管理方式", "枚举型", "手动搬运、半自动链条输送、全自动立体栽培"),
            ("空间布局", "参数组", "进出口方向、棚室宽高、通道数量、层数、单通道布局、多通道布局、开放式布局、封闭式布局、模块化布局、立体式布局、平铺地面布局、移动苗床布局"),
            ("环境等级", "枚举型", "潮湿高腐蚀、温和干燥、低温霜冻、高温炎热、多尘环境、光照充足、通风良好、温湿度可控")
        ]
        for row in table_data:
            self.treeview.insert("", "end", values=row)

        # 用户输入和推荐结果区域
        input_and_result_frame = ttk.Frame(main_frame, padding="20")
        input_and_result_frame.pack(fill=tk.BOTH, expand=True)

        # 用户输入区域
        input_frame = ttk.Frame(input_and_result_frame, padding="5")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 输入字段
        self.inputs = {}
        fields = [
            ("使用场所", ttk.Combobox, ("温室大棚", "现代育苗工厂", "简易遮阳棚", "露天场地", "塑料大棚", "智能温室", "玻璃温室")),
            ("安装方式", ttk.Combobox, ("固定式", "可拆卸式", "可移动轮式")),
            ("作业周期", ttk.Combobox, ("短期集中出苗", "高频育秧轮作", "低频长苗期")),
            ("通风条件", ttk.Combobox, ("自然通风", "侧窗送风", "风道强制送风")),
            ("管理方式", ttk.Combobox, ("手动搬运", "半自动链条输送", "全自动立体栽培")),
            ("空间布局_进出口方向", ttk.Entry, None),
            ("空间布局_棚室宽高", ttk.Entry, None),
            ("空间布局_通道数量", ttk.Entry, None),
            ("空间布局_层数", ttk.Entry, None),
            ("空间布局_布局类型", ttk.Combobox, ("单通道布局", "多通道布局", "开放式布局", "封闭式布局", "模块化布局", "立体式布局", "平铺地面布局", "移动苗床布局")),
            ("环境等级", ttk.Combobox, ("潮湿高腐蚀", "温和干燥", "低温霜冻", "高温炎热", "多尘环境", "光照充足", "通风良好", "温湿度可控"))
        ]

        for i, (label, field_type, values) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, padx=5, pady=2, sticky=tk.W)
            if field_type == ttk.Entry:
                entry = ttk.Entry(input_frame, width=30)
            elif field_type == ttk.Combobox:
                entry = ttk.Combobox(input_frame, values=values, width=27)
            entry.grid(row=i, column=1, padx=5, pady=2, sticky=tk.W)
            self.inputs[label] = entry

        # 生成推荐按钮
        generate_button = ttk.Button(input_frame, text="生成推荐", command=self.generate_recommendations)
        generate_button.grid(row=len(fields), column=0, columnspan=2, pady=10)

        # 推荐结果区域
        result_frame = ttk.Frame(input_and_result_frame, padding="10")
        result_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.result_label = ttk.Label(result_frame, text="推荐结果", font=("Arial", 14, "bold"))
        self.result_label.pack(pady=10)
        self.result_text = tk.Text(result_frame, height=25, width=60)
        self.result_text.pack(pady=10)

    def generate_recommendations(self):
        try:
            user_inputs = convert_inputs_to_dict(self.inputs)
            recommendations = inference_engine(user_inputs)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "输入转换后的内容：\n")
            self.result_text.insert(tk.END, str(user_inputs) + "\n\n")
            self.result_text.insert(tk.END, "推荐结果：\n")
            self.result_text.insert(tk.END, "\n".join(recommendations))
        except Exception as e:
            messagebox.showerror("错误", f"生成推荐时发生错误: {e}")

    def get_frame(self):
        return self.parent

if __name__ == "__main__":
    root = tk.Tk()
    app = FormDeviceKnowledge(root)
    root.mainloop()