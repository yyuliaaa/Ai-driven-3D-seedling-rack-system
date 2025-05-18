import importlib
import logging
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import subprocess
from loguru import logger
from catia_integration.catia_operator_0_很久之前 import CATIAOperator

class KnowledgeBasedDesignForm(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)  # 传递父窗口
        self.root = root
        self.title("用户界面")
        self.geometry("800x600")  # 修改初始大小

        # 创建图片显示区域
        self.create_picture_frame()

        # 创建单选按钮区域
        self.create_radio_frame()

        # 创建按钮
        self.create_buttons()

        # 初始化CATIA操作符
        self.catia_operator = None

    def create_picture_frame(self):
        self.picture_frame = tk.LabelFrame(self, text="图片展示", width=400, height=400, font=("Arial", 14, "bold"))
        self.picture_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        self.picture_frame.pack_propagate(False)

        # 加载并显示图片
        self.load_and_display_image()

    from tkinter import messagebox

    def get_resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # Fallback to __file__ if not in frozen mode
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    def load_and_display_image(self):
        try:
            # 获取资源文件路径
            self.image_path = self.get_resource_path("AMEKB/img/育秧架.jpg")

            # 加载并显示图片
            self.image = Image.open(self.image_path)
            self.image.thumbnail((400, 400))  # 修改图片大小
            self.photo = ImageTk.PhotoImage(self.image)
            self.picture_label = tk.Label(self.picture_frame, image=self.photo, font=("Arial", 14))
            self.picture_label.pack(expand=True)
        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片：{e}")

    def create_radio_frame(self):
        self.radio_frame = tk.LabelFrame(self, text="育秧总成", width=200, height=400, font=("Arial", 14, "bold"))
        self.radio_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=False)
        self.radio_frame.pack_propagate(False)

        # 创建单选按钮变量
        self.selected_type = tk.StringVar(value="卧式育秧架")

        # 创建单选按钮
        tk.Radiobutton(self.radio_frame, text="卧式育秧架", variable=self.selected_type, value="卧式育秧架", font=("Arial", 14)).pack(anchor=tk.W)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.radio_frame)
        self.button_frame.pack(pady=100, fill=tk.X)

        self.create_button("规则推荐", self.run_rule_recommend, 20, ("Arial", 14))
        self.create_button("实例推荐", self.run_shi_li_cha_xun, 20, ("Arial", 14))
        self.create_button("上下文知识推荐", self.run_context_knowledge_recommend, 20, ("Arial", 14))
        self.create_button("基于知识的设计", self.run_basic_ai_interaction, 20, ("Arial", 14))
        self.create_button("调用模型", self.open_catia, 20, ("Arial", 14))

    def create_button(self, text, command, width, font):
        button = tk.Button(self.button_frame, text=text, command=command, width=width, font=font)
        button.pack(pady=5, padx=10, fill=tk.X)

    def run_context_knowledge_recommend(self):
        self.run_script("form_上下文知识推荐", "FormDeviceKnowledge")

    def run_shi_li_cha_xun(self):
        self.run_script("form_实例推荐", "FormShiLiChaXun")

    def run_rule_recommend(self):
        self.run_script("form_规则推荐", "RiceTransplanterFrameApp")

    def run_basic_ai_interaction(self):
        self.run_script("catia_ai_ok", "BasicAIInteractionWindow")

    # def run_script(self, script_name, class_name=None):
    #     try:
    #         if class_name:
    #             subprocess.run(['python', f'{script_name}.py', class_name], check=True)
    #         else:
    #             subprocess.run(['python', f'{script_name}.py'], check=True)
    #     except subprocess.CalledProcessError as e:
    #         messagebox.showerror("错误", f"运行脚本时发生错误: {e}")

    import logging

    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    import os
    import importlib.util
    import sys
    from tkinter import messagebox
    import logging

    def run_script(self, script_name, class_name=None):
        try:
            # 获取当前脚本的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))

            # 构建完整的脚本路径
            script_path = os.path.join(current_dir, f"{script_name}.py")

            # 检查脚本是否存在
            if not os.path.exists(script_path):
                logging.error(f"脚本文件不存在: {script_path}")
                messagebox.showerror("错误", f"脚本文件不存在: {script_path}")
                return

            logging.info(f"Running script: {script_path}")

            # 动态导入脚本
            spec = importlib.util.spec_from_file_location("module.name", script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 运行脚本中的类或函数
            if class_name:
                # 假设类名和文件名相同
                class_ = getattr(module, class_name)
                obj = class_()
                # 假设类中有一个 run 方法
                obj.run()
            else:
                # 假设脚本中有一个 main 函数
                if hasattr(module, 'main'):
                    module.main()
                else:
                    logging.error("脚本中没有找到 main 函数")
                    messagebox.showerror("错误", "脚本中没有找到 main 函数")

        except Exception as e:
            logging.error(f"运行脚本时发生错误: {e}")
            messagebox.showerror("错误", f"运行脚本时发生错误: {e}")

    def open_catia(self):
        try:
            if self.catia_operator is None:
                # from catia_integration.catia_operator_0_很久之前 import CATIAOperator
                self.catia_operator = CATIAOperator()

            # 获取当前脚本的绝对路径
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # 构建相对路径
            file_path = os.path.join(current_dir, "..", "..", "new_py_catia", "canshuhuamoxing.CATPart")

            if not os.path.exists(file_path):
                messagebox.showerror("错误", f"文件不存在: {file_path}")
                return

            self.catia_operator.open_document(file_path)
        except Exception as e:
            logger.error(f"打开文件时发生错误: {str(e)}")
            messagebox.showerror("错误", f"打开文件时发生错误: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KnowledgeBasedDesignForm(root)
    root.withdraw()  # 隐藏根窗口
    app.mainloop()