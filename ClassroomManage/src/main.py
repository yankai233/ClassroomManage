from AdminWindow import *
from StudentWindow import *
from TeacherWindow import *


class LoginWindow:
    def __init__(self, window_size='500x500'):
        # 数据库连接
        self.root_user = Connect(
            user='root',
            host='localhost',
            password='123456',
            database='crdb'
        )
        self.cursor = self.root_user.cursor()

        self.window_size = window_size
        # 创建一个窗口
        self.login_window = tk.Tk()
        self.login_window.title('login')
        self.login_window.geometry(window_size)
        # var
        self.combobox_var = tk.StringVar()
        self.login_user_var = tk.StringVar()
        self.login_password = tk.StringVar()

        # 窗口组件
        # 身份
        tk.Label(self.login_window, text='用户身份:', width=20, height=2).place(x=50, y=100)
        combobox = ttk.Combobox(self.login_window, textvariable=self.combobox_var,
                                   values=['admin', 'student', 'teacher'], state='readonly')
        combobox.current(0)
        combobox.place(x=200, y=110)

        # 账号,密码
        tk.Label(self.login_window, text='账号:', width=20, height=2).place(x=50, y=150)
        tk.Label(self.login_window, text='密码:', width=20, height=2).place(x=50, y=200)
        tk.Entry(self.login_window, textvariable=self.login_user_var, width=23).place(x=200, y=160)
        tk.Entry(self.login_window, textvariable=self.login_password, width=23).place(x=200, y=210)

        # 按钮
        tk.Button(self.login_window, text='确定', width=30, height=2, bg='yellow',
                  command=self.login_command).place(x=170, y=280)
        tk.Button(self.login_window, text='取消', width=30, height=2, bg='yellow',
                  command=self.cancel_login_window).place(x=170, y=340)

        self.login_window.mainloop()

    def login_command(self):
        """登录事件"""
        user_type = self.combobox_var.get()
        username = self.login_user_var.get()
        password = self.login_password.get()
        # 检查是否输入有误
        if len(username) * len(user_type) * len(password) == 0:
            messagebox.showerror(message='输入错误，请重新输入')
            return
        # admin
        if user_type == 'admin':
            try:
                self.cursor.execute('select * from admin where username=%s and password=%s;', (username, password))
                sql_res = self.cursor.fetchall()
                # 检查账号和密码
                if len(sql_res) == 0:
                    messagebox.showerror(message='账号密码输入错误，请重新输入')
                    return
                # 进入管理员界面
                admin_window = AdminWindow(self.login_window, username, password)
            except Exception as e:
                messagebox.showerror(title='(login_command admin)', message=e)
                return
        # student
        elif user_type == 'student':
            try:
                self.cursor.execute('select * from student where username=%s and password=%s;', (username, password))
                sql_res = self.cursor.fetchall()
                if len(sql_res) == 0:
                    messagebox.showerror(message='账号密码错误，请重新输入')
                    return
                studentWindow = StudentWindow(self.login_window, username, password, self.window_size)
                return
            except Exception as e:
                messagebox.showerror(title='(login_command student)', message=e)
                return
        # Teacher
        elif user_type == 'teacher':
            try:
                self.cursor.execute('select * from teacher where username=%s and password=%s;', (username, password))
                sql_res = self.cursor.fetchall()
                if len(sql_res) == 0:
                    messagebox.showerror(message='账号密码错误，重新输入')
                    return
                teacherWindow = TeacherWindow(self.login_window, username, password, self.window_size)
                return
            except Exception as e:
                messagebox.showerror(title='(login_command teacher)', message=e)
                return
        else:
            messagebox.showerror(title='用户身份错误', message='用户身份错误，重新输入')
            return

    def cancel_login_window(self):
        """取消按钮"""
        flag = messagebox.askyesno(message='是否取消')
        if flag:
            self.login_window.destroy()
            return


if __name__ == '__main__':
    LoginWindow()
