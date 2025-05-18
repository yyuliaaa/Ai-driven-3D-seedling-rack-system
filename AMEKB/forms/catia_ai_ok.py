import os
import re
import subprocess
import sys
import time
import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox, simpledialog
import win32com.client
# current_dir = os.path.dirname(os.path.abspath(__file__))
# catia_integration_path = os.path.join(current_dir, "..", "catia_integration")
# sys.path.append(catia_integration_path)

#from catia_operator_0_很久之前 import CATIAOperator
#from catia_integration.catia_operator_0_很久之前 import CATIAOperator
#from catia_integration.catia_operator_0_很久之前 import CATIAOperator
import json
import requests
from configparser import ConfigParser
import logging
from loguru import logger
import csv
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
import win32com.client

import pythoncom
import win32com.client
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import os
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
class FormKnowledgeDesign:
    def __init__(self, root):
        # 初始化 COM 库
        pythoncom.CoInitialize()

        self.root = root
        self.root.title("基于知识的设计")
        self.root.geometry("600x500")
        self.root.minsize(600, 500)

        # 初始化 CATIA 操作器和当前参数
        self.catia_operator = None
        self.current_parameters = {'layers': 0, 'rows': 0, 'trays_per_row': 0}
        self.current_dimensions = {'length': 0, 'width': 0, 'height': 0}

        # 初始化 NLP 处理器
        config_path = os.path.join(os.path.dirname(__file__), 'settings.ini')
        self.nlp_processor = NLPProcessor(config_path, catia_operator=self.catia_operator, current_parameters=self.current_parameters)

        # 设置样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TRadiobutton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TFrame", background="#f0f0f0")

        # 创建主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        title_label = ttk.Label(
            main_frame,
            text="基于知识的设计",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=20)

        # 选项区域
        options_frame = ttk.Frame(main_frame)
        options_frame.pack(pady=10, fill=tk.X)

        # 选择设计类型
        self.radio_var = tk.IntVar()
        ttk.Radiobutton(
            options_frame,
            text="育秧架",
            variable=self.radio_var,
            value=1,
            command=self.reset_entries
        ).pack(side=tk.LEFT, padx=20)
        ttk.Radiobutton(
            options_frame,
            text="其他设计",
            variable=self.radio_var,
            value=2
        ).pack(side=tk.LEFT, padx=20)

        # 按钮区域
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(pady=20, fill=tk.X)

        # 确定按钮
        self.btn_ok = ttk.Button(
            buttons_frame,
            text="确定",
            command=self.on_ok,
            width=20
        )
        self.btn_ok.pack(pady=10, padx=10, fill=tk.X)

        # 打开CATIA按钮
        self.btn_open_catia = ttk.Button(
            buttons_frame,
            text="打开CATIA",
            command=self.open_catia,
            width=20
        )
        self.btn_open_catia.pack(pady=10, padx=10, fill=tk.X)

        # 基础版AI交互按钮
        self.btn_ai_interaction_basic = ttk.Button(
            buttons_frame,
            text="基础版AI交互",
            command=self.open_basic_ai_interaction,
            width=20
        )
        self.btn_ai_interaction_basic.pack(pady=10, padx=10, fill=tk.X)

        # 升级版CATIA AI交互按钮
        self.btn_ai_interaction_advanced = ttk.Button(
            buttons_frame,
            text="升级版CATIA AI交互",
            command=self.open_ai_interaction,
            width=20
        )
        self.btn_ai_interaction_advanced.pack(pady=10, padx=10, fill=tk.X)

    def on_ok(self):
        if self.radio_var.get() == 1:
            # 打开输入窗口
            self.input_parameters()

    def reset_entries(self):
        # 重置输入字段或清除当前参数
        self.current_parameters = {'layers': 0, 'rows': 0, 'trays_per_row': 0}
        self.current_dimensions = {'length': 0, 'width': 0, 'height': 0}
        messagebox.showinfo("重置", "所有输入字段已重置")

    def input_parameters(self):
        user_input = simpledialog.askstring("输入",
                                            self.nlp_processor._SYSTEM_PROMPT,
                                            parent=self.root)
        if not user_input:
            messagebox.showerror("错误", "请输入所有必填字段")
            return

        try:
            # 调用 NLP 处理器处理用户输入
            response = self.nlp_processor.process_user_input(user_input)
            messagebox.showinfo("AI 响应", response)
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def input_layers(self):
        # 获取用户输入的层数
        layers = simpledialog.askstring(
            "输入",
            "层数（输入偶数，最大30层）：",
            parent=self.root
        )
        if layers is None:  # 检查是否点击了Cancel
            return
        if layers and layers.isdigit() and int(layers) % 2 == 0 and int(layers) <= 30:
            # 打开第二个输入窗口
            self.input_rows(int(layers))
        else:
            messagebox.showerror("错误", "请输入一个偶数且不超过30层")
            self.input_layers()

    def input_rows(self, layers):
        # 获取用户输入的行数
        rows = simpledialog.askinteger(
            "输入",
            "行数：",
            parent=self.root
        )
        if rows is None:  # 检查是否点击了Cancel
            return
        if rows is not None:
            # 打开第三个输入窗口
            self.input_trays_per_row(rows, layers)

    def input_trays_per_row(self, rows, layers):
        # 获取用户输入的每行托盘数
        trays_per_row = simpledialog.askinteger(
            "输入",
            "每行托盘数：",
            parent=self.root
        )
        if trays_per_row is None:  # 检查是否点击了Cancel
            return
        if trays_per_row is not None:
            # 计算育秧架尺寸
            length, width, height = self.calculate_dimensions(rows, trays_per_row, layers)
            # 检查长度是否超过27米
            if length > 27000:  # 27米转换为毫米
                messagebox.showwarning("警告", "根据电机和架体强度，育秧架总长度不能超过27m")
                return
            # 保存当前参数和尺寸
            self.current_parameters = {'layers': layers, 'rows': rows, 'trays_per_row': trays_per_row}
            self.current_dimensions = {'length': length, 'width': width, 'height': height}
            # 显示推荐尺寸
            self.show_recommendation(length, width, height)

    def calculate_dimensions(self, rows, trays_per_row, layers):
        # 根据用户输入计算尺寸
        # 高=底座（187mm）+层数（输入）+层高（498mm）
        height = 187 + layers * 497.946 - 153
        # 长=扩展架长（2317.5mm） + 行数（输入） X 行长（410mm）
        length = 2317.5 + rows * 410
        # 宽=余量（209mm X 2=418mm） + 每行托盘数（输入） X 托盘宽（623.7mm）
        width = 418 + trays_per_row * 623.7

        # 检查长度是否超过20000mm
        if length > 20000:  # 20000mm
            raise ValueError("根据电机和架体强度，育秧架总长度不能超过20000mm")

        return length, width, height

    def show_recommendation(self, length, width, height):
        # 显示推荐尺寸
        recommendation_window = tk.Toplevel(self.root)
        recommendation_window.title("推荐尺寸")
        recommendation_window.geometry("500x300")
        recommendation_window.minsize(500, 300)

        # 设置样式
        style = ttk.Style(recommendation_window)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 12), padding=10)

        # 创建主框架
        main_frame = ttk.Frame(recommendation_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(
            main_frame,
            text="根据您的输入，为您推荐合适地育秧架尺寸：",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # 尺寸信息
        ttk.Label(main_frame, text=f"长：{length} mm").pack(pady=5)
        ttk.Label(main_frame, text=f"宽：{width} mm").pack(pady=5)
        ttk.Label(main_frame, text=f"高：{height} mm").pack(pady=5)

        # 按钮
        ttk.Button(
            main_frame,
            text="在CATIA查看为您设计的育秧架",
            command=lambda: self.modify_and_open_catia(length, width, height)
        ).pack(pady=20)

    def modify_and_open_catia(self, length, width, height):
        try:
            if self.catia_operator is None:
                self.catia_operator = CATIAOperator()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
            self.catia_operator.open_document(file_path)
            self.catia_operator.set_dimensions(length=length, width=width, height=height)
            self.current_dimensions = {'length': length, 'width': width, 'height': height}
            self.btn_modify_parameters.config(state=tk.NORMAL)
            messagebox.showinfo("成功", "模型已更新并在CATIA中打开")

            # 在命令行输出修改后的模型尺寸
            print(f"修改后的模型尺寸：长={length}mm，宽={width}mm，高={height}mm")
        except Exception as e:
            messagebox.showerror("错误", f"修改模型时发生错误: {e}")

    def open_catia(self):
        try:
            if self.catia_operator is None:
                self.catia_operator = CATIAOperator()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
            self.catia_operator.open_document(file_path)
        except Exception as e:
            messagebox.showerror("错误", f"打开文件时发生错误: {e}")

    def open_basic_ai_interaction(self):
        # 创建基础版 AI 交互窗口
        basic_ai_interaction_window = BasicAIInteractionWindow(
            parent=self.root,  # 当前窗口作为父窗口
            catia_operator=self.catia_operator,  # 当前的 CATIA 操作器
            current_parameters=self.current_parameters  # 当前的参数
        )

    def open_ai_interaction(self):
        # 创建升级版 AI 交互窗口
        advanced_ai_interaction_window = AIInteractionWindow(
            parent=self.root,  # 当前窗口作为父窗口
            catia_operator=self.catia_operator,  # 当前的 CATIA 操作器
            current_parameters=self.current_parameters  # 当前的参数
        )

    def open_modify_parameters(self):
        # 打开修改参数窗口
        modify_window = tk.Toplevel(self.root)
        modify_window.title("修改参数")
        modify_window.geometry("400x300")
        modify_window.minsize(400, 300)

        # 设置样式
        style = ttk.Style(modify_window)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 12), padding=10)

        # 创建主框架
        main_frame = ttk.Frame(modify_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 当前参数显示
        ttk.Label(main_frame, text="当前参数:").pack(pady=5)
        ttk.Label(main_frame, text=f"层数：{self.current_parameters['layers']}").pack(pady=5)
        ttk.Label(main_frame, text=f"行数：{self.current_parameters['rows']}").pack(pady=5)
        ttk.Label(main_frame, text=f"每行托盘数：{self.current_parameters['trays_per_row']}").pack(pady=5)

        # 新参数输入
        ttk.Label(main_frame, text="新参数:").pack(pady=10)

        # 层数输入
        layers_frame = ttk.Frame(main_frame)
        layers_frame.pack(fill=tk.X, pady=5)
        ttk.Label(layers_frame, text="层数（偶数）:").pack(side=tk.LEFT)
        self.layers_entry = ttk.Entry(layers_frame)
        self.layers_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.layers_entry.insert(0, str(self.current_parameters['layers']))

        # 行数输入
        rows_frame = ttk.Frame(main_frame)
        rows_frame.pack(fill=tk.X, pady=5)
        ttk.Label(rows_frame, text="行数:").pack(side=tk.LEFT)
        self.rows_entry = ttk.Entry(rows_frame)
        self.rows_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.rows_entry.insert(0, str(self.current_parameters['rows']))

        # 每行托盘数输入
        trays_frame = ttk.Frame(main_frame)
        trays_frame.pack(fill=tk.X, pady=5)
        ttk.Label(trays_frame, text="每行托盘数:").pack(side=tk.LEFT)
        self.trays_entry = ttk.Entry(trays_frame)
        self.trays_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.trays_entry.insert(0, str(self.current_parameters['trays_per_row']))

        # 确认按钮
        ttk.Button(
            main_frame,
            text="确认修改",
            command=self.confirm_parameter_modification
        ).pack(pady=20)

    def confirm_parameter_modification(self):
        try:
            # 获取新参数
            new_layers = int(self.layers_entry.get())
            new_rows = int(self.rows_entry.get())
            new_trays_per_row = int(self.trays_entry.get())

            # 验证输入
            if new_layers % 2 != 0:
                messagebox.showerror("错误", "层数必须为偶数")
                return

            if new_layers <= 0 or new_rows <= 0 or new_trays_per_row <= 0:
                messagebox.showerror("错误", "参数必须为正数")
                return

            # 计算新尺寸
            new_length, new_width, new_height = self.calculate_dimensions(
                new_rows,
                new_trays_per_row,
                new_layers
            )

            # 更新CATIA模型
            if self.catia_operator is None:
                self.catia_operator = CATIAOperator()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
            self.catia_operator.open_document(file_path)
            self.catia_operator.set_dimensions(
                length=new_length,
                width=new_width,
                height=new_height
            )

            # 更新当前参数和尺寸
            self.current_parameters = {
                'layers': new_layers,
                'rows': new_rows,
                'trays_per_row': new_trays_per_row
            }
            self.current_dimensions = {
                'length': new_length,
                'width': new_width,
                'height': new_height
            }

            messagebox.showinfo("成功", "模型参数已更新")
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数字")
        except Exception as e:
            messagebox.showerror("错误", f"修改参数时发生错误: {e}")

    def __del__(self):
        # 释放 COM 库
        pythoncom.CoUninitialize()
import logging
import requests
import json
from configparser import ConfigParser

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EnhancedNLPProcessor:
    _SYSTEM_PROMPT = """
    您是一位专业的农业机械知识库人工智能助手。请帮助用户了解育秧架的相关知识，告知用户所有的必填、选填字段。引导用户输入字段，以获取用户所需的育秧架尺寸（长、宽、高），并给予推荐和警告。用户对CATIA和育秧架不太熟悉，请您以简洁易懂的方式全面指导用户。
    **必填字段**：
    - 层数 (N_layer)：整数
    - 托盘行数 (N_row)：整数
    - 每行托盘数 (N_col)：整数
    - 棚高 (Pavilion_Height)：浮点数
    - 场地最大宽度 (Venue_Max_Width)：浮点数
    - 通风需求 (Ventilation_Requirement)：Strong/Medium/Low
    - 进苗方式 (Entry_Direction)：Single Side/Double Side
    - 管理方式 (Management_Method)：Manual Handling/Semi-Automatic Conveying/Fully Automatic Cultivation
    - 横梁类型 (Beam_Type)：字符串
    - 风道布置 (Vent_Layout)：double-sided/single-sided
    - 滑轨类型 (Slide_Type)：标准/加强/无
    - 使用场所 (Usage_Place)：温室大棚/现代育苗工厂/简易遮阳棚
    - 安装方式 (Installation_Method)：固定式/可拆卸式/可移动轮式
    - 作业周期 (Operation_Cycle)：短期集中出苗/高频育秧轮作/低频长苗期
    - 通风条件 (Ventilation_Condition)：自然通风/侧窗送风/风道强制送风
    - 环境等级 (Environment_Level)：潮湿高腐蚀/温和干燥/低温霜冻等
    - 风道配置 (Ventilation_Configuration)：左风道/双风道/顶风道

    ### 选填字段：
    - **托盘宽度 (W_tray)**：浮点数，托盘的宽度，单位为毫米。
    - **间隙宽度 (W_gap)**：浮点数，托盘之间的间隙宽度，单位为毫米。
    - **基础高度 (H_base)**：浮点数，育秧架的基础高度，单位为毫米。
    - **每层高度 (H_each)**：浮点数，每层的高度，单位为毫米。
    - **基础长度 (L_base)**：浮点数，育秧架的基础长度，单位为毫米。
    - **托盘长度 (L_tray)**：浮点数，托盘的长度，单位为毫米。
    - **空间布局 (Space_Layout)**：参数组，用于描述空间布局的详细信息。
    - **托盘总面积 (A_tray_total)**：浮点数，所有托盘的总面积，单位为平方毫米。

    **提示**：
    一定要检查用户能够一次性输入所有必填字段，用户输入格式示例：
    层数: 4
    托盘行数: 5
    每行托盘数: 6
    棚高: 3000
    场地最大宽度: 4000
    通风需求: Strong
    进苗方式: Single Side
    管理方式: Manual Handling
    横梁类型: 标准
    风道布置: double-sided
    滑轨类型: 标准
    使用场所: 温室大棚
    安装方式: 固定式
    作业周期: 短期集中出苗
    通风条件: 自然通风
    环境等级: 温和干燥
    风道配置: 左风道

    参数表：
    parameter,description,options,required
    N_layer,层数,整数,是
    W_tray,托盘宽度,浮点数,否
    N_row,托盘行数,整数,是
    N_col,托盘列数,整数,是
    Pavilion_Height,棚高,浮点数,是
    Venue_Max_Width,场地最大宽度,浮点数,是
    Ventilation_Requirement,通风需求,Strong/Medium/Low,是
    Entry_Direction,进苗方式,Single Side/Double Side,是
    Management_Method,管理方式,Manual Handling/Semi-Automatic Conveying/Fully Automatic Cultivation,是
    Beam_Type,横梁类型,字符串,是
    W_gap,间隙宽度,浮点数,否
    H_base,基础高度,浮点数,否
    H_each,每层高度,浮点数,否
    L_base,基础长度,浮点数,否
    L_tray,托盘长度,浮点数,否
    Vent_Layout,风道布置,double-sided/single-sided,是
    Slide_Type,滑轨类型,标准/加强/无,是
    Usage_Place,使用场所,温室大棚/现代育苗工厂/简易遮阳棚,否
    Installation_Method,安装方式,固定式/可拆卸式/可移动轮式,否
    Operation_Cycle,作业周期,短期集中出苗/高频育秧轮作/低频长苗期,否
    Ventilation_Condition,通风条件,自然通风/侧窗送风/风道强制送风,否
    Space_Layout,空间布局,参数组,否
    Environment_Level,环境等级,潮湿高腐蚀/温和干燥/低温霜冻等,否
    Ventilation_Configuration,风道配置,左风道/双风道/顶风道,否
    Ventilation_Requirement,通风要求,强/中/弱,否

    规则表：
    condition,message
    H_total > Pavilion_Height,"警告：超出棚高"
    N_row > 15,"推荐：加装滑轨模块"
    W_total > 4.2,"推荐：双侧进苗"
    Ventilation_Requirement == 'Strong',"推荐：双风道"
    N_layer >= 6,"推荐：横梁类型 = 加强型"
    H_total > Pavilion_Height,"警告：高度超限"
    W_tray * N_col > Venue_Max_Width,"警告：降低列数或间距"
    Ventilation_Requirement == 'Strong',"推荐：风道类型 = 双侧"
    Ventilation_Requirement == 'Low',"推荐：风道类型 = 左侧风道"
    Ventilation_Requirement == 'Medium',"推荐：风道类型 = 单侧风道"
    N_row >= 15,"推荐：滑轨 = 加强型"
    Entry_Direction == 'Double Side',"推荐：风道布置 = 顶出式或内嵌式风道"
    N_col == 6,"推荐：使用双层左右限位结构"
    Beam_Type == '加强型',"推荐：模板 = CATIA_Beam_Strong.CATPart"
    Vent_Layout == 'double-sided',"推荐：调用 SD-L 风道模块"
    H_total > 4000,"推荐：附加稳定支撑柱"
    H_total > Pavilion_Height,"警告：架体高度超限，建议减层"
    Beam_Type == '加强型' and L_tray > 600,"推荐：横梁间距 = 1000mm"
    W_gap <= 1000 and H_total <= 2.8,"推荐：风道布置 = 左通风"
    N_row > 18 and W_gap < 900,"警告：跨度过小"
    Slide_Type == '无' and N_layer > 7,"提示：建议添加滑轨限位"
    H_total > Pavilion_Height and N_layer > 6,"推荐：使用压缩型托盘"
    L_tray > 600,"警告：横梁间距需减小，推荐≤1000 mm"
    Beam_Type == '加强型' and L_tray > 600,"推荐：横梁间距 = 950 mm"
    W_gap <= 1000 and N_row == 15,"推荐：横向滑轨 = 加装式"
    Pavilion_Height < 3200 and N_layer == 8,"警告：空间偏紧"
    使用场所 == '玻璃温室',"推荐：不锈钢横梁 + 透明顶风道"
    管理方式 == '手动',"不推荐使用滑轨；增加托盘留手孔"
    作业周期 == '高频',"推荐：可拆卸模块化结构，缩短更换时间"
    空间布局 == '单通道',"推荐：单侧进苗方向，避免风道与进苗冲突"
    环境等级 == '高腐蚀',"推荐：防腐蚀涂层或不锈钢部件"

    公式：
    H_total=H_base+N_layer*H_each, H_base=187mm, H_each=498mm
    L_total=L_base+N_row*L_tray, L_base=2317.5mm, L_tray=410mm
    W_total=2*W_gap+N_col*W_tray, W_gap=209mm, W_tray=623.7mm

    其中 H_base=187mm，H_each=498mm，L_base=2317.5mm, L_tray=410mm，W_gap=209mm, W_tray=623.7mm 是初始默认值，若用户未告知 H_base、H_each、L_base、L_tray、W_gap、W_tray 则用默认值计算。

    ### 用户输入监督
    在用户输入参数时，请确保所有必填字段（标记为“是”的字段）都已提供。如果用户未提供某些必填字段，请提示用户输入这些字段。例如：
    - 如果用户未输入“层数 (N_layer)”，请提示：“请提供层数 (N_layer)。”
    - 如果用户未输入“托盘行数 (N_row)”，请提示：“请提供托盘行数 (N_row)。”
    """

    def __init__(self, config_path=None, catia_operator=None, current_parameters=None):
        self.config = ConfigParser()
        if config_path is None:
            config_path = os.path.join(current_dir, "..", "config", "settings.ini")

        self.config.read(config_path)
        self._setup_api()

        # 初始化 CATIA 操作器和当前参数
        self.catia_operator = catia_operator
        self.current_parameters = current_parameters if current_parameters is not None else {'layers': 0, 'rows': 0, 'trays_per_row': 0}

    def _setup_api(self):
        self.api_url = self.config.get('API', 'deepseek_url')
        self.api_key = self.config.get('API', 'api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _load_parameters(self):
        required_params = {}
        with open('./parameters.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                required_params[row['parameter']] = {
                    'description': row['description'],
                    'required': row['required'] == '是',
                    'default': row.get('default', None)
                }
        return required_params

    def _load_rules(self):
        rules = []
        with open('./rules.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                rules.append((row['condition'], row['message']))
        return rules

    def parse_command(self, user_input: str) -> dict:
        try:
            payload = {
                "model": "Qwen/Qwen2.5-7B-Instruct",
                "messages": [
                    {"role": "system", "content": self._SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.2
            }
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=500
            )
            response.raise_for_status()
            logger.info(f"API 返回数据: {response.json()}")
            return self._validate_output(response.json())
        except requests.RequestException as e:
            logger.error(f"API 请求失败: {str(e)}")
            raise Exception("自然语言处理服务不可用") from e

    def add_message(self, sender, message):
        print(f"{sender}: {message}")

    def update_model_parameters(self, layers, rows, trays_per_row):
        try:
            # 检查层数是否超过30层
            if layers > 30:
                raise ValueError("层数不能超过30层")

            # 检查层数是否为偶数
            if layers % 2 != 0:
                raise ValueError("层数必须是偶数")

            # 计算新尺寸
            length, width, height = self.calculate_dimensions(rows, trays_per_row, layers)

            # 更新 CATIA 模型
            if self.catia_operator is None:
                self.catia_operator = CATIAOperator()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
            self.catia_operator.open_document(file_path)
            self.catia_operator.set_dimensions(length=length, width=width, height=height)

            # 更新当前参数和尺寸
            self.current_parameters = {
                'layers': layers,
                'rows': rows,
                'trays_per_row': trays_per_row
            }

            return f"模型参数已更新。更新后的参数如下：\n长: {length}mm\n宽: {width}mm\n高: {height}mm"
        except Exception as e:
            return f"发生错误: {str(e)}"
    def _validate_output(self, response: dict) -> dict:
        try:
            choices = response.get('choices', [])
            if not choices:
                raise ValueError("API返回结果中没有找到有效的数据")

            raw_data = choices[0].get('message', {}).get('content', '')
            data = json.loads(raw_data)

            if not all(key in data for key in ('operation', 'parameters')):
                raise ValueError("无效的命令结构")

            valid_operations = {
                'PartDesign.Pad',
                'PartDesign.Pocket',
                'PartDesign.SetDimensions',
                'PartDesign.UpdateModel',
                'OpenCATIA'
            }
            if data['operation'] not in valid_operations:
                raise ValueError("不支持的CATIA操作")

            return data
        except json.JSONDecodeError:
            logging.info("检测到非JSON输出，按普通聊天处理")
            return {
                "response": "普通聊天",
                "message": raw_data
            }
        except Exception as e:
            logging.error(f"命令解析失败：{str(e)}")
            return {
                "response": "普通聊天",
                "message": raw_data
            }

    def process_user_input(self, user_input: str) -> str:
        try:
           result = self.parse_command(user_input)
           if result.get('response') == '普通聊天':
               return result.get('message', "这是一个普通聊天。")
           else:
               operation = result['operation']
               parameters = result['parameters']

               if operation == "OpenCATIA":
                   if self.catia_operator is None:
                       self.catia_operator = CATIAOperator()
                   current_dir = os.path.dirname(os.path.abspath(__file__))
                   file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
                   self.catia_operator.open_document(file_path)
                   return "CATIA已打开"

               elif operation == "PartDesign.SetDimensions":
                   new_layers = parameters.get('layers', self.current_parameters['layers'])
                   new_rows = parameters.get('rows', self.current_parameters['rows'])
                   new_trays_per_row = parameters.get('trays_per_row', self.current_parameters['trays_per_row'])
                   response = self.update_model_parameters(new_layers, new_rows, new_trays_per_row)
                   return response

               elif operation == "PartDesign.UpdateModel":
                   current_layers = self.current_parameters['layers']
                   current_rows = self.current_parameters['rows']
                   current_trays_per_row = self.current_parameters['trays_per_row']
                   response = self.update_model_parameters(current_layers, current_rows, current_trays_per_row)
                   return response

               elif operation == "CloseCATIA":
                   if self.catia_operator and self.catia_operator.catia:
                       self.catia_operator.catia.Quit()
                       self.catia_operator = None
                       return "CATIA已关闭"
                   else:
                       return "CATIA未打开"
               else:
                   return f"抱歉，我不支持该操作: {operation}"
        except Exception as e:
           logging.error(f"处理用户输入时发生错误: {str(e)}")
           return f"抱歉，发生了一个错误：{str(e)}"

    def _check_rules(self, results: dict) -> str:
        warnings = []
        for condition, message in self.rules:
            if eval(condition, results):
                warnings.append(message)
        return "\n".join(warnings) if warnings else "无警告或建议。"

# 确保 EnhancedNLPProcessor 类文件中正确导入和配置了 logging 模块

class BasicAIInteractionWindow:
    def __init__(self, parent, catia_operator, current_parameters):
        self.parent = parent
        self.catia_operator = catia_operator
        self.current_parameters = current_parameters

        config_path = os.path.join(os.path.dirname(__file__), 'settings.ini')
        self.nlp_processor = EnhancedNLPProcessor(config_path)

        self.window = tk.Toplevel(parent)
        self.window.title("基础AI交互")
        self.window.geometry("800x600")
        self.window.minsize(800, 600)

        style = ttk.Style(self.window)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TFrame", background="#f0f0f0")

        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(
            main_frame,
            text="基础AI交互",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        self.chat_frame = ttk.Frame(main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.chat_frame, command=self.chat_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.config(yscrollcommand=scrollbar.set)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        self.input_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        send_button = ttk.Button(
            input_frame,
            text="发送",
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT, padx=10)

        self.input_entry.bind("<Return>", lambda event: self.send_message())

        self.add_message("系统", "欢迎来到基础AI交互界面。请输入您的问题或指令。")

    def add_message(self, sender, message):
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def send_message(self):
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        self.input_entry.delete(0, tk.END)
        self.add_message("用户", user_input)

        try:
            response = self.nlp_processor.process_user_input(user_input)
            self.add_message("AI", response)
        except Exception as e:
            self.add_message("AI", f"抱歉，发生了一个错误：{str(e)}")


class AIInteractionWindow:
    def __init__(self, parent, catia_operator, current_parameters):
        self.parent = parent
        self.catia_operator = catia_operator
        self.current_parameters = current_parameters
        self.waiting_for_download_input = False  # 添加状态标记

        # 动态获取配置文件路径
        config_path = os.path.join(current_dir, "..", "config", "settings.ini")
        # 初始化 NLP 处理器
        self.nlp_processor = NLPProcessor(config_path, catia_operator=self.catia_operator, current_parameters=self.current_parameters)
        # 创建新窗口
        self.window = tk.Toplevel(parent)
        self.window.title("AI交互界面")
        self.window.geometry("800x600")
        self.window.minsize(800, 600)

        # 设置样式
        style = ttk.Style(self.window)
        style.configure("TLabel", font=("Arial", 14))
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TFrame", background="#f0f0f0")

        # 创建主框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # 标题
        ttk.Label(
            main_frame,
            text="AI交互界面",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # 聊天区域
        self.chat_frame = ttk.Frame(main_frame)
        self.chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # 聊天内容
        self.chat_text = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 聊天滚动条
        scrollbar = ttk.Scrollbar(self.chat_frame, command=self.chat_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.chat_text.config(yscrollcommand=scrollbar.set)

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=10)

        # 输入框
        self.input_entry = ttk.Entry(input_frame, font=("Arial", 12))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

        # 发送按钮
        send_button = ttk.Button(
            input_frame,
            text="发送",
            command=self.send_message
        )
        send_button.pack(side=tk.RIGHT, padx=10)

        # 绑定回车键发送消息
        self.input_entry.bind("<Return>", lambda event: self.send_message())

        # 添加欢迎信息
        self.add_message("系统", "欢迎使用AI交互界面，请输入您的指令。")

    def add_message(self, sender, message):
        # 添加消息到聊天窗口
        self.chat_text.config(state=tk.NORMAL)
        self.chat_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_text.see(tk.END)
        self.chat_text.config(state=tk.DISABLED)

    def update_model_parameters(self, layers, rows, trays_per_row):
        try:
            # 检查层数是否超过30层
            if layers > 30:
                raise ValueError("层数不能超过30层")

            # 检查层数是否为偶数
            if layers % 2 != 0:
                raise ValueError("层数必须是偶数")

            # 计算新尺寸
            length, width, height = FormKnowledgeDesign.calculate_dimensions(
                None, rows, trays_per_row, layers
            )

            # 更新CATIA模型
            if self.catia_operator is None:
                self.catia_operator = CATIAOperator()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
            self.catia_operator.open_document(file_path)
            updated_dimensions = self.catia_operator.set_dimensions(length=length, width=width, height=height)

            # 更新当前参数和尺寸
            self.current_parameters = {
                'layers': layers,
                'rows': rows,
                'trays_per_row': trays_per_row
            }
            self.current_dimensions = {
                'length': length,
                'width': width,
                'height': height
            }

            # 输出成功信息和更新后的参数
            self.add_message("AI",
                             f"模型参数已更新并在CATIA中展示。更新后的参数如下：\n长: {updated_dimensions['length']}mm\n宽: {updated_dimensions['width']}mm\n高: {updated_dimensions['height']}mm")

            # 设置等待下载确认的状态，并询问用户
            self.waiting_for_download_input = True
            self.add_message("AI", "是否下载模型（格式为STP）？请输入“是”或“否”：")

        except Exception as e:
            self.add_message("AI", f"✗ 发生错误: {str(e)}")

    def send_message(self):
        # 获取用户输入
        user_input = self.input_entry.get().strip()
        if not user_input:
            return

        # 清空输入框
        self.input_entry.delete(0, tk.END)

        # 添加用户消息
        self.add_message("用户", user_input)

        # 处理AI回复
        try:
            if self.waiting_for_download_input:
                # 如果正在等待下载确认
                if user_input.lower() == "是":
                    # 用户选择下载模型
                    self.download_model()
                    self.waiting_for_download_input = False
                elif user_input.lower() == "否":
                    # 用户取消下载
                    self.add_message("AI", "已取消下载模型。")
                    self.waiting_for_download_input = False
                else:
                    # 用户输入无效
                    self.add_message("AI", "无效输入，请输入“是”或“否”：")
                return

            # 解析命令
            command = self.nlp_processor.parse_command(user_input)

            # 执行操作
            if 'operation' in command:
                operation = command['operation']
                parameters = command.get('parameters', {})

                if operation == "OpenCATIA":
                    if self.catia_operator is None:
                        self.catia_operator = CATIAOperator()
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
                    self.catia_operator.open_document(file_path)
                    self.add_message("AI", "CATIA已打开")

                elif operation == "PartDesign.SetDimensions":
                    # 获取新参数
                    new_layers = parameters.get('layers', self.current_parameters['layers'])
                    new_rows = parameters.get('rows', self.current_parameters['rows'])
                    new_trays_per_row = parameters.get('trays_per_row', self.current_parameters['trays_per_row'])

                    # 更新模型参数
                    self.update_model_parameters(new_layers, new_rows, new_trays_per_row)

                elif operation == "PartDesign.UpdateModel":
                    # 更新并展示模型
                    current_layers = self.current_parameters['layers']
                    current_rows = self.current_parameters['rows']
                    current_trays_per_row = self.current_parameters['trays_per_row']
                    self.update_model_parameters(current_layers, current_rows, current_trays_per_row)

                elif operation == "CloseCATIA":
                    if self.catia_operator and self.catia_operator.catia:
                        self.catia_operator.catia.Quit()
                        self.catia_operator = None
                        self.add_message("AI", "CATIA已关闭")
                    else:
                        self.add_message("AI", "CATIA未打开")

                else:
                    # 处理不支持的操作
                    self.add_message("AI", f"抱歉，我不支持该操作: {operation}")
            else:
                # 处理一般聊天请求
                ai_response = command.get('message', "这是一个一般聊天。")
                self.add_message("AI", ai_response)

        except Exception as e:
            # 捕获所有异常并显示错误信息
            self.add_message("AI", f"抱歉，发生错误: {str(e)}")

    def download_model(self):
        try:
            if self.catia_operator is None:
                self.add_message("AI", "CATIA未打开，无法下载模型。")
                return

            # 定义保存路径
            save_path = "AMEKB"

            # 执行导出操作
            self.catia_operator.export_to_stp(save_path)

            # 提示用户下载完成
            self.add_message("AI", f"模型已成功导出为STP格式，保存路径：{save_path}")

        except Exception as e:
            self.add_message("AI", f"✗ 下载模型时发生错误: {str(e)}")

class NLPProcessor:
    _SYSTEM_PROMPT = """您是一个专业的CATIA自动化助手，您主要处理与CATIA建模和设计相关的指令。
    对于非CATIA相关的闲聊或其他话题，您也可以进行简单回复。

    请将有效的CATIA指令转换为以下JSON格式：
    {
      "operation": "模块.命令",
      "parameters": {
        "参数1": 值,
        ...
      }
    }

    示例指令："创建一个半径为20、高度为50的圆柱体"
    示例输出：{
      "operation": "PartDesign.Pad",
      "parameters": {
        "sketch_plane": "XY",
        "radius": 20,
        "height": 50
      }
    }

    示例指令："在XY平面上创建一个宽为30、长为40、深度为10的矩形凹槽"
    示例输出：{
      "operation": "PartDesign.Pocket",
      "parameters": {
        "sketch_plane": "XY",
        "width": 30,
        "length": 40,
        "depth": 10
      }
    }

    示例指令："调整框架长为8600mm、宽为4200mm、高为4100mm"
    示例输出：{
      "operation": "PartDesign.SetDimensions",
      "parameters": {
        "length": 8600,
        "width": 4200,
        "height": 4100
      }
    }

    示例指令："打开CATIA"
    示例输出：{
      "operation": "OpenCATIA",
      "parameters": {}
    }

    示例指令："更新当前模型的参数和尺寸：层数：12、行数：15、每行托盘数：10"
    示例输出：{
      "operation": "PartDesign.SetDimensions",
      "parameters": {
        "layers": 12,
        "rows": 15,
        "trays_per_row": 10
      }
    }

    示例指令："更新并展示模型"
    示例输出：{
      "operation": "PartDesign.UpdateModel",
      "parameters": {}
    }
    """

    def __init__(self, config_path=None, catia_operator=None, current_parameters=None):
        self.config = ConfigParser()
        if config_path is None:
            config_path = os.path.join(current_dir, "..", "config", "settings.ini")
        self.config.read(config_path)
        self._setup_api()

        # 初始化 CATIA 操作器和当前参数
        self.catia_operator = catia_operator
        self.current_parameters = current_parameters if current_parameters is not None else {'layers': 0, 'rows': 0, 'trays_per_row': 0}

    def _setup_api(self):
        self.api_url = self.config.get('API', 'deepseek_url')
        self.api_key = self.config.get('API', 'api_key')
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def update_model_parameters(self, layers, rows, trays_per_row):
        try:
            # 检查层数是否超过30层
            if layers > 30:
                raise ValueError("层数不能超过30层")

            # 检查层数是否为偶数
            if layers % 2 != 0:
                raise ValueError("层数必须是偶数")

            # 计算新尺寸
            length, width, height = self.calculate_dimensions(rows, trays_per_row, layers)

            # 更新 CATIA 模型
            if self.catia_operator is None:
                self.catia_operator = CATIAOperator()
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
            self.catia_operator.open_document(file_path)
            self.catia_operator.set_dimensions(length=length, width=width, height=height)

            # 更新当前参数和尺寸
            self.current_parameters = {
                'layers': layers,
                'rows': rows,
                'trays_per_row': trays_per_row
            }

            return f"模型参数已更新。更新后的参数如下：\n长: {length}mm\n宽: {width}mm\n高: {height}mm"
        except Exception as e:
            return f"发生错误: {str(e)}"

    def calculate_dimensions(self, rows, trays_per_row, layers):
        # 根据用户输入计算尺寸
        height = 187 + layers * 497.946 - 153
        length = 2317.5 + rows * 410
        width = 418 + trays_per_row * 623.7
        return length, width, height
    def parse_command(self, user_input: str) -> dict:
        """将自然语言转换为CATIA命令或处理聊天请求"""
        try:
            payload = {
                "model": "Qwen/Qwen2.5-7B-Instruct",
                "messages": [
                    {"role": "system", "content": self._SYSTEM_PROMPT},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.2
            }

            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=500
            )
            response.raise_for_status()

            return self._validate_output(response.json())
        except requests.RequestException as e:
            logging.error(f"API请求失败: {str(e)}")
            raise Exception("自然语言处理服务不可用") from e

    def _validate_output(self, response: dict) -> dict:
        """验证并清理API输出"""
        raw_data = response['choices'][0]['message']['content']

        try:
            # 尝试解析为JSON
            data = json.loads(raw_data)
            if not all(key in data for key in ('operation', 'parameters')):
                raise Exception("无效的命令结构")

            # 验证操作是否为有效的CATIA模块
            valid_operations = {
                'PartDesign.Pad',
                'PartDesign.Pocket',
                'PartDesign.SetDimensions',
                'PartDesign.UpdateModel',
                'OpenCATIA'
            }
            if data['operation'] not in valid_operations:
                raise Exception("不支持的CATIA操作")

            return data
        except json.JSONDecodeError:
            # 如果返回的不是JSON格式，则视为一般聊天
            logging.info("检测到非JSON返回内容，视为一般聊天")
            return {
                "response": "一般聊天",
                "message": raw_data
            }
        except Exception as e:
            logging.error(f"命令解析失败: {str(e)}")
            # 如果解析失败，直接返回原始内容作为一般聊天
            return {
                "response": "一般聊天",
                "message": raw_data
            }

    def process_user_input(self, user_input: str) -> str:
        try:
            result = self.parse_command(user_input)
            if result.get('response') == '一般聊天':
                return result.get('message', "这是一个一般聊天。")
            else:
                operation = result['operation']
                parameters = result['parameters']

                if operation == "OpenCATIA":
                    if self.catia_operator is None:
                        self.catia_operator = CATIAOperator()
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")
                    self.catia_operator.open_document(file_path)
                    return "CATIA已打开"

                elif operation == "PartDesign.SetDimensions":
                    new_layers = parameters.get('layers', self.current_parameters['layers'])
                    new_rows = parameters.get('rows', self.current_parameters['rows'])
                    new_trays_per_row = parameters.get('trays_per_row', self.current_parameters['trays_per_row'])
                    response = self.update_model_parameters(new_layers, new_rows, new_trays_per_row)
                    return response

                elif operation == "PartDesign.UpdateModel":
                    current_layers = self.current_parameters['layers']
                    current_rows = self.current_parameters['rows']
                    current_trays_per_row = self.current_parameters['trays_per_row']
                    response = self.update_model_parameters(current_layers, current_rows, current_trays_per_row)
                    return response

                elif operation == "CloseCATIA":
                    if self.catia_operator and self.catia_operator.catia:
                        self.catia_operator.catia.Quit()
                        self.catia_operator = None
                        return "CATIA已关闭"
                    else:
                        return "CATIA未打开"
                else:
                    return f"抱歉，我不支持该操作: {operation}"
        except Exception as e:
            logging.error(f"处理用户输入时发生错误: {str(e)}")
            return f"抱歉，发生了一个错误：{str(e)}"


if __name__ == "__main__":
    root = tk.Tk()
    app = FormKnowledgeDesign(root)
    root.mainloop()