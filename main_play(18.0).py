import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3

def create_database():
    conn = sqlite3.connect('logpasswd.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_superuser INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

window_width = 1024
window_height = 720

class App:
    def __init__(self, master):
        self.master = master
        self.loaded_dbs = []  # Список загруженных баз данных
        self.db_frames = []  # Список для хранения фреймов и их связанных баз данных
        self.is_superuser = False

        master.title("Авторизация")
        master.configure(bg='gray')
        self.bg_color = 'gray'
        self.fg_color = 'black'

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.label_username = tk.Label(master, text="Имя пользователя", bg=self.bg_color, fg=self.fg_color)
        self.label_username.place(relwidth=0.1, relheight=0.045, relx=0.5, rely=0.3, anchor='center')

        self.entry_username = tk.Entry(master, width=45)
        self.entry_username.place(relwidth=0.25, relheight=0.04, relx=0.5, rely=0.35, anchor='center')

        self.label_password = tk.Label(master, text="Пароль", bg=self.bg_color, fg=self.fg_color)
        self.label_password.place(relwidth=0.1, relheight=0.045, relx=0.5, rely=0.4, anchor='center')

        self.entry_password = tk.Entry(master, show='*', width=45)
        self.entry_password.place(relwidth=0.25, relheight=0.04, relx=0.5, rely=0.45, anchor='center')

        self.show_password_button = tk.Button(master, text="Показать пароль", command=self.toggle_password, bg='lightgray', fg=self.fg_color)
        self.show_password_button.place(relwidth=0.25, relheight=0.04, relx=0.5, rely=0.5, anchor='center')

        self.button_login = tk.Button(master, text="Войти", command=self.login, bg='lightgray', fg=self.fg_color)
        self.button_login.place(relwidth=0.12, relheight=0.04, relx=0.435, rely=0.55, anchor='center')

        self.button_superuser_login = tk.Button(master, text="Вход от суперпользователя", command=self.superuser_login, bg='lightgray', fg=self.fg_color)
        self.button_superuser_login.place(relwidth=0.25, relheight=0.04, relx=0.5, rely=0.6, anchor='center')

        self.button_register = tk.Button(master, text="Регистрация", command=self.register, bg='lightgray', fg=self.fg_color)
        self.button_register.place(relwidth=0.12, relheight=0.04, relx=0.565, rely=0.55, anchor='center')

        self.db_frame = None

    def toggle_password(self):
        if self.entry_password.cget('show') == '*':
            self.entry_password.config(show='')
            self.show_password_button.config(text="Скрыть пароль")
        else:
            self.entry_password.config(show='*')
            self.show_password_button.config(text="Показать пароль")

    def check_fields(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        return username, password

    def superuser_login(self):
        if self.entry_username.get() == "Sudo" and self.entry_password.get() == "Rs12345*":
            self.is_superuser = True
            messagebox.showinfo("Успешная авторизация!", "Добро пожаловать, суперпользователь!")
            self.open_database_interface()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль суперпользователя.")

    def login(self):
        username, password = self.check_fields()

        if not username or not password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            conn = sqlite3.connect('logpasswd.db')
            cursor = conn.cursor()
            cursor.execute("SELECT password, is_superuser FROM users WHERE username=?", (username,))
            result = cursor.fetchone()
            conn.close()

            if result and password == result[0]:
                self.is_superuser = bool(result[1])
                messagebox.showinfo("Успешная авторизация", "Добро пожаловать!")
                self.open_database_interface()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль. Попробуйте еще раз")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")

    def register(self):
        username, password = self.check_fields()

        if not username or not password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            conn = sqlite3.connect('logpasswd.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=?", (username,))
            if cursor.fetchone():
                messagebox.showerror("Ошибка Регистрации", "Пользователь с таким логином уже существует.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Успешная регистрация", "Поздравляем! Вы зарегистрировались")
                self.open_database_interface()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")

    def open_database_interface(self):
        if self.db_frame:
            self.db_frame.destroy()

        self.db_frame = tk.Frame(self.master, bg=self.bg_color)
        self.db_frame.pack(expand=True, fill=tk.BOTH)

        welcome_label = tk.Label(self.db_frame, text="Добро пожаловать!", bg=self.bg_color, fg=self.fg_color, font=("Arial", 16))
        welcome_label.pack(side=tk.TOP, pady=10)

        # Кнопка для загрузки базы данных
        self.button_load_db = tk.Button(self.db_frame, text="Загрузить базу данных", command=self.load_database, bg='lightgray', fg=self.fg_color)
        self.button_load_db.pack(pady=10)


        if self.is_superuser:
            self.edit_table_button = tk.Button(self.db_frame, text="Редактировать таблицы", command=self.edit_table)
            self.edit_table_button.pack(pady=10)

            self.create_superuser_button = tk.Button(self.db_frame, text="Создать суперпользователя", command=self.create_superuser)
            self.create_superuser_button.pack(pady=10)

    def load_database(self):
        db_path = filedialog.askopenfilename(filetypes=[("Database files", "*.db")])
        if db_path:
            if db_path in [db[0] for db in self.loaded_dbs]:  # Проверка на повторную загрузку
                messagebox.showerror("Ошибка", "Эта база данных уже загружена.")
                return
            
            self.loaded_dbs.append((db_path, tk.Frame(self.db_frame, bg=self.bg_color)))
            messagebox.showinfo("Успех", f"База данных загружена: {db_path}")

            # Здесь добавляем новый Frame для базы данных
            self.create_database_frame(db_path)

    def create_database_frame(self, db_path):
        # Создаем отдельный фрейм для каждой базы данных
        database_frame = tk.Frame(self.db_frame, bg=self.bg_color)
        database_frame.pack(side=tk.LEFT, pady=5)

        # Создаем новый Listbox
        table_list = tk.Listbox(database_frame, width=35)
        table_list.pack(side=tk.TOP, pady=5)

        show_selected_button = tk.Button(database_frame, text="Показать содержимое таблицы",
                                        command=lambda: self.show_selected_table(table_list, db_path))
        show_selected_button.pack(side=tk.BOTTOM, pady=5)

        # Заполняем Listbox названиями таблиц
        self.populate_table_list(table_list, db_path)

    def populate_table_list(self, table_list, db_path):  
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()

            # Очищаем Listbox перед добавлением новых элементов
            table_list.delete(0, tk.END)  # Очищаем все элементы в Listbox

            for table in tables:
                table_list.insert(tk.END, table[0])  # Добавление таблиц в новый Listbox

        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")


    def show_selected_table(self, table_list, db_path):
        selected_table = table_list.get(tk.ACTIVE)  # Теперь берем из переданного Listbox
        if selected_table:
            self.open_table_data(selected_table, db_path)
        else:
            messagebox.showwarning("Предупреждение", "Выберите таблицу для отображения.")

    def open_table_data(self, table_name, db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            query = f"SELECT * FROM {table_name}"  # table_name <-- Имя таблицы передается сюда
            cursor.execute(query)
            records = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            conn.close()

            if records:
                self.show_table_window(table_name, records, columns)
            else:
                messagebox.showinfo("Информация", f"Таблица {table_name} пуста.")

        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")

    def show_table_window(self, table_name, records, columns):
        db_window = tk.Toplevel(self.master)
        db_window.geometry(f"{window_width}x{window_height}")
        db_window.title(f"Содержимое таблицы: {table_name}")

        frame = tk.Frame(db_window)
        frame.pack(expand=True, fill=tk.BOTH)

        tree = ttk.Treeview(frame, columns=columns, show='headings', height=20)
        tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        for column in columns:
            tree.heading(column, text=column)
            tree.column(column, anchor="center", width=100)

        for record in records:
            tree.insert('', tk.END, values=record)

        vertical_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.configure(yscrollcommand=vertical_scrollbar.set)

        horizontal_scrollbar = ttk.Scrollbar(db_window, orient="horizontal", command=tree.xview)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        tree.configure(xscrollcommand=horizontal_scrollbar.set)
    
    def edit_table(self, table_list):
        selected_table = table_list.get(tk.ACTIVE)
        if selected_table:
            self.open_edit_window(selected_table)
    
    def open_edit_window(self, table_name):
        edit_window = tk.Toplevel(self.master)
        edit_window.title(f"Редактировать таблицу {table_name}")
        edit_window.geometry(f"{window_width}x{window_height}")

        # Простая форма ввода для новой записи
        self.label_new_record = tk.Label(edit_window, text="Новая строка в таблицу (записывайте данные через запятую):", bg=self.bg_color, fg=self.fg_color)
        self.label_new_record.pack(pady=10)

        self.entry_new_record = tk.Entry(edit_window, width=50)
        self.entry_new_record.pack(pady=10)

        self.button_add_record = tk.Button(edit_window, text="Добавить запись", command=lambda: self.add_record(table_name))
        self.button_add_record.pack(pady=10)

    def create_superuser(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if not username or not password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        try:
            conn = sqlite3.connect('logpasswd.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, is_superuser) VALUES (?, ?, 1)", (username, password))  # Пароль без хэширования
            conn.commit()
            messagebox.showinfo("Успешное создание", "Суперпользователь создан.")
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")

    def add_record(self, table_name):
        new_record = self.entry_new_record.get().split(',')
        if not new_record:
            messagebox.showerror("Ошибка", "Введите данные для новой записи.")
            return
        
        try:
            conn = sqlite3.connect(self.current_db)
            cursor = conn.cursor()
            placeholders = ','.join(['?' for _ in new_record])  # Создаем плейсхолдеры
            cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", new_record)
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", "Запись добавлена успешно!")
        except sqlite3.Error as e:
            messagebox.showerror("Ошибка", f"Ошибка базы данных: {e}")

if __name__ == "__main__":
    create_database()
    root = tk.Tk()
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(True, True)
    app = App(root)
    root.mainloop()
