import tkinter as tk
from tkinter import ttk
from pymysql import Connect
from Course_SQL import *


class AdminTeacherManage(Course_SQL):
    """
    admin:老师管理
    """

    def __init__(self, parent_window, con, cusor, username, password, window_size='400x500'):
        super(AdminTeacherManage, self).__init__(parent_window, username, password, 'admin', '123456')
        self.parent_window = parent_window
        self.adminTeacherWindow = tk.Toplevel(self.parent_window)
        self.adminTeacherWindow.title('老师管理界面')
        self.adminTeacherWindow.geometry(window_size)
        self.con = con
        self.cusor = cusor
        # var
        self.add_Tno_var = tk.StringVar()
        self.add_Tname_var = tk.StringVar()
        self.add_username_var = tk.StringVar()
        self.add_password_var = tk.StringVar()

        self.drop_Tno_var = tk.StringVar()
        self.drop_listbox_var = tk.StringVar()
        self.drop_info_var = tk.StringVar()
        self.drop_info_var.trace(mode='w', callback=self.drop_info_var_callback)
        self.all_teacher_info = []

        self.select_teacher_info_var = tk.StringVar()

        self.update_teacher_type = tk.StringVar()
        self.update_teacher_info = tk.StringVar()
        # 组件
        tk.Button(self.adminTeacherWindow, text='添加', width=35, bg='yellow',
                  command=self.add_teacher_user_window).place(x=100, y=50)
        tk.Button(self.adminTeacherWindow, text='删除', width=35, bg='yellow',
                  command=self.drop_teacher_user_window).place(x=100, y=100)
        tk.Button(self.adminTeacherWindow, text='修改', width=35, bg='yellow',
                  command=self.update_teacher_user_window).place(x=100, y=150)
        tk.Button(self.adminTeacherWindow, text='查看', width=35, bg='yellow',
                  command=self.select_teacher_user_window).place(x=100, y=200)
        tk.Button(self.adminTeacherWindow, text='取消', width=35, bg='yellow',
                  command=lambda: self.window_exit(self.adminTeacherWindow)).place(x=100, y=250)

    def drop_info_var_callback(self, *args):
        """绑定模糊搜索框的事件"""
        info = self.drop_info_var.get()
        teacher_info = self.all_teacher_info
        new_info_lst = []
        # 模糊搜索
        for i in range(len(teacher_info)):
            if info in teacher_info[i]:
                new_info_lst.append(teacher_info[i])
        self.drop_listbox_var.set(new_info_lst)

    def var_init(self):
        """var初始化"""
        self.add_Tno_var.set('')
        self.add_Tname_var.set('')
        self.add_username_var.set('')
        self.add_password_var.set('')
        self.drop_Tno_var.set('')
        self.drop_listbox_var.set('')
        self.drop_info_var.set('')
        self.all_teacher_info = []
        self.select_teacher_info_var.set('')
        self.update_teacher_type.set('')
        self.update_teacher_info.set('')

    def add_teacher_user_window(self):
        """添加老师账号"""
        self.add_teacher_window = tk.Toplevel(self.adminTeacherWindow)
        self.add_teacher_window.title('添加老师账号')
        self.add_teacher_window.geometry('600x500')
        tk.Label(self.add_teacher_window, text='工号:', width=10).place(x=50, y=50)
        tk.Entry(self.add_teacher_window, textvariable=self.add_Tno_var, width=20).place(x=120, y=50)
        tk.Label(self.add_teacher_window, text='姓名:', width=10).place(x=300, y=50)
        tk.Entry(self.add_teacher_window, textvariable=self.add_Tname_var, width=20).place(x=370, y=50)

        tk.Label(self.add_teacher_window, text='账号:', width=10).place(x=50, y=100)
        tk.Entry(self.add_teacher_window, textvariable=self.add_username_var, width=20).place(x=120, y=100)

        tk.Label(self.add_teacher_window, text='密码:', width=10).place(x=300, y=100)
        tk.Entry(self.add_teacher_window, textvariable=self.add_password_var, width=20).place(x=370, y=100)

        tk.Button(self.add_teacher_window, text='添加', bg='yellow',
                  width=25, command=self.add_teacher_command).place(x=200, y=250)
        tk.Button(self.add_teacher_window, text='取消', bg='yellow',
                  width=25, command=lambda: self.window_exit(self.add_teacher_window)).place(x=200, y=300)

    def add_teacher_command(self):
        """添加老师"""
        # 读取信息
        Tno, Tname, username, password = self.add_Tno_var.get(), self.add_Tname_var.get(), self.add_username_var.get(), self.add_password_var.get()
        print(Tno, '\t', Tname, '\t', username, '\t', password)
        sql_res = self.sql_teacher_username(username, password)
        if sql_res == -1:  # 报错
            return
        if len(sql_res) != 0:  # 老师存在
            messagebox.showerror(title='添加老师错误(add_teacher_command)', message='账号已经存在')
            return
        sql_res = self.sql_insert_teacher_user(Tno, Tname, username, password)
        # 报错
        if sql_res == -1:
            return
        messagebox.showinfo(title='添加老师成功(add_teacher_command)', message='添加老师成功')
        self.var_init()

    def drop_teacher_user_window(self):
        """删除老师账号"""
        self.drop_teacher_window = tk.Toplevel(self.adminTeacherWindow)
        self.drop_teacher_window.title('删除老师账号')
        self.drop_teacher_window.geometry('500x600')
        tk.Label(self.drop_teacher_window, text='查询信息:', width=10).place(x=50, y=50)
        tk.Entry(self.drop_teacher_window, textvariable=self.drop_info_var, width=50).place(x=120, y=50)
        self.drop_listbox = tk.Listbox(self.drop_teacher_window, listvariable=self.drop_listbox_var, width=50,
                                       height=10)
        self.drop_listbox.place(x=120, y=100)
        self.listbox_var_init()
        # 模糊搜索框绑定点击事件
        self.drop_listbox.bind('<ButtonRelease-1>', self.hit_drop_listbox, add='+')
        tk.Label(self.drop_teacher_window, text='工号:', width=10).place(x=50, y=400)
        tk.Entry(self.drop_teacher_window, textvariable=self.drop_Tno_var, width=50).place(x=120, y=400)
        tk.Button(self.drop_teacher_window, text='删除老师', width=25, command=self.drop_teacher_command,
                  bg='yellow').place(x=200, y=450)
        tk.Button(self.drop_teacher_window, text='取消', width=25,
                  command=lambda: self.window_exit_functions_init(self.drop_teacher_window, self.listbox_var_init), bg='yellow').place(x=200, y=500)

    def window_exit_functions_init(self, window, *args):
        """
        init_functions()+window_exit()
        :param window:
        :param args: init_functions()
        :return: None
        """
        for func in args:
            func()
        self.window_exit(window)

    def listbox_var_init(self):
        """模糊搜索初始化"""
        # 获取所有老师信息
        sql_res = self.sql_teacher_all_info()
        if sql_res == -1:
            self.drop_listbox_var.set('')
        else:
            all_info = self.sql2str(sql_res)
            self.drop_listbox_var.set(all_info)
            self.all_teacher_info = all_info

    def hit_drop_listbox(self, event):
        """点击搜索框"""
        s: str = self.drop_listbox.get(self.drop_listbox.curselection())
        print(s)
        self.drop_info_var.set(s)
        self.drop_listbox_var.set('')
        # 获取字符串的Sno
        Tno = s.split(',')[0]
        self.drop_Tno_var.set(Tno)

    def drop_teacher_command(self):
        """删除老师"""
        Tno = self.drop_Tno_var.get()
        sql_res = self.sql_delete_teacher_Tno(Tno)
        if sql_res == 1:
            messagebox.showinfo(title='(hit_drop_listbox)', message='删除老师成功')
            self.var_init()
            self.listbox_var_init()
            return

    def update_teacher_user_window(self):
        """修改老师账号"""
        self.update_teacher_window = tk.Toplevel(self.adminTeacherWindow)
        self.update_teacher_window.title('删除老师账号')
        self.update_teacher_window.geometry('500x600')
        tk.Label(self.update_teacher_window, text='查询信息:', width=10).place(x=50, y=50)
        tk.Entry(self.update_teacher_window, textvariable=self.drop_info_var, width=50).place(x=120, y=50)
        self.drop_listbox = tk.Listbox(self.update_teacher_window, listvariable=self.drop_listbox_var, width=50,
                                       height=10)
        self.drop_listbox.place(x=120, y=100)
        self.listbox_var_init()
        # 模糊搜索框绑定点击事件
        self.drop_listbox.bind('<ButtonRelease-1>', self.hit_drop_listbox, add='+')
        tk.Label(self.update_teacher_window, text='学号:', width=10).place(x=50, y=300)
        tk.Entry(self.update_teacher_window, textvariable=self.drop_Tno_var, width=50).place(x=120, y=300)
        tk.Label(self.update_teacher_window, text='修改的属性:', width=10).place(x=50, y=350)
        self.update_combobox = ttk.Combobox(self.update_teacher_window, values=['Tname', 'password'],
                                            textvariable=self.update_teacher_type, width=10, state='readonly')
        self.update_combobox.place(x=130, y=350)
        tk.Label(self.update_teacher_window, text='修改的信息:', width=10).place(x=250, y=350)
        tk.Entry(self.update_teacher_window, textvariable=self.update_teacher_info, width=10).place(x=330, y=350)

        tk.Button(self.update_teacher_window, text='修改老师信息', width=25, command=self.update_teacher_command,
                  bg='yellow').place(x=200, y=450)
        tk.Button(self.update_teacher_window, text='取消', width=25,
                  command=lambda: self.window_exit_functions_init(self.update_teacher_window, self.listbox_var_init),
                  bg='yellow').place(x=200, y=500)

    def update_teacher_command(self):
        """更新老师信息"""
        Tno = self.drop_Tno_var.get()
        info_type = self.update_teacher_type.get()
        teacher_info = self.update_teacher_info.get()
        if len(Tno) * len(info_type) * len(teacher_info) == 0:
            messagebox.showerror(title='update_teacher_command', message='更新输入信息错误')
            return
        # 更新
        sql_res = self.sql_update_teacher_Sno(Tno, info_type, teacher_info)
        if sql_res == -1:
            self.update_teacher_info.set('')
            return
        messagebox.showinfo(title='update_teacher_command', message='更新成功')
        self.var_init()
        self.listbox_var_init()

    def select_teacher_user_window(self):
        """查看老师账号"""

        # 窗口
        self.select_window = tk.Toplevel(self.adminTeacherWindow)
        self.select_window.title('查看老师账号')
        self.select_window.geometry('500x600')
        # 组件
        self.select_text = tk.Text(self.select_window, width=50, height=20)
        self.select_text.place(x=75, y=50)
        self.select_insert()
        tk.Button(self.select_window, text='取消', bg='yellow', command=lambda: self.window_exit(self.select_window),
                  width=50).place(x=90, y=400)

    def select_insert(self):
        """插入到Text中"""
        sql_res = self.sql2str(self.sql_teacher_all_info())
        s = ''
        for i in range(len(sql_res)):
            s = s + sql_res[i] + '\n'
        self.select_text.insert('end', s)


if __name__ == '__main__':
    window = tk.Tk()
    window.withdraw()
    con = Connect(
        host='localhost',
        user='teacher',
        password='123456',
        database='crdb'
    )
    AdminTeacherManage(window, con, con.cursor(), 'admin', '123456')
