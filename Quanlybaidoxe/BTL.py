import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import sqlite3
import json
import os


class LoginWindow:
    def __init__(self, root):
        self.root = root

        self.root.title("Đăng Nhập")
        self.root.geometry("500x400")
        self.root.eval('tk::PlaceWindow . center')  # Center the window

        # Define colors
        self.main_bg_color = "#F0F0F0"
        self.button_color = "#4CAF50"
        self.text_color = "#333333"
        self.entry_bg_color = "#E0E0E0"
        self.frame_color = "#FFFFFF"

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_me_var = tk.BooleanVar()

        self.conn = sqlite3.connect('users.db')
        self.create_user_table()

        self.create_login_ui()
        self.load_remembered_credentials()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        cursor.close()

    def create_login_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load and display background image
        self.bg_image = Image.open("img_5.png")  # Thay đường dẫn tới ảnh của bạn
        self.bg_image = self.bg_image.resize((2000, 900), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Stretch to cover the entire window

        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme

        style.configure("TLabel", foreground=self.text_color, font=("Helvetica", 12, "bold"),
                        background=self.main_bg_color)
        style.configure("TEntry", foreground=self.text_color, font=("Helvetica", 12),
                        fieldbackground=self.entry_bg_color, background=self.frame_color, borderwidth=1, relief="solid")
        style.configure("TButton", foreground=self.main_bg_color, font=("Helvetica", 12, "bold"),
                        background=self.button_color, padding=8)
        style.map("TButton", background=[('active', '#45a049')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.configure("TCheckbutton", foreground=self.text_color, font=("Helvetica", 12),
                        background=self.main_bg_color)
        style.configure("Login.TFrame", background=self.frame_color, borderwidth=2, relief="solid")

        login_frame = ttk.Frame(self.root, padding=20, style="Login.TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

        ttk.Label(login_frame, text="Tên Đăng nhập:", style="TLabel").grid(column=0, row=0, padx=10, pady=10,
                                                                           sticky='e')
        ttk.Entry(login_frame, textvariable=self.username_var, style="TEntry").grid(column=1, row=0, padx=10, pady=10,
                                                                                    sticky='ew')

        ttk.Label(login_frame, text="Mật khẩu:", style="TLabel").grid(column=0, row=1, padx=10, pady=10, sticky='e')
        ttk.Entry(login_frame, textvariable=self.password_var, show='*', style="TEntry").grid(column=1, row=1, padx=10,
                                                                                              pady=10, sticky='ew')

        ttk.Checkbutton(login_frame, text="Ghi nhớ mật khẩu", variable=self.remember_me_var, style="TCheckbutton").grid(
            column=0, row=2, columnspan=2, padx=10, pady=10, sticky='w')

        button_frame = ttk.Frame(login_frame, style="Login.TFrame")
        button_frame.grid(column=0, row=3, columnspan=2, pady=10, sticky='ew')
        ttk.Button(button_frame, text="Đăng Nhập", command=self.login, style="TButton").pack(side=tk.LEFT, expand=True,
                                                                                             padx=5)
        ttk.Button(button_frame, text="Đăng Ký", command=self.show_register_page, style="TButton").pack(side=tk.LEFT,
                                                                                                        expand=True,
                                                                                                        padx=5)

        login_frame.grid_columnconfigure(1, weight=1)
        login_frame.grid_rowconfigure(3, weight=1)

    def show_register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Load and display background image
        self.bg_image = Image.open("img_5.png")  # Replace with your actual image path
        self.bg_image = self.bg_image.resize((2000, 900), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Stretch to cover the entire window

        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme

        style.configure("TLabel", foreground=self.text_color, font=("Helvetica", 12, "bold"),
                        background=self.main_bg_color)
        style.configure("TEntry", foreground=self.text_color, font=("Helvetica", 12),
                        fieldbackground=self.entry_bg_color, background=self.frame_color, borderwidth=1, relief="solid")
        style.configure("TButton", foreground=self.main_bg_color, font=("Helvetica", 12, "bold"),
                        background=self.button_color, padding=8)
        style.map("TButton", background=[('active', '#45a049')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.configure("TCheckbutton", foreground=self.text_color, font=("Helvetica", 12),
                        background=self.main_bg_color)
        style.configure("Register.TFrame", background=self.frame_color, borderwidth=2, relief="solid")

        register_frame = ttk.Frame(self.root, padding=20, style="Register.TFrame")
        register_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

        ttk.Label(register_frame, text="Tên Đăng nhập:", style="TLabel").grid(column=0, row=0, padx=10, pady=10,
                                                                              sticky='e')
        ttk.Entry(register_frame, textvariable=self.username_var, style="TEntry").grid(column=1, row=0, padx=10,
                                                                                       pady=10, sticky='ew')

        ttk.Label(register_frame, text="Mật khẩu:", style="TLabel").grid(column=0, row=1, padx=10, pady=10, sticky='e')
        ttk.Entry(register_frame, textvariable=self.password_var, show='*', style="TEntry").grid(column=1, row=1,
                                                                                                 padx=10, pady=10,
                                                                                                 sticky='ew')

        ttk.Label(register_frame, text="Nhập lại mật khẩu:", style="TLabel").grid(column=0, row=2, padx=10, pady=10,
                                                                                  sticky='e')
        self.repassword_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.repassword_var, show='*', style="TEntry").grid(column=1, row=2,
                                                                                                   padx=10, pady=10,
                                                                                                   sticky='ew')

        ttk.Button(register_frame, text="Đăng Ký", command=self.register, style="TButton").grid(column=0, row=3,
                                                                                                columnspan=2, pady=20,
                                                                                                sticky='ew')
        ttk.Button(register_frame, text="Quay lại", command=self.create_login_ui, style="TButton").grid(column=0, row=4,
                                                                                                        columnspan=2,
                                                                                                        pady=20,
                                                                                                        sticky='ew')

        register_frame.grid_columnconfigure(1, weight=1)

    def register(self):
        username = self.username_var.get()
        password = self.password_var.get()
        repassword = self.repassword_var.get()

        if not username or not password or not repassword:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        if password != repassword:
            messagebox.showerror("Lỗi", "Mật khẩu nhập lại không khớp.")
            return

        if len(password) > 10:
            messagebox.showerror("Lỗi", "Mật khẩu không được quá 10 ký tự.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Thông báo", "Đăng ký thành công!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
        finally:
            cursor.close()
            self.create_login_ui()

    def load_remembered_credentials(self):
        if os.path.exists('credentials.json'):
            with open('credentials.json', 'r') as file:
                credentials = json.load(file)
                self.username_var.set(credentials.get('username', ''))
                self.password_var.set(credentials.get('password', ''))
                self.remember_me_var.set(True)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            if self.remember_me_var.get():
                with open('credentials.json', 'w') as file:
                    json.dump({'username': username, 'password': password}, file)
            else:
                if os.path.exists('credentials.json'):
                    os.remove('credentials.json')

            self.open_management_window()
        else:
            messagebox.showerror("Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")

    def open_management_window(self):
        self.root.destroy()
        root = tk.Tk()
        root.state('zoomed')  # Fullscreen mode

        # Kiểm tra tên đăng nhập
        if self.username_var.get() == "admin":
            # Nếu tên đăng nhập là "admin", mở trang quản lý tài khoản
            app = AccountManagementApp(root, self)
        else:
            # Nếu không phải "admin", mở trang quản lý vé
            app = ParkingManagementApp(root, self)

        root.mainloop()


class AccountManagementApp:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window

        self.root.title("Quản Lý Tài Khoản")
        self.root.geometry("800x600")

        self.main_bg_color = "#F0F0F0"
        self.button_color = "#4CAF50"
        self.text_color = "#333333"
        self.entry_bg_color = "#E0E0E0"
        self.frame_color = "#FFFFFF"

        self.conn = sqlite3.connect('users.db')
        self.create_user_table()

        self.create_ui()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()
        cursor.close()

    def create_ui(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("TLabel", foreground=self.text_color, font=("Helvetica", 12, "bold"),
                        background=self.main_bg_color)
        style.configure("TEntry", foreground=self.text_color, font=("Helvetica", 12),
                        fieldbackground=self.entry_bg_color, background=self.frame_color, borderwidth=1, relief="solid")
        style.configure("TButton", foreground=self.main_bg_color, font=("Helvetica", 12, "bold"),
                        background=self.button_color, padding=8)
        style.map("TButton", background=[('active', '#45a049')], relief=[('pressed', 'sunken'), ('!pressed', 'raised')])
        style.configure("TTreeview", font=("Helvetica", 12), background=self.frame_color,
                        fieldbackground=self.frame_color)
        style.configure("TFrame", background=self.main_bg_color)
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background=self.main_bg_color)
        style.configure("TSeparator", background=self.main_bg_color)

        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(expand=True, fill='both')

        # Search frame
        search_frame = ttk.Frame(main_frame, padding=10)
        search_frame.pack(fill='x', pady=(0, 10))

        ttk.Label(search_frame, text="Tìm kiếm:", style="TLabel").pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry = ttk.Entry(search_frame, style="TEntry")
        self.search_entry.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10))
        ttk.Button(search_frame, text="Tìm", command=self.search_user, style="TButton").pack(side=tk.LEFT)

        self.user_tree = ttk.Treeview(main_frame, columns=("ID", "Username", "Password"), show="headings",
                                      selectmode="browse")
        self.user_tree.heading("ID", text="ID")
        self.user_tree.heading("Username", text="Username")
        self.user_tree.heading("Password", text="Password")
        self.user_tree.column("ID", width=50, anchor='center')
        self.user_tree.column("Username", width=200, anchor='center')
        self.user_tree.column("Password", width=200, anchor='center')
        self.user_tree.tag_configure('oddrow', background=self.entry_bg_color)
        self.user_tree.tag_configure('evenrow', background=self.frame_color)
        self.user_tree.pack(expand=True, fill='both', pady=(20, 10))

        # Add striped row tags to the treeview
        def add_striped_rows():
            for i, item in enumerate(self.user_tree.get_children()):
                if i % 2 == 0:
                    self.user_tree.item(item, tags=('evenrow',))
                else:
                    self.user_tree.item(item, tags=('oddrow',))

        form_frame = ttk.Frame(main_frame, padding=10)
        form_frame.pack(fill='x', pady=10)

        form_inner_frame = ttk.Frame(form_frame)
        form_inner_frame.pack(anchor='center')

        ttk.Label(form_inner_frame, text="Username:", style="TLabel").grid(column=0, row=0, padx=10, pady=10,
                                                                           sticky='e')
        self.username_entry = ttk.Entry(form_inner_frame, style="TEntry")
        self.username_entry.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

        ttk.Label(form_inner_frame, text="Password:", style="TLabel").grid(column=0, row=1, padx=10, pady=10,
                                                                           sticky='e')
        self.password_entry = ttk.Entry(form_inner_frame, style="TEntry")
        self.password_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

        button_frame = ttk.Frame(main_frame, padding=10)
        button_frame.pack(fill='x', pady=10)

        button_inner_frame = ttk.Frame(button_frame)
        button_inner_frame.pack(anchor='center')

        ttk.Button(button_inner_frame, text="Thêm", command=self.add_user, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_inner_frame, text="Sửa", command=self.edit_user, style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_inner_frame, text="Xóa", command=self.delete_user, style="TButton").pack(side=tk.LEFT, padx=5)

        logout_frame = ttk.Frame(main_frame, padding=10)
        logout_frame.pack(fill='x', pady=(10, 20))
        logout_button = ttk.Button(logout_frame, text="Đăng Xuất", command=self.logout, style="TButton")
        logout_button.pack(anchor='center')

        self.load_users()
        add_striped_rows()  # Call the function to add striped rows

    def search_user(self):
        search_text = self.search_entry.get()
        if not search_text:
            self.load_users()  # If search text is empty, load all users
            return

        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username LIKE ?", ('%' + search_text + '%',))
        users = cursor.fetchall()
        cursor.close()

        for user in users:
            self.user_tree.insert("", "end", values=user)

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            messagebox.showinfo("Thông báo", "Thêm người dùng thành công!")
            self.load_users()
        except sqlite3.IntegrityError:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
        finally:
            cursor.close()

    def edit_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một người dùng để sửa.")
            return

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập và mật khẩu.")
            return

        user_id = self.user_tree.item(selected_item[0])['values'][0]

        cursor = self.conn.cursor()
        cursor.execute("UPDATE users SET username = ?, password = ? WHERE id = ?", (username, password, user_id))
        self.conn.commit()
        cursor.close()
        messagebox.showinfo("Thông báo", "Sửa người dùng thành công!")
        self.load_users()

    def delete_user(self):
        selected_item = self.user_tree.selection()
        if not selected_item:
            messagebox.showerror("Lỗi", "Vui lòng chọn một người dùng để xóa.")
            return

        user_id = self.user_tree.item(selected_item[0])['values'][0]

        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        cursor.close()
        messagebox.showinfo("Thông báo", "Xóa người dùng thành công!")
        self.load_users()

    def load_users(self):
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()

        for user in users:
            self.user_tree.insert("", "end", values=user)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginWindow(root)
        root.mainloop()


class ParkingManagementApp:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("Hệ Thống Quản Lý Bãi Đỗ Xe")
        self.root.geometry("800x600")

        self.conn = sqlite3.connect('parking_management.db')
        self.create_tables()

        self.style = ttk.Style()

        # Cấu hình style
        self.style.theme_use('clam')  # Chọn một theme hiện đại

        # Các màu sắc và phông chữ
        dark_yellow = "#FFD700"
        green = "#008000"
        light_blue = "#ADD8E6"
        light_grey = "#D3D3D3"
        white = "#FFFFFF"
        black = "#000000"

        # Load and display background image
        self.bg_image = Image.open("img_10.png")  # Thay đường dẫn tới ảnh của bạn
        self.bg_image = self.bg_image.resize((2000, 900), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)  # Stretch to cover the entire window

        # Cấu hình style cho các widget
        self.style.configure("TLabel", foreground=black, font=("Helvetica", 12, "bold"))
        self.style.configure("TEntry", foreground=black, font=("Helvetica", 12), fieldbackground=white,
                             background=white)
        self.style.configure("TButton", foreground=white, font=("Helvetica", 10, "bold"), background=green,
                             padding=(10, 8))
        self.style.map("TButton", background=[('active', dark_yellow)])
        self.style.configure("TCheckbutton", foreground=black, font=("Helvetica", 12), background=light_blue)
        self.style.configure("Treeview", font=("Helvetica", 12), background=light_grey, fieldbackground=white)
        self.style.map("Treeview", background=[('selected', dark_yellow)], foreground=[('selected', black)])
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground=black,
                             background='orange')
        self.style.configure("Blue.TFrame", background='')
        # Cấu hình màu cho tab được chọn
        self.style.configure("TNotebook.Tab", font=('Arial', 12), padding=(198, 2), background=light_blue)
        self.style.map("TNotebook.Tab", background=[('selected', 'pink')])

        # Tạo Notebook để chứa các tab
        self.notebook = ttk.Notebook(self.root, style='My.TNotebook')
        self.notebook.pack(pady=10, fill='both', expand=True)

        # Tạo các tab cho các phần khác nhau của ứng dụng
        self.parking_spots_tab = ttk.Frame(self.notebook, style='My.TFrame')
        self.vehicle_registration_tab = ttk.Frame(self.notebook, style='My.TFrame')
        self.ticket_management_tab = ttk.Frame(self.notebook, style='My.TFrame')
        self.revenue_tab = ttk.Frame(self.notebook, style='My.TFrame')

        # Tạo label để hiển thị hình ảnh nền
        self.background_label = tk.Label(self.root, image=self.bg_photo)
        self.background_label.place(relwidth=1, relheight=1)

        # Nút "Chọn ở đây"
        self.select_button = ttk.Button(self.root, text="Hệ thống quản lý Bãi đỗ xe", command=self.show_tabs_interface,
                                        style='TButton')
        self.select_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

        # Nút Đăng xuất
        ttk.Button(self.root, text="Đăng Xuất", command=self.logout, style='TButton').pack(side='bottom', pady=10)

        # Tạo nội dung cho tab 'Bãi đỗ xe'
        self.create_parking_spots_tab()

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        LoginWindow(root)

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parking_spots (
                id INTEGER PRIMARY KEY,
                spot_number TEXT UNIQUE,
                is_occupied BOOLEAN
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id INTEGER PRIMARY KEY,
                license_plate TEXT UNIQUE,
                owner_name TEXT,
                parking_spot_id INTEGER,
                FOREIGN KEY(parking_spot_id) REFERENCES parking_spots(id)
            )
        """)
        cursor.execute('''CREATE TABLE IF NOT EXISTS tickets (
                                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                vehicle_id TEXT NOT NULL,
                                                entry_time TEXT NOT NULL,
                                                exit_time TEXT NOT NULL,
                                                fee INTEGER NOT NULL,
                                                paid INTEGER DEFAULT 0
                                            )''')
        self.conn.commit()
        cursor.close()

    def show_tabs_interface(self):
        # Xóa nút "Chọn ở đây"
        self.select_button.place_forget()

        # Xóa hình ảnh nền
        self.background_label.destroy()

        # Thêm tab 'Bãi đỗ xe' vào Notebook
        self.notebook.add(self.parking_spots_tab, text='Bãi đỗ xe')
        self.notebook.add(self.vehicle_registration_tab, text='Đăng ký gửi xe')
        self.notebook.add(self.ticket_management_tab, text='Quản lý vé')
        # self.notebook.add(self.revenue_tab, text='Doanh thu')

        # Tạo nội dung cho từng tab mới
        self.create_vehicle_registration_tab()
        self.create_ticket_management_tab()
        self.create_revenue_tab()

    def create_parking_spots_tab(self):
        self.total_parking_spots = 200  # Số bãi xe mặc định

        # Configure the style for the light blue background
        style = ttk.Style()
        style.configure("Gray.TFrame", background="lightblue")  # Changed to light blue

        frame = ttk.Frame(self.parking_spots_tab, padding=20, style="Gray.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        self.parking_spot_var = tk.StringVar()
        self.is_occupied_var = tk.BooleanVar()

        ttk.Label(frame, text="Vị trí Đỗ xe:", style="TLabel").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        ttk.Entry(frame, textvariable=self.parking_spot_var, style="TEntry").grid(column=1, row=0, padx=10, pady=10,
                                                                                  sticky='ew')

        ttk.Label(frame, text="Đang sử dụng:", style="TLabel").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        ttk.Checkbutton(frame, variable=self.is_occupied_var, style="TCheckbutton").grid(column=1, row=1, padx=10,
                                                                                         pady=10, sticky='ew')

        button_frame = ttk.Frame(frame, style="Gray.TFrame")
        button_frame.grid(column=0, row=2, columnspan=2, pady=20, sticky='ew')
        ttk.Button(button_frame, text="Thêm Vị trí", command=self.add_parking_spot, style="TButton").pack(side=tk.LEFT,
                                                                                                          expand=True,
                                                                                                          padx=5)
        ttk.Button(button_frame, text="Sửa Vị trí", command=self.edit_parking_spot, style="TButton").pack(side=tk.LEFT,
                                                                                                          expand=True,
                                                                                                          padx=5)
        ttk.Button(button_frame, text="Xóa Vị trí", command=self.delete_parking_spot, style="TButton").pack(
            side=tk.LEFT, expand=True, padx=5)

        search_frame = ttk.Frame(frame, style="Gray.TFrame")
        search_frame.grid(column=0, row=3, columnspan=2, pady=10, sticky='ew')

        search_frame.grid_columnconfigure(1, weight=1)
        search_frame.grid_columnconfigure(2, weight=0)

        columns = ("ID", "Vị trí", "Đang sử dụng")
        self.parking_spots_treeview = ttk.Treeview(frame, columns=columns, show="headings", style="My.Treeview")
        for col in columns:
            self.parking_spots_treeview.heading(col, text=col)
        self.parking_spots_treeview.column("ID", width=50, anchor='center')
        self.parking_spots_treeview.column("Vị trí", width=100, anchor='center')
        self.parking_spots_treeview.column("Đang sử dụng", width=100, anchor='center')
        self.parking_spots_treeview.grid(column=0, row=4, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Thêm label để hiển thị số chỗ còn lại
        ttk.Label(frame, text="Số chỗ còn trống : ", style="TLabel").grid(column=0, row=5, padx=10, pady=10, sticky='w')
        self.available_spots_label = ttk.Label(frame, text="", style="TLabel")
        self.available_spots_label.grid(column=1, row=5, padx=10, pady=10, sticky='w')

        # Tính lại số chỗ còn trống và cập nhật label
        self.update_available_spots_count()

        frame.grid_rowconfigure(4, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.load_parking_spots()

        def update_available_spots_count(self):
            try:
                cursor = self.conn.cursor()

                cursor.execute("SELECT COUNT(*) FROM parking_spots")
                count_total = cursor.fetchone()[0]  # Tổng số lượng vị trí đỗ xe đã được thêm vào cơ sở dữ liệu

                cursor.close()

                # Tính lại số lượng xe còn trống dựa trên tổng số bãi xe và số lượng vị trí đã thêm
                available_spots = self.total_parking_spots - count_total
                if available_spots >= 0:
                    self.available_spots_label.config(text=str(available_spots))

            except sqlite3.Error as e:
                messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def add_parking_spot(self):
        spot_number = self.parking_spot_var.get()
        is_occupied = self.is_occupied_var.get()

        # Kiểm tra điều kiện vị trí đỗ xe từ 1 đến 200
        try:
            spot_number_int = int(spot_number)
            if spot_number_int < 1 or spot_number_int > 200:
                messagebox.showwarning("Lỗi nhập liệu", "Vị trí đỗ xe phải nằm trong khoảng từ 1 đến 200.")
                return
        except ValueError:
            messagebox.showwarning("Lỗi nhập liệu", "Vị trí đỗ xe phải là số nguyên.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO parking_spots (spot_number, is_occupied) VALUES (?, ?)",
                           (spot_number, is_occupied))
            self.conn.commit()
            cursor.close()
            self.load_parking_spots()  # Load spots in parking spots tab
            self.update_available_spots_count()  # Update available spots count

            # Load parking spots into combobox in vehicle registration tab
            self.load_parking_spots_into_combobox()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def edit_parking_spot(self):
        selected_item = self.parking_spots_treeview.selection()
        if not selected_item:
            return

        spot_id = self.parking_spots_treeview.item(selected_item, 'values')[0]
        spot_number = self.parking_spot_var.get()
        is_occupied = self.is_occupied_var.get()

        # Kiểm tra điều kiện vị trí đỗ xe từ 1 đến 200
        try:
            spot_number_int = int(spot_number)
            if spot_number_int < 1 or spot_number_int > 200:
                messagebox.showwarning("Lỗi nhập liệu", "Vị trí đỗ xe phải nằm trong khoảng từ 1 đến 200.")
                return
        except ValueError:
            messagebox.showwarning("Lỗi nhập liệu", "Vị trí đỗ xe phải là số nguyên.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE parking_spots SET spot_number = ?, is_occupied = ? WHERE id = ?",
                           (spot_number, is_occupied, spot_id))
            self.conn.commit()
            cursor.close()
            self.load_parking_spots()
            self.update_available_spots_count()  # Update available spots count

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def delete_parking_spot(self):
        selected_item = self.parking_spots_treeview.selection()
        if not selected_item:
            return

        spot_id = self.parking_spots_treeview.item(selected_item, 'values')[0]

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM parking_spots WHERE id = ?", (spot_id,))
            self.conn.commit()
            cursor.close()
            self.load_parking_spots()
            self.update_available_spots_count()  # Update available spots count

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def update_available_spots_count(self):
        try:
            cursor = self.conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM parking_spots")
            count_total = cursor.fetchone()[0]  # Tổng số lượng vị trí đỗ xe đã được thêm vào cơ sở dữ liệu

            cursor.close()

            # Tính lại số lượng xe còn trống dựa trên tổng số bãi xe và số lượng vị trí đã thêm
            available_spots = self.total_parking_spots - count_total
            if available_spots >= 0:
                self.available_spots_label.config(text=str(available_spots))

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def count_occupied_parking_spots(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM parking_spots WHERE is_occupied = 1")
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")
            return 0

    def load_parking_spots(self):
        self.parking_spots_treeview.delete(*self.parking_spots_treeview.get_children())

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, spot_number, is_occupied FROM parking_spots")

            for row in cursor.fetchall():
                self.parking_spots_treeview.insert("", "end", values=(row[0], row[1], "Có" if row[2] else "Không"))

            cursor.close()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải dữ liệu: {e}")

    def load_parking_spots_in_vehicle_tab(self, new_spot_id):
        # This method will be called to update parking spot options in vehicle registration tab
        pass

    def create_vehicle_registration_tab(self):
        # Configure the style for the light blue background
        style = ttk.Style()
        style.configure("LightBlue.TFrame", background="lightblue")  # Changed to light blue

        frame = ttk.Frame(self.vehicle_registration_tab, padding=20, style="LightBlue.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        self.license_plate_var = tk.StringVar()
        self.owner_name_var = tk.StringVar()
        self.parking_spot_id_var = tk.StringVar()
        self.search_var = tk.StringVar()

        ttk.Label(frame, text="Biển số xe:", style="TLabel").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        ttk.Entry(frame, textvariable=self.license_plate_var, style="TEntry").grid(column=1, row=0, padx=10, pady=10,
                                                                                   sticky='ew')

        ttk.Label(frame, text="Tên chủ xe:", style="TLabel").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        ttk.Entry(frame, textvariable=self.owner_name_var, style="TEntry").grid(column=1, row=1, padx=10, pady=10,
                                                                                sticky='ew')

        ttk.Label(frame, text="Vị trí đỗ xe:", style="TLabel").grid(column=0, row=2, padx=10, pady=10, sticky='w')
        self.parking_spot_combobox = ttk.Combobox(frame, textvariable=self.parking_spot_id_var, state="readonly",
                                                  style="TCombobox")
        self.parking_spot_combobox.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

        button_frame = ttk.Frame(frame, style="LightBlue.TFrame")
        button_frame.grid(column=0, row=3, columnspan=2, pady=20, sticky='ew')
        ttk.Button(button_frame, text="Đăng Ký", command=self.add_vehicle, style="TButton").pack(side=tk.LEFT,
                                                                                                 expand=True, padx=5)
        ttk.Button(button_frame, text="Sửa Thông Tin", command=self.edit_vehicle, style="TButton").pack(side=tk.LEFT,
                                                                                                        expand=True,
                                                                                                        padx=5)
        ttk.Button(button_frame, text="Xóa Xe", command=self.delete_vehicle, style="TButton").pack(side=tk.LEFT,
                                                                                                   expand=True, padx=5)

        columns = ("ID", "Biển số", "Chủ xe", "Vị trí đỗ xe")
        self.vehicles_treeview = ttk.Treeview(frame, columns=columns, show="headings", style="My.Treeview")
        for col in columns:
            self.vehicles_treeview.heading(col, text=col)
        self.vehicles_treeview.column("ID", width=50, anchor='center')
        self.vehicles_treeview.column("Biển số", width=100, anchor='center')
        self.vehicles_treeview.column("Chủ xe", width=150, anchor='center')
        self.vehicles_treeview.column("Vị trí đỗ xe", width=100, anchor='center')
        self.vehicles_treeview.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky='nsew')

        frame.grid_rowconfigure(5, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.load_vehicles()

        # Load parking spots into the combobox
        self.load_parking_spots_into_combobox()

    def load_parking_spots_into_combobox(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id, spot_number FROM parking_spots WHERE is_occupied = 0")  # Only load unoccupied spots
            parking_spots = cursor.fetchall()
            cursor.close()

            self.parking_spot_combobox['values'] = [f"{spot[1]}" for spot in parking_spots]

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải danh sách vị trí đỗ xe: {e}")

    def add_vehicle(self):
        license_plate = self.license_plate_var.get()
        owner_name = self.owner_name_var.get()
        parking_spot_number = self.parking_spot_id_var.get()

        if not license_plate or not owner_name or not parking_spot_number:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            # Check if the selected parking spot is occupied
            cursor = self.conn.cursor()
            cursor.execute("SELECT is_occupied FROM parking_spots WHERE spot_number = ?", (parking_spot_number,))
            row = cursor.fetchone()
            if row and row[0] == 1:
                messagebox.showerror("Lỗi đăng ký xe", "Vị trí đỗ xe đã được sử dụng. Vui lòng chọn vị trí khác.")
                cursor.close()
                return

            # Insert the vehicle into the database
            cursor.execute("INSERT INTO vehicles (license_plate, owner_name, parking_spot_id) VALUES (?, ?, ?)",
                           (license_plate, owner_name, parking_spot_number))
            self.conn.commit()
            cursor.close()
            self.load_vehicles()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def is_parking_spot_occupied(self, spot_number):
                try:
                    cursor = self.conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM parking_spots WHERE spot_number = ? AND is_occupied = 1",
                                   (spot_number,))
                    count = cursor.fetchone()[0]
                    cursor.close()
                    return count > 0
                except sqlite3.Error as e:
                    messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")
                    return True  # Trả về True nếu xảy ra lỗi để đảm bảo không cho phép đăng ký

    def is_parking_spot_taken(self, parking_spot_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE parking_spot_id = ?", (parking_spot_id,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")
            return False

    def is_license_plate_duplicate(self, license_plate):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM vehicles WHERE license_plate = ?", (license_plate,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")
            return False

    def edit_vehicle(self):
        selected_item = self.vehicles_treeview.focus()
        if not selected_item:
            return

        vehicle_id = self.vehicles_treeview.item(selected_item, 'values')[0]
        license_plate = self.license_plate_var.get()
        owner_name = self.owner_name_var.get()
        parking_spot_number = self.parking_spot_id_var.get()

        if not license_plate or not owner_name or not parking_spot_number:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE vehicles SET license_plate = ?, owner_name = ?, parking_spot_id = ? WHERE id = ?",
                           (license_plate, owner_name, parking_spot_number, vehicle_id))
            self.conn.commit()
            cursor.close()
            self.load_vehicles()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def delete_vehicle(self):
        selected_item = self.vehicles_treeview.focus()
        if not selected_item:
            return

        vehicle_id = self.vehicles_treeview.item(selected_item, 'values')[0]

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM vehicles WHERE id = ?", (vehicle_id,))
            self.conn.commit()
            cursor.close()
            self.load_vehicles()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def load_vehicles(self):
        for i in self.vehicles_treeview.get_children():
            self.vehicles_treeview.delete(i)

        cursor = self.conn.cursor()
        cursor.execute("SELECT id, license_plate, owner_name, parking_spot_id FROM vehicles")
        for row in cursor.fetchall():
            self.vehicles_treeview.insert("", "end", values=(row[0], row[1], row[2], row[3]))
        cursor.close()

    def search_vehicles(self):
        search_term = self.search_var.get().strip().lower()
        if not search_term:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập từ khóa tìm kiếm.")
            return

        for i in self.vehicles_treeview.get_children():
            self.vehicles_treeview.delete(i)

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id, license_plate, owner_name, parking_spot_id FROM vehicles WHERE lower(license_plate) LIKE ? OR lower(owner_name) LIKE ?",
                ('%' + search_term + '%', '%' + search_term + '%'))
            for row in cursor.fetchall():
                self.vehicles_treeview.insert("", "end", values=(row[0], row[1], row[2], row[3]))
            cursor.close()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tìm kiếm: {e}")

    def set_entry_time(self):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.entry_time_var.set(formatted_time)

    def set_exit_time(self):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        self.exit_time_var.set(formatted_time)

    def get_license_plates_from_vehicle_registration(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT license_plate FROM vehicles")
            license_plates = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return license_plates
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải danh sách biển số xe: {e}")
            return []
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")
            return []

    def calculate_fee(self):
        time_format = "%Y-%m-%d %H:%M:%S"

        entry_time_str = self.entry_time_var.get()
        exit_time_str = self.exit_time_var.get()

        try:
            entry_time = datetime.datetime.strptime(entry_time_str, time_format)
            exit_time = datetime.datetime.strptime(exit_time_str, time_format)
        except ValueError:
            return None

        delta = exit_time - entry_time
        hours = delta.total_seconds() / 3600

        if hours <= 1:
            fee = 3000
        else:
            # Tính phí theo quy tắc 3000 VNĐ cho 1 giờ đầu và 3000 VNĐ cho mỗi giờ tiếp theo
            fee = 3000 * (int(hours) + (1 if hours > int(hours) else 0))

        if hours > 24:
            fee += 20000
            messagebox.showwarning("Thông báo", "Bạn đã để quá 24 giờ. Bạn đã bị phạt thêm 20,000 VNĐ.")

        return round(fee)

    def update_fee(self, *args):
        try:
            fee = self.calculate_fee()
            self.fee_var.set(fee)
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))
            self.fee_var.set("")

    def create_ticket_management_tab(self):
        frame = ttk.Frame(self.ticket_management_tab, padding=20, style="Gray.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        self.vehicle_id_var = tk.StringVar()
        self.entry_time_var = tk.StringVar()
        self.exit_time_var = tk.StringVar()
        self.fee_var = tk.StringVar()
        self.search_var = tk.StringVar()

        ttk.Label(frame, text="Biển số xe:", style="TLabel").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        license_plates = self.get_license_plates_from_vehicle_registration()
        self.license_plate_combobox = ttk.Combobox(frame, values=license_plates, state="readonly")
        self.license_plate_combobox.grid(column=1, row=0, padx=10, pady=10, sticky='ew')

        ttk.Button(frame, text="Thời gian vào", command=self.set_entry_time, style="TButton").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        entry_time_entry = ttk.Entry(frame, textvariable=self.entry_time_var, style="TEntry")
        entry_time_entry.grid(column=1, row=1, padx=10, pady=10, sticky='ew')

        ttk.Button(frame, text="Thời gian ra", command=self.set_exit_time, style="TButton").grid(column=0, row=2, padx=10, pady=10, sticky='w')
        exit_time_entry = ttk.Entry(frame, textvariable=self.exit_time_var, style="TEntry")
        exit_time_entry.grid(column=1, row=2, padx=10, pady=10, sticky='ew')

        self.entry_time_var.trace_add("write", self.update_fee)
        self.exit_time_var.trace_add("write", self.update_fee)

        ttk.Label(frame, text="Phí:", style="TLabel").grid(column=0, row=3, padx=10, pady=10, sticky='w')
        ttk.Entry(frame, textvariable=self.fee_var, style="TEntry").grid(column=1, row=3, padx=10, pady=10, sticky='ew')

        button_frame = ttk.Frame(frame, style="Gray.TFrame")
        button_frame.grid(column=0, row=4, columnspan=2, pady=20, sticky='ew')
        ttk.Button(button_frame, text="Thêm Vé", command=self.add_ticket, style="TButton").pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Sửa Vé", command=self.edit_ticket, style="TButton").pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Xóa Vé", command=self.delete_ticket, style="TButton").pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(button_frame, text="Thanh toán", command=self.pay_ticket, style="TButton").pack(side=tk.LEFT, expand=True, padx=5)

        search_frame = ttk.Frame(frame, style="Gray.TFrame")
        search_frame.grid(column=0, row=5, columnspan=2, pady=10, sticky='ew')

        ttk.Label(search_frame, text="Tìm kiếm:", style="TLabel").grid(column=0, row=0, padx=5, pady=5, sticky='w')
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, style="TEntry")
        search_entry.grid(column=1, row=0, padx=5, pady=5, sticky='ew')

        search_button = ttk.Button(search_frame, text="Tìm kiếm", command=self.search_tickets, style="TButton")
        search_button.grid(column=2, row=0, padx=5, pady=5, sticky='ew')

        search_frame.grid_columnconfigure(1, weight=1)

        columns = ("ID", "Biển số xe", "Thời gian vào", "Thời gian ra", "Phí")
        self.tickets_treeview = ttk.Treeview(frame, columns=columns, show="headings", style="My.Treeview")
        for col in columns:
            self.tickets_treeview.heading(col, text=col)
        self.tickets_treeview.column("ID", width=50, anchor='center')
        self.tickets_treeview.column("Biển số xe", width=100, anchor='center')
        self.tickets_treeview.column("Thời gian vào", width=150, anchor='center')
        self.tickets_treeview.column("Thời gian ra", width=150, anchor='center')
        self.tickets_treeview.column("Phí", width=100, anchor='center')
        self.tickets_treeview.grid(column=0, row=6, columnspan=2, padx=10, pady=10, sticky='nsew')

        frame.grid_rowconfigure(6, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        self.load_tickets()

    def add_ticket(self):
        vehicle_id = self.license_plate_combobox.get()  # Lấy giá trị từ combobox biển số xe
        entry_time = self.entry_time_var.get()
        exit_time = self.exit_time_var.get()
        fee = self.fee_var.get()

        if not vehicle_id or not entry_time or not exit_time or not fee:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            # Thực hiện chèn dữ liệu vào CSDL
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO tickets (vehicle_id, entry_time, exit_time, fee) VALUES (?, ?, ?, ?)",
                           (vehicle_id, entry_time, exit_time, fee))
            self.conn.commit()
            cursor.close()
            self.load_tickets()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def edit_ticket(self):
        selected_item = self.tickets_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Thông báo", "Vui lòng chọn vé cần sửa.")
            return

        ticket_id = self.tickets_treeview.item(selected_item, 'values')[0]

        vehicle_id = self.license_plate_combobox.get()
        entry_time = self.entry_time_var.get()
        exit_time = self.exit_time_var.get()
        fee = self.fee_var.get()

        if not vehicle_id or not entry_time or not exit_time or not fee:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tickets SET vehicle_id = ?, entry_time = ?, exit_time = ?, fee = ? WHERE id = ?",
                           (vehicle_id, entry_time, exit_time, fee, ticket_id))
            self.conn.commit()
            cursor.close()
            self.load_tickets()
            messagebox.showinfo("Thông báo", "Đã cập nhật thông tin vé thành công.")
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def delete_ticket(self):
        selected_item = self.tickets_treeview.selection()
        if not selected_item:
            return

        ticket_id = self.tickets_treeview.item(selected_item, 'values')[0]

        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM tickets WHERE id = ?", (ticket_id,))
            self.conn.commit()
            cursor.close()
            self.load_tickets()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def load_tickets(self):
        self.tickets_treeview.delete(*self.tickets_treeview.get_children())

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, vehicle_id, entry_time, exit_time, fee FROM tickets")
            for row in cursor.fetchall():
                self.tickets_treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
            cursor.close()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải dữ liệu: {e}")

    def search_tickets(self):
        search_term = self.search_var.get().strip()
        self.tickets_treeview.delete(*self.tickets_treeview.get_children())

        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "SELECT id, vehicle_id, entry_time, exit_time, fee FROM tickets WHERE vehicle_id LIKE ? OR entry_time LIKE ? OR exit_time LIKE ? OR fee LIKE ?",
                ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
            for row in cursor.fetchall():
                self.tickets_treeview.insert("", "end", values=(row[0], row[1], row[2], row[3], row[4]))
            cursor.close()

        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tìm kiếm: {e}")

    def create_revenue_tab(self):
        # Configure the style for the light blue background
        style = ttk.Style()
        style.configure("Cyan.TFrame", background="lightblue")  # Changed to light blue

        self.revenue_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.revenue_tab, text='Doanh thu')

        frame = ttk.Frame(self.revenue_tab, padding=20, style="Cyan.TFrame")
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Doanh thu Tổng:").grid(column=0, row=0, padx=10, pady=10, sticky='w')
        self.total_revenue_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.total_revenue_var, state='readonly').grid(column=1, row=0, padx=10, pady=10,
                                                                                     sticky='ew')

        ttk.Label(frame, text="Tổng số vé đã thanh toán:").grid(column=0, row=1, padx=10, pady=10, sticky='w')
        self.total_paid_tickets_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.total_paid_tickets_var, state='readonly', font=('Arial', 12),
                  foreground='Black').grid(column=1, row=1, padx=10, pady=10, sticky='ew')

        ttk.Label(frame, text="Chi tiết Doanh thu:").grid(column=0, row=2, padx=10, pady=10, sticky='w')

        columns = ("ID", "Biển số xe", "Thời gian vào", "Thời gian ra", "Phí")
        self.revenue_treeview = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            self.revenue_treeview.heading(col, text=col)
        self.revenue_treeview.column("ID", width=50, anchor='center')
        self.revenue_treeview.column("Biển số xe", width=100, anchor='center')
        self.revenue_treeview.column("Thời gian vào", width=150, anchor='center')
        self.revenue_treeview.column("Thời gian ra", width=150, anchor='center')
        self.revenue_treeview.column("Phí", width=100, anchor='center')
        self.revenue_treeview.grid(column=0, row=3, columnspan=2, padx=10, pady=10, sticky='nsew')

        frame.grid_rowconfigure(3, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        # Thêm nút Chọn tất cả và Xuất PDF
        select_all_checkbox = ttk.Checkbutton(frame, text="Chọn tất cả", command=self.select_all_revenue_items)
        select_all_checkbox.grid(column=0, row=4, padx=10, pady=10, sticky='w')

        export_pdf_button = ttk.Button(frame, text="Xuất PDF", command=self.export_selected_revenue_pdf)
        export_pdf_button.grid(column=1, row=4, padx=10, pady=10, sticky='e')

        # Thêm nút Sửa và Xóa
        buttons_frame = ttk.Frame(frame, style="Cyan.TFrame")
        buttons_frame.grid(column=0, row=5, columnspan=2, padx=10, pady=10, sticky='ew')

        edit_button = ttk.Button(buttons_frame, text="Sửa", command=self.edit_revenue)
        edit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        delete_button = ttk.Button(buttons_frame, text="Xóa", command=self.delete_revenue)
        delete_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.load_revenue()

    def select_all_revenue_items(self):
        # Lặp qua tất cả các item trong Treeview và chọn chúng
        for item in self.revenue_treeview.get_children():
            self.revenue_treeview.selection_add(item)

    def export_selected_revenue_pdf(self):
        # Lấy dữ liệu từ Treeview
        selected_items = self.revenue_treeview.selection()
        if not selected_items:
            messagebox.showwarning("Lỗi", "Vui lòng chọn ít nhất một hóa đơn để xuất PDF.")
            return

        data = []
        for item in selected_items:
            values = self.revenue_treeview.item(item, 'values')
            data.append(values)

        # Kiểm tra xem có chọn tất cả hay không
        if len(selected_items) == len(self.revenue_treeview.get_children()):
            data = []
            for item in self.revenue_treeview.get_children():
                values = self.revenue_treeview.item(item, 'values')
                data.append(values)

        # Xuất PDF
        file_path = "doanh_thu.pdf"
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        c.drawString(250, height - 50, "Chi tiet Hoa Don")
        y = height - 100
        for item in data:
            id, vehicle_id, entry_time, exit_time, fee = item
            c.drawString(10, y, f"ID: {id}")
            c.drawString(50, y, f"Bien: {vehicle_id}")
            c.drawString(140, y, f"TG vào: {entry_time}")
            c.drawString(320, y, f"TG ra : {exit_time}")
            c.drawString(500, y, f"Phí: {fee} VND")
            y -= 20

        c.save()
        os.startfile(file_path)

    def edit_revenue(self):
        selected_item = self.revenue_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn mục cần sửa.")
            return

        revenue_id = self.revenue_treeview.item(selected_item, 'values')[0]
        vehicle_id = self.revenue_treeview.item(selected_item, 'values')[1]
        entry_time = self.revenue_treeview.item(selected_item, 'values')[2]
        exit_time = self.revenue_treeview.item(selected_item, 'values')[3]
        fee = self.revenue_treeview.item(selected_item, 'values')[4]

        # Hiển thị cửa sổ sửa thông tin doanh thu
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Sửa Doanh thu")

        tk.Label(edit_window, text="Biển số xe:").grid(column=0, row=0, padx=10, pady=10)
        vehicle_id_entry = ttk.Entry(edit_window)
        vehicle_id_entry.insert(0, vehicle_id)
        vehicle_id_entry.grid(column=1, row=0, padx=10, pady=10)

        tk.Label(edit_window, text="Thời gian vào:").grid(column=0, row=1, padx=10, pady=10)
        entry_time_entry = ttk.Entry(edit_window)
        entry_time_entry.insert(0, entry_time)
        entry_time_entry.grid(column=1, row=1, padx=10, pady=10)

        tk.Label(edit_window, text="Thời gian ra:").grid(column=0, row=2, padx=10, pady=10)
        exit_time_entry = ttk.Entry(edit_window)
        exit_time_entry.insert(0, exit_time)
        exit_time_entry.grid(column=1, row=2, padx=10, pady=10)

        tk.Label(edit_window, text="Phí:").grid(column=0, row=3, padx=10, pady=10)
        fee_entry = ttk.Entry(edit_window)
        fee_entry.insert(0, fee)
        fee_entry.grid(column=1, row=3, padx=10, pady=10)

        def update_revenue():
            new_vehicle_id = vehicle_id_entry.get()
            new_entry_time = entry_time_entry.get()
            new_exit_time = exit_time_entry.get()
            new_fee = fee_entry.get()

            if not new_vehicle_id or not new_entry_time or not new_exit_time or not new_fee:
                messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
                return

            try:
                cursor = self.conn.cursor()
                cursor.execute("UPDATE tickets SET vehicle_id=?, entry_time=?, exit_time=?, fee=? WHERE id=?",
                               (new_vehicle_id, new_entry_time, new_exit_time, new_fee, revenue_id))
                self.conn.commit()
                cursor.close()
                self.load_revenue()
                edit_window.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

        update_button = ttk.Button(edit_window, text="Cập nhật", command=update_revenue)
        update_button.grid(column=0, row=4, columnspan=2, padx=10, pady=10)

    def delete_revenue(self):
        selected_item = self.revenue_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn mục cần xóa.")
            return

        revenue_id = self.revenue_treeview.item(selected_item, 'values')[0]

        try:
            confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa mục doanh thu này?")
            if confirm:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM tickets WHERE id=?", (revenue_id,))
                self.conn.commit()
                cursor.close()
                self.load_revenue()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def add_ticket(self):
        vehicle_id = self.license_plate_combobox.get()
        entry_time = self.entry_time_var.get()
        exit_time = self.exit_time_var.get()
        fee = self.fee_var.get()

        if not vehicle_id or not entry_time or not exit_time or not fee:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO tickets (vehicle_id, entry_time, exit_time, fee) VALUES (?, ?, ?, ?)",
                           (vehicle_id, entry_time, exit_time, fee))
            self.conn.commit()
            cursor.close()
            self.load_tickets()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def edit_ticket(self):
        selected_item = self.tickets_treeview.selection()
        if not selected_item:
            return

        ticket_id = self.tickets_treeview.item(selected_item, 'values')[0]
        vehicle_id = self.license_plate_combobox.get()
        entry_time = self.entry_time_var.get()
        exit_time = self.exit_time_var.get()
        fee = self.fee_var.get()

        if not vehicle_id or not entry_time or not exit_time or not fee:
            messagebox.showwarning("Lỗi nhập liệu", "Vui lòng nhập đầy đủ thông tin.")
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tickets SET vehicle_id=?, entry_time=?, exit_time=?, fee=? WHERE id=?",
                           (vehicle_id, entry_time, exit_time, fee, ticket_id))
            self.conn.commit()
            cursor.close()
            self.load_tickets()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def delete_ticket(self):
        selected_item = self.tickets_treeview.selection()
        if not selected_item:
            return

        ticket_id = self.tickets_treeview.item(selected_item, 'values')[0]

        try:
            confirm = messagebox.askyesno("Xác nhận xóa", "Bạn có chắc chắn muốn xóa vé này?")
            if confirm:
                cursor = self.conn.cursor()
                cursor.execute("DELETE FROM tickets WHERE id=?", (ticket_id,))
                self.conn.commit()
                cursor.close()
                self.load_tickets()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi: {e}")

    def pay_ticket(self):
        selected_item = self.tickets_treeview.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn vé để thanh toán.")
            return

        ticket_id = self.tickets_treeview.item(selected_item, 'values')[0]
        vehicle_id = self.tickets_treeview.item(selected_item, 'values')[1]
        entry_time = self.tickets_treeview.item(selected_item, 'values')[2]
        exit_time = self.tickets_treeview.item(selected_item, 'values')[3]
        fee = self.tickets_treeview.item(selected_item, 'values')[4]

        try:
            cursor = self.conn.cursor()
            cursor.execute("UPDATE tickets SET paid = 1 WHERE id = ?", (ticket_id,))
            self.conn.commit()
            cursor.close()
            self.load_tickets()
            self.update_total_revenue()  # Cập nhật tổng doanh thu sau khi thanh toán
            self.load_revenue()  # Cập nhật lại chi tiết doanh thu

            # Hiển thị hóa đơn
            receipt = f"Hóa đơn\nID: {ticket_id}\nBiển số xe: {vehicle_id}\nThời gian vào: {entry_time}\nThời gian ra: {exit_time}\nPhí: {fee} VND"
            messagebox.showinfo("Hóa đơn", receipt)
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi thanh toán: {e}")

    def load_tickets(self):
        self.tickets_treeview.delete(*self.tickets_treeview.get_children())

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, vehicle_id, entry_time, exit_time, fee FROM tickets WHERE paid = 0")
            for row in cursor.fetchall():
                self.tickets_treeview.insert("", "end", values=row)
            cursor.close()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải dữ liệu: {e}")

    def load_revenue(self):
        self.revenue_treeview.delete(*self.revenue_treeview.get_children())

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT id, vehicle_id, entry_time, exit_time, fee FROM tickets WHERE paid = 1")
            total_revenue = 0
            total_paid_tickets = 0
            for row in cursor.fetchall():
                self.revenue_treeview.insert("", "end", values=row)
                total_revenue += row[4]
                total_paid_tickets += 1
            self.total_revenue_var.set(f"{total_revenue} VND")
            self.total_paid_tickets_var.set(f"{total_paid_tickets} vé")
            cursor.close()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải dữ liệu: {e}")

    def update_total_revenue(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SUM(fee) FROM tickets WHERE paid = 1")
            total_revenue = cursor.fetchone()[0]
            self.total_revenue_var.set(f"{total_revenue} VND")
            cursor.close()
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tính tổng doanh thu: {e}")

    def get_license_plates_from_vehicle_registration1(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT DISTINCT vehicle_id FROM tickets")
            plates = [row[0] for row in cursor.fetchall()]
            cursor.close()
            return plates
        except sqlite3.Error as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", f"Đã xảy ra lỗi khi tải dữ liệu: {e}")
            return []

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
