import tkinter as tk
from tkinter import ttk
from pymysql import Connect
from Course_SQL import *


class AdminArrageClass(Course_SQL):
    """
    admin:排课管理
    """

    def __init__(self, parent_window, con, cusor, username, password, window_size='400x500'):
        super(AdminArrageClass, self).__init__(parent_window, username, password, 'admin', '123456')
        self.parent_window = parent_window
        self.adminArrageClassWindow = tk.Toplevel(self.parent_window)
        self.adminArrageClassWindow.title('排课管理界面')
        self.adminArrageClassWindow.geometry(window_size)
        self.con = con
        self.cusor = cusor
        # var
        self.add_sc_Sno_var = tk.StringVar()
        self.add_sc_Cno_var = tk.StringVar()
        self.add_sc_grade_var = tk.StringVar()
        self.add_sc_check_var = tk.BooleanVar()
        self.add_sc_class_var = tk.StringVar()

        # 组件
        tk.Button(self.adminArrageClassWindow, text='添加学生选课', width=35, bg='yellow',
                  command=self.add_student_sc_Window).place(x=100, y=50)
        tk.Button(self.adminArrageClassWindow, text='删除学生选课', width=35, bg='yellow',
                  command=self.drop_student_sc_Window).place(x=100, y=100)
        tk.Button(self.adminArrageClassWindow, text='修改学生选课', width=35, bg='yellow',
                  command=self.update_student_sc_Window).place(x=100, y=150)
        tk.Button(self.adminArrageClassWindow, text='添加老师课程', width=35, bg='yellow',
                  command=self.add_teacher_tc_Window).place(x=100, y=200)
        tk.Button(self.adminArrageClassWindow, text='删除老师课程', width=35, bg='yellow',
                  command=self.drop_teacher_tc_Window).place(x=100, y=250)
        tk.Button(self.adminArrageClassWindow, text='修改老师课程', width=35, bg='yellow',
                  command=self.update_teacher_tc_Window).place(x=100, y=300)
        tk.Button(self.adminArrageClassWindow, text='取消', width=35, bg='yellow',
                  command=lambda: self.window_exit(self.adminArrageClassWindow)).place(x=100, y=350)
        self.adminArrageClassWindow.mainloop()

    def var_init(self):
        """
        var_init
        :return:
        """
        self.add_sc_Sno_var.set('')
        self.add_sc_Cno_var.set('')
        self.add_sc_grade_var.set('')
        self.add_sc_class_var.set('')

    def add_student_sc_Window(self):
        """添加学生选课"""
        # 窗口
        self.add_sc_window = tk.Toplevel(self.adminArrageClassWindow)
        self.add_sc_window.title('添加学生选课')
        self.add_sc_window.geometry('500x600')

        # 组件
        # 学生选课
        self.add_student_Sno_label = tk.Label(self.add_sc_window, text='学号:', width=10)
        self.add_student_Sno_entry = tk.Entry(self.add_sc_window, textvariable=self.add_sc_Sno_var, width=15)
        self.add_student_Cno_label = tk.Label(self.add_sc_window, text='课程', width=10)
        self.add_sc_combobox = ttk.Combobox(self.add_sc_window, textvariable=self.add_sc_Cno_var, width=15, state='readonly')
        self.add_student_grade_label = tk.Label(self.add_sc_window, text='成绩', width=10)
        self.add_student_grade_entry = tk.Entry(self.add_sc_window, textvariable=self.add_sc_grade_var, width=10)
        # 班级选课
        self.add_student_Class_label = tk.Label(self.add_sc_window, text='班级', width=10)
        self.add_student_Class_combobox = ttk.Combobox(self.add_sc_window, textvariable=self.add_sc_class_var, width=15, state='readonly')
        # 课程
        self.add_student_Cno_label.place(x=250, y=50)
        self.add_sc_combobox.place(x=320, y=50)
        course_Cno_info = self.sql_course_Cno_info()
        if course_Cno_info == -1:
            return
        if len(course_Cno_info) == 0:
            Cno_lst = []
        else:
            Cno_lst = [s[0] for s in course_Cno_info]
        self.add_sc_combobox['values'] = Cno_lst
        # 班级
        student_all_info = self.sql_student_all_info()
        if student_all_info == -1:
            self.add_sc_check_var.set(True)
            self.add_sc_hit_check_command()
        else:
            student_class_info = {i[2] for i in student_all_info}
            self.add_student_Class_combobox['values'] = list(student_class_info)
        self.add_sc_hit_check_command()
        # 勾选
        tk.Checkbutton(self.add_sc_window, text='按班级选课', var=self.add_sc_check_var, onvalue=True, offvalue=False,
                       command=self.add_sc_hit_check_command).place(x=150, y=170)
        # Button
        tk.Button(self.add_sc_window, text='选课', width=35, bg='yellow', command=self.add_student_sc_command).place(x=150, y=200)
        tk.Button(self.add_sc_window, text='取消', width=35, bg='yellow', command=lambda: self.window_exit(self.add_sc_window)).place(x=150, y=250)

    def add_sc_hit_check_command(self, grade_window=True):
        """勾选，按照班级选课"""
        check = self.add_sc_check_var.get()
        self.var_init()
        if grade_window:
            self.add_student_grade_label.place(x=50, y=100)
            self.add_student_grade_entry.place(x=120, y=100)
        else:
            self.add_student_grade_label.place_forget()
            self.add_student_grade_entry.place_forget()
        if not check:    # 学生选课
            # 学生选课组件
            self.add_student_Sno_label.place(x=50, y=50)
            self.add_student_Sno_entry.place(x=120, y=50)
            # 遗忘班级选课组件
            self.add_student_Class_label.place_forget()
            self.add_student_Class_combobox.place_forget()
        else:
            self.add_student_Class_label.place(x=50, y=50)
            self.add_student_Class_combobox.place(x=120, y=50)
            # 遗忘学生组件
            self.add_student_Sno_label.place_forget()
            self.add_student_Sno_entry.place_forget()
            self.add_student_grade_label.place_forget()
            self.add_student_grade_entry.place_forget()

    def add_student_sc_command(self):
        """为学生添加课程"""
        check = self.add_sc_check_var.get()
        if not check:   # 学生
            Sno = self.add_sc_Sno_var.get()
            Cno = self.add_sc_Cno_var.get()
            grade = self.add_sc_grade_var.get()
            if len(Sno) * len(Cno) == 0:
                messagebox.showerror(title='add_student_sc_command', message='请输入完整信息')
                return
            sql_res = self.sql_insert_sc(Sno, Cno, grade)
            if sql_res == -1:
                return
            messagebox.showinfo(title='add_student_sc_command', message='学生添加课程成功')
            self.var_init()
        else:       # 班级
            SClass = self.add_sc_class_var.get()
            Cno = self.add_sc_Cno_var.get()
            if len(SClass) * len(Cno) == 0:
                messagebox.showwarning(title='add_student_sc_command', message='请输入完整信息')
                return
            # 检查是否有同学选择相同的课
            sql_res = self.sql_check_select_Class_Cname(SClass, Cno)
            # sql错误
            if sql_res == -1:
                return
            # 有学生选择相同Cname的课程
            if len(sql_res) != 0:
                # 报错信息
                same_sc = [(sc[0], sc[2]) for sc in sql_res]
                str_lst = self.sql2str(same_sc)
                s = ''
                for ss in str_lst:
                    s = s + f'({ss})  '
                messagebox.showwarning(title='add_student_sc_command', message=f'已有同学选择相同的课:{s}')
                return
            # 为班级的所有学生选课
            sql_res = self.sql_insert_sc_by_Class(SClass, Cno)
            if sql_res == -1:
                return
            messagebox.showinfo(title='add_student_sc_command', message='选课成功')
            self.var_init()

    def drop_student_sc_Window(self):
        """删除学生选课"""
        # 窗口
        self.drop_sc_window = tk.Toplevel(self.adminArrageClassWindow)
        self.drop_sc_window.title('添加学生选课')
        self.drop_sc_window.geometry('500x600')

        # 组件
        # 学生选课
        self.add_student_Sno_label = tk.Label(self.drop_sc_window, text='学号:', width=10)
        self.add_student_Sno_entry = tk.Entry(self.drop_sc_window, textvariable=self.add_sc_Sno_var, width=15)
        self.add_student_Cno_label = tk.Label(self.drop_sc_window, text='课程', width=10)
        self.add_sc_combobox = ttk.Combobox(self.drop_sc_window, textvariable=self.add_sc_Cno_var, width=15,
                                            state='readonly')
        self.add_student_grade_label = tk.Label(self.drop_sc_window, text='成绩', width=10)
        self.add_student_grade_entry = tk.Entry(self.drop_sc_window, textvariable=self.add_sc_grade_var, width=10)
        # 班级选课
        self.add_student_Class_label = tk.Label(self.drop_sc_window, text='班级', width=10)
        self.add_student_Class_combobox = ttk.Combobox(self.drop_sc_window, textvariable=self.add_sc_class_var, width=15,
                                                       state='readonly')
        # 课程
        self.add_student_Cno_label.place(x=250, y=50)
        self.add_sc_combobox.place(x=320, y=50)
        course_Cno_info = self.sql_course_Cno_info()
        if course_Cno_info == -1:
            return
        if len(course_Cno_info) == 0:
            Cno_lst = []
        else:
            Cno_lst = [s[0] for s in course_Cno_info]
        self.add_sc_combobox['values'] = Cno_lst
        # 班级
        student_all_info = self.sql_student_all_info()
        if student_all_info == -1:
            self.add_sc_check_var.set(True)
        else:
            student_class_info = {i[2] for i in student_all_info}
            self.add_student_Class_combobox['values'] = list(student_class_info)
        self.add_sc_hit_check_command(grade_window=False)
        # 删除grade
        self.add_student_grade_label.place_forget()
        self.add_student_grade_entry.place_forget()
        # 勾选
        tk.Checkbutton(self.drop_sc_window, text='按班级选课', var=self.add_sc_check_var, onvalue=True, offvalue=False,
                       command=lambda: self.add_sc_hit_check_command(grade_window=False)).place(x=150, y=170)
        # Button
        tk.Button(self.drop_sc_window, text='删除选课', width=35, bg='yellow', command=self.drop_student_sc_command).place(
            x=150, y=200)
        tk.Button(self.drop_sc_window, text='取消', width=35, bg='yellow',
                  command=lambda: self.window_exit(self.drop_sc_window)).place(x=150, y=250)

    def drop_student_sc_command(self):
        """删除学生选课"""
        check = self.add_sc_check_var.get()
        if not check:   # 学生
            Sno, Cno = self.add_sc_Sno_var.get(), self.add_sc_Cno_var.get()
            if len(Sno) * len(Cno) == 0:
                messagebox.showwarning(title='drop_student_sc_command', message='请输入完整')
                return
            # 检查学生是否选择该课程
            sql_res = self.sql_select_sc_by_Sno_Cno(Sno, Cno)
            if len(sql_res) == 0:
                messagebox.showwarning(title='drop_student_sc_command', message='该学生未选择该门课程')
                return
            # 删除学生选课
            sql_res = self.sql_delete_sc_by_Sno_Cno(Sno, Cno)
            if sql_res == -1:   # 报错
                return
            messagebox.showinfo(title='drop_student_sc_command', message='删除学生选课成功')
        else:       # 班级
            Sclass, Cno = self.add_sc_class_var.get(), self.add_sc_Cno_var.get()
            if len(Sclass) * len(Cno) == 0:
                messagebox.showwarning()
                messagebox.showwarning(title='drop_student_sc_command', message='请输入完整')
                return
            # 删除整个班的学生选课
            sql_res = self.sql_delete_sc_by_Sclass_Cno(Sclass, Cno)
            if sql_res == -1:
                return
            messagebox.showinfo(title='drop_student_sc_command', message='删除班级选课成功')
        self.var_init()


    def update_student_sc_Window(self):
        """修改学生选课"""
        ...

    def add_teacher_tc_Window(self):
        """添加老师选课"""
        ...

    def drop_teacher_tc_Window(self):
        """删除老师选课"""
        ...

    def update_teacher_tc_Window(self):
        """修改老师选课"""
        ...


if __name__ == '__main__':
    window = tk.Tk()
    window.withdraw()
    con = Connect(
        host='localhost',
        user='admin',
        password='123456',
        database='crdb'
    )
    AdminArrageClass(window, con, con.cursor(), 'admin', '123456')