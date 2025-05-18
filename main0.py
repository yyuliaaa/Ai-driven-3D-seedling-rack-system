import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
import os

# 确保所有模块都在同一目录下
from AMEKB.forms.form_知识库 import FormDeviceFormula
from AMEKB.forms.form_用户界面 import KnowledgeBasedDesignForm


class MainFrame:
    def __init__(self, master=None):
        self.root = master
        self.root.title("农业机械装备知识库系统")
        self.WIDTH = 800
        self.HEIGHT = 600

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # 将窗口居中显示
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        x = (self.ws / 2) - (self.WIDTH / 2)
        y = (self.hs / 2) - (self.HEIGHT / 2)
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}+{int(x)}+{int(y)}")
        self.root.resizable(False, False)

        # 创建Canvas
        self.canvas = tk.Canvas(self.root, width=self.WIDTH, height=self.HEIGHT)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        current_dir = os.path.dirname(__file__)

        # 加载背景图片
        try:
            background_image_path = os.path.join(current_dir, 'AMEKB', 'aa.jpg')
            background_image = Image.open(background_image_path)
            background_image = background_image.resize((self.WIDTH, self.HEIGHT), Image.Resampling.LANCZOS)
            self.background_photo = ImageTk.PhotoImage(background_image)
            self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
        except Exception as e:
            print(f"加载背景图片失败: {e}")

        # 欢迎信息
        self.welcome_label = self.canvas.create_text(
            self.WIDTH // 2, 100,
            text="欢迎使用农业机械装备知识库系统",
            font=("Arial", 24, "bold"),
            fill="blue"
        )

        # 按钮框架
        self.button_frame = ttk.Frame(self.canvas)
        self.canvas.create_window(
            self.WIDTH // 2, 350,
            window=self.button_frame,
            anchor=tk.CENTER
        )

        # 创建按钮
        self.create_button("知识库", self.open_knowledge_base)
        self.create_button("用户界面", self.open_user_interface)
        self.create_button("系统设置", self.system_settings)

        # 设置样式
        style = ttk.Style()
        style.configure(
            "Custom.TButton",
            font=("Arial", 16, "bold"),
            padding=20,
            background="#4a7abc",
            foreground="black",
            borderwidth=0,
            relief="flat",
            focusthickness=5,
            focuscolor="#4a7abc"
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#345a96"), ("pressed", "#2a4a7a")],
            foreground=[("active", "white"), ("pressed", "white")]
        )

    def create_button(self, text, command):
        btn = ttk.Button(
            self.button_frame,
            text=text,
            command=command,
            width=20,
            style="Custom.TButton"
        )
        btn.pack(pady=15, padx=10, fill=tk.X)

    def open_knowledge_base(self):
        knowledge_base_window = tk.Toplevel(self.root)
        knowledge_base_window.title("知识库")
        knowledge_base_window.geometry("1300x680")  # 调整窗口大小
        FormDeviceFormula(knowledge_base_window)

    def open_user_interface(self):
        KnowledgeBasedDesignForm(self.root)  # 直接实例化 KnowledgeBasedDesignForm

    def system_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("系统设置")
        settings_window.geometry("300x200")

        user_management_button = ttk.Button(
            settings_window,
            text="人员管理",
            command=self.user_management,
            style="Custom.TButton"
        )
        user_management_button.pack(pady=10, padx=20, fill=tk.X)

        exit_button = ttk.Button(
            settings_window,
            text="退出系统",
            command=self.root.quit,
            style="Custom.TButton"
        )
        exit_button.pack(pady=10, padx=20, fill=tk.X)

    def user_management(self):
        user_window = tk.Toplevel(self.root)
        user_window.title("人员管理")
        user_window.geometry("300x200")

        user_management_button = ttk.Button(
            user_window,
            text="用户管理",
            command=self.open_user_management,
            style="Custom.TButton"
        )
        user_management_button.pack(pady=10, padx=20, fill=tk.X)

        admin_info_button = ttk.Button(
            user_window,
            text="管理员信息",
            command=self.open_admin_info,
            style="Custom.TButton"
        )
        admin_info_button.pack(pady=10, padx=20, fill=tk.X)

    def open_user_management(self):
        user_window = tk.Toplevel(self.root)
        user_window.title("用户管理")
        user_window.geometry("600x400")

        columns = ("用户名", "角色")
        user_table = ttk.Treeview(user_window, columns=columns, show="headings")
        user_table.heading("用户名", text="用户名")
        user_table.heading("角色", text="角色")
        user_table.pack(fill=tk.BOTH, expand=True)

        user_table.insert("", tk.END, values=("user1", "普通用户"))
        user_table.insert("", tk.END, values=("admin", "管理员"))

        add_button = ttk.Button(user_window, text="添加用户", command=lambda: self.add_user(user_table))
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        delete_button = ttk.Button(user_window, text="删除用户", command=lambda: self.delete_user(user_table))
        delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def open_admin_info(self):
        admin_window = tk.Toplevel(self.root)
        admin_window.title("管理员信息")
        admin_window.geometry("600x400")

        columns = ("用户名", "角色", "联系方式")
        admin_table = ttk.Treeview(admin_window, columns=columns, show="headings")
        admin_table.heading("用户名", text="用户名")
        admin_table.heading("角色", text="角色")
        admin_table.heading("联系方式", text="联系方式")
        admin_table.pack(fill=tk.BOTH, expand=True)

        admin_table.insert("", tk.END, values=("admin", "管理员", "admin@example.com"))

        add_button = ttk.Button(admin_window, text="添加管理员", command=lambda: self.add_admin(admin_table))
        add_button.pack(side=tk.LEFT, padx=10, pady=10)

        delete_button = ttk.Button(admin_window, text="删除管理员", command=lambda: self.delete_admin(admin_table))
        delete_button.pack(side=tk.RIGHT, padx=10, pady=10)

    def add_user(self, table):
        username = simpledialog.askstring("添加用户", "请输入用户名")
        role = simpledialog.askstring("添加用户", "请输入角色")
        if username and role:
            table.insert("", tk.END, values=(username, role))

    def delete_user(self, table):
        selected_item = table.selection()
        if selected_item:
            table.delete(selected_item)

    def add_admin(self, table):
        username = simpledialog.askstring("添加管理员", "请输入用户名")
        role = simpledialog.askstring("添加管理员", "请输入角色")
        contact = simpledialog.askstring("添加管理员", "请输入联系方式")
        if username and role and contact:
            table.insert("", tk.END, values=(username, role, contact))

    def delete_admin(self, table):
        selected_item = table.selection()
        if selected_item:
            table.delete(selected_item)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainFrame(root)
    root.mainloop()