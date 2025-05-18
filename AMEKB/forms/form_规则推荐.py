import tkinter as tk
from tkinter import messagebox, ttk


class RiceTransplanterFrameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("育秧架设计系统")

        # 初始化参数
        self.N_layer = tk.IntVar()
        self.W_tray = tk.DoubleVar()
        self.N_row = tk.IntVar()
        self.N_col = tk.IntVar()
        self.pavilion_height = tk.DoubleVar()
        self.venue_max_width = tk.DoubleVar()
        self.ventilation = tk.StringVar()
        self.entry_direction = tk.StringVar()
        self.management_method = tk.StringVar()

        # 创建输入框
        tk.Label(root, text="层数:").grid(row=0, column=0, sticky="e")
        tk.Entry(root, textvariable=self.N_layer).grid(row=0, column=1)

        tk.Label(root, text="托盘宽度 (mm):").grid(row=1, column=0, sticky="e")
        tk.Entry(root, textvariable=self.W_tray).grid(row=1, column=1)

        tk.Label(root, text="托盘行数:").grid(row=2, column=0, sticky="e")
        tk.Entry(root, textvariable=self.N_row).grid(row=2, column=1)

        tk.Label(root, text="托盘列数:").grid(row=3, column=0, sticky="e")
        tk.Entry(root, textvariable=self.N_col).grid(row=3, column=1)

        tk.Label(root, text="棚高 (mm):").grid(row=4, column=0, sticky="e")
        tk.Entry(root, textvariable=self.pavilion_height).grid(row=4, column=1)

        tk.Label(root, text="场地最大宽度 (mm):").grid(row=5, column=0, sticky="e")
        tk.Entry(root, textvariable=self.venue_max_width).grid(row=5, column=1)

        # 创建下拉框
        tk.Label(root, text="通风需求:").grid(row=6, column=0, sticky="e")
        ttk.Combobox(root, textvariable=self.ventilation, values=["强", "中", "弱"]).grid(row=6, column=1)

        tk.Label(root, text="进苗方式:").grid(row=7, column=0, sticky="e")
        ttk.Combobox(root, textvariable=self.entry_direction, values=["单侧", "双侧"]).grid(row=7, column=1)

        tk.Label(root, text="管理方式:").grid(row=8, column=0, sticky="e")
        ttk.Combobox(root, textvariable=self.management_method,
                     values=["手动搬运", "半自动输送", "全自动立体栽培"]).grid(row=8, column=1)

        # 创建按钮
        tk.Button(root, text="运行设计分析", command=self.run_design_analysis).grid(row=9, column=0, columnspan=2)

    def calculate_total_height(self):
        N_layer = self.N_layer.get()
        return 187 + N_layer * 498

    def calculate_total_length(self):
        N_row = self.N_row.get()
        return 2317.5 + N_row * 410

    def calculate_total_width(self):
        N_col = self.N_col.get()
        W_tray = self.W_tray.get()
        return 2 * 209 + N_col * W_tray

    def apply_rules(self):
        H_total = self.calculate_total_height()
        L_total = self.calculate_total_length()
        W_total = self.calculate_total_width()
        N_row = self.N_row.get()
        N_layer = self.N_layer.get()
        W_tray = self.W_tray.get()
        N_col = self.N_col.get()
        pavilion_height = self.pavilion_height.get()
        venue_max_width = self.venue_max_width.get()
        ventilation = self.ventilation.get()
        entry_direction = self.entry_direction.get()

        warnings = []
        suggestions = []

        # 警告规则
        if H_total > pavilion_height:
            warnings.append(f"警告：根据行数和列数计算，育秧架的总高为{H_total} mm，而棚高为 {pavilion_height} mm，超出棚高")
        if W_tray * N_col > venue_max_width:
            warnings.append(
                f"警告：托盘宽度 × 列数超过场地最大宽度，当前总宽 {W_tray * N_col} mm，场地最大宽度 {venue_max_width} mm")
        if N_row > 18 and (L_total / N_row) < 900:
            warnings.append("警告：跨度过小")
        if self.entry_direction.get() == "无" and N_layer > 7:
            warnings.append("警告：建议添加滑轨限位")
        if pavilion_height < 3200 and N_layer == 8:
            warnings.append("警告：空间偏紧")

        # 推荐规则
        if N_row > 15:
            suggestions.append("推荐：加装滑轨模块")
        if W_total > 4200:
            suggestions.append("推荐：双侧进苗")
        if ventilation == "强":
            suggestions.append("推荐：风道类型 = 双侧")
        elif ventilation == "中":
            suggestions.append("推荐：风道类型 = 单侧风道")
        elif ventilation == "弱":
            suggestions.append("推荐：风道类型 = 左侧风道")
        if N_layer >= 6:
            suggestions.append("推荐：横梁类型 = 加强型")
        if H_total > 4000:
            suggestions.append("推荐：附加稳定支撑柱")
        if H_total > pavilion_height and N_layer > 6:
            suggestions.append("推荐：使用压缩型托盘")
        if entry_direction == "双侧":
            suggestions.append("推荐：风道布置 = 顶出式或内嵌式风道")
        if N_col == 6:
            suggestions.append("推荐：使用双层左右限位结构")
        if ventilation == "强" and W_tray > 600:
            suggestions.append("推荐：横梁间距 = 950 mm")
        if N_row == 15 and W_tray > 600:
            suggestions.append("推荐：横向滑轨 = 加装式")

        return warnings, suggestions

    def run_design_analysis(self):
        try:
            warnings, suggestions = self.apply_rules()

            H_total = self.calculate_total_height()
            L_total = self.calculate_total_length()
            W_total = self.calculate_total_width()

            if warnings:
                messagebox.showwarning("警告", "\n".join(warnings))
            else:
                result_message = (
                    f"推荐的育秧架尺寸:\n"
                    f"总高: {H_total} mm\n"
                    f"总长: {L_total} mm\n"
                    f"总宽: {W_total} mm\n"
                )
                if suggestions:
                    result_message += "推荐:\n" + "\n".join(suggestions)
                else:
                    result_message += "未触发任何推荐机制"
                messagebox.showinfo("设计结果", result_message)
        except Exception as e:
            messagebox.showerror("错误", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = RiceTransplanterFrameApp(root)
    root.mainloop()

# class RiceTransplanterFrame:
#     def __init__(self):
#         # 初始化参数（表1和表2的参数）
#         self.N_layer = None  # 层数
#         self.H_each = 498  # 单层高度，默认值
#         self.W_tray = None  # 托盘宽度
#         self.N_row = None  # 托盘行数
#         self.N_col = None  # 托盘列数
#         self.pavilion_height = None  # 棚高（用户输入）
#         self.venue_max_width = None  # 场地最大宽度（用户输入）
#
#         # 初始化结构配置参数（表2）
#         self.beam_type = None  # 横梁类型
#         self.slide_type = None  # 滑轨设置
#         self.vent_layout = None  # 风道布局
#         self.tray_arrangement = None  # 托盘排列方式
#         self.frame_material = None  # 架体材料建议
#         self.entry_direction = None  # 进苗方向
#
#         # 初始化公式计算结果
#         self.H_total = None  # 架体总高
#         self.L_total = None  # 架体总长
#         self.W_total = None  # 架体总宽
#
#     def calculate_total_height(self):
#         """计算架体总高（公式1）"""
#         if self.N_layer is None:
#             return None
#         self.H_total = 187 + self.N_layer * self.H_each
#         return self.H_total
#
#     def calculate_total_length(self):
#         """计算架体总长（公式2）"""
#         if self.N_row is None:
#             return None
#         self.L_total = 2317.5 + self.N_row * 410
#         return self.L_total
#
#     def calculate_total_width(self):
#         """计算架体总宽（公式3）"""
#         if self.N_col is None or self.W_tray is None:
#             return None
#         self.W_total = 2 * 209 + self.N_col * self.W_tray
#         return self.W_total
#
#     def check_height_limit(self):
#         """高度校验（公式4）"""
#         if self.H_total is None or self.pavilion_height is None:
#             return False
#         return self.H_total > self.pavilion_height
#
#     def check_row_limit(self):
#         """行数校验（公式5）"""
#         if self.N_row is None:
#             return False
#         return self.N_row > 15
#
#     def apply_structure_safety_rules(self):
#         """应用结构安全规则（表4）"""
#         # 规则R1: 层数≥6时使用加强型横梁
#         if self.N_layer >= 6:
#             self.beam_type = "加强型"
#
#         # 规则R2: 高度超过棚高时提示警告
#         if self.H_total is not None and self.pavilion_height is not None:
#             if self.H_total > self.pavilion_height:
#                 self.show_warning("高度超限")
#
#         # 规则R3: 托盘总宽度超过场地最大宽度时提示调整
#         if self.W_tray is not None and self.N_col is not None and self.venue_max_width is not None:
#             total_width = self.W_tray * self.N_col
#             if total_width > self.venue_max_width:
#                 self.show_warning("宽度超限，建议降低列数或增加间距")
#
#     def apply_functional_rules(self):
#         """应用功能配置规则（表5）"""
#         # 规则R4: 通风需求强时使用双侧风道
#         # 此处需要通风需求参数，暂不实现
#
#         # 则R5: 行数≥15时使用加强型滑轨
#         if self.N_row >= 15:
#             self.slide_type = "加强型"
#
#         # 规则R6: 双侧进苗时使用顶出式或内嵌式风道
#         # 此处需要进苗方式参数，暂不实现
#
#     def apply_parameter_linking_rules(self):
#         """应用参数联动与派生规则（表6）"""
#         # 规则R7: 根据层数计算总高
#         self.calculate_total_height()
#
#         # 规则R8: 根据行数计算总长
#         self.calculate_total_length()
#
#         # 规则R9: 列数=6时推荐使用双层左右限位结构
#         if self.N_col == 6:
#             self.show_suggestion("推荐使用双层左右限位结构")
#
#     def apply_module_call_rules(self):
#         """应用模块调用规则（表7）"""
#         # 规则R10: 加强型横梁使用特定模板
#         # 规则R11: 根据风道类型调用特定模块
#         # 规则R12: 总高>4000mm时附加稳定支撑柱
#         pass
#
#     def apply_exception_handling_rules(self):
#         """应用异常处理与预警规则（表8）"""
#         # 规则R13: 总高超过棚高时提示警告
#         if self.H_total is not None and self.pavilion_height is not None:
#             if self.H_total > self.pavilion_height:
#                 self.show_warning("架体高度超限，建议减层")
#
#         # 规则R14: 行数>18且横梁间距<900时提示跨度过小
#         # 需要横梁间距参数，暂不实现
#
#         # 规则R15: 层数>7且无滑轨时建议添加滑轨限位
#         if self.N_layer > 7 and self.slide_type == "无":
#             self.show_suggestion("建议添加滑轨限位")
#
#     def show_warning(self, message):
#         """显示警告信息"""
#         print(f"警告: {message}")
#
#     def show_suggestion(self, message):
#         """显示建议信息"""
#         print(f"建议: {message}")
#
#     def run_design_analysis(self):
#         """运行设计分析"""
#         print("开始育秧架设计分析...")
#
#         # 计算基本尺寸
#         self.calculate_total_height()
#         self.calculate_total_length()
#         self.calculate_total_width()
#
#         # 检查基本限制
#         height_exceeded = self.check_height_limit()
#         if height_exceeded:
#             self.show_warning(f"架体总高 {self.H_total} 超过棚高 {self.pavilion_height}")
#
#         row_exceeded = self.check_row_limit()
#         if row_exceeded:
#             self.show_suggestion("托盘行数超过15，建议考虑滑轨设置")
#
#         # 应用所有设计规则
#         self.apply_structure_safety_rules()
#         self.apply_functional_rules()
#         self.apply_parameter_linking_rules()
#         self.apply_module_call_rules()
#         self.apply_exception_handling_rules()
#
#         print("设计分析完成！")
#
#     def get_design_results(self):
#         """获取设计结果"""
#         results = {
#             "H_total": self.H_total,
#             "L_total": self.L_total,
#             "W_total": self.W_total,
#             "beam_type": self.beam_type,
#             "slide_type": self.slide_type,
#             "vent_layout": self.vent_layout,
#             "tray_arrangement": self.tray_arrangement,
#             "frame_material": self.frame_material,
#             "entry_direction": self.entry_direction
#         }
#         return results
#
#
# # 示例用法
# if __name__ == "__main__":
#     # 创建育秧架实例
#     frame = RiceTransplanterFrame()
#
#     # 设置用户输入参数
#     frame.N_layer = 6
#     frame.W_tray = 623.7
#     frame.N_row = 12
#     frame.N_col = 4
#     frame.pavilion_height = 3200  # 用户输入的棚高
#     frame.venue_max_width = 3000  # 用户输入的场地最大宽度
#
#     # 运行设计分析
#     frame.run_design_analysis()
#
#     # 获取设计结果
#     results = frame.get_design_results()
#     print("\n最终设计结果:")
#     for key, value in results.items():
#         print(f"{key}: {value}")