from AdminStudentManage import *
from AdminTeacherManage import *
from AdminArrangeClass import *
from Course_SQL import *



class AdminWindow(Course_SQL):
    """
    管理员需求：  1.添加、删除、修改老师
                2.添加、删除、修改学生
                3.添加、删除、修改教室
                4.自动为一个班学生安排课程、老师、教室
                5.查看学生选课（sca视图）
                6.查看老师情况：（tsc视图）
    """
    def __init__(self, parent_window:tk.Tk, username, password, window_size='500x400'):
        super(AdminWindow, self).__init__(parent_window, username, password, 'admin', '123456')
        self.parent_window = parent_window

        # 窗口
        self.adminWindow = tk.Toplevel(self.parent_window)
        self.adminWindow.geometry(window_size)
        self.adminWindow.title('管理员界面')
        sql_res = self.sql_admin_username(username, password)
        if sql_res == -1:
            return
        self.Ano, self.username, self.password = sql_res[0]
        # var

        # 组件
        self.init_Component()


        self.adminWindow.mainloop()

    def init_Component(self):
        """初始化组件"""
        tk.Label(self.adminWindow, text=f'{self.Ano}管理员，您好', width=15, height=1, bg='yellow').place(x=200, y=0)
        tk.Button(self.adminWindow, text='老师管理', width=35, bg='yellow', command=self.teacherManage).place(x=125, y=50)
        tk.Button(self.adminWindow, text='学生管理', width=35, bg='yellow', command=self.studentManage).place(x=125, y=100)
        tk.Button(self.adminWindow, text='教室管理', width=35, bg='yellow', command=self.classroomManage).place(x=125, y=150)
        tk.Button(self.adminWindow, text='课程管理', width=35, bg='yellow', command=self.courseManage).place(x=125, y=200)
        tk.Button(self.adminWindow, text='取消', width=35, bg='yellow', command=lambda: self.window_exit(self.adminWindow)).place(x=125, y=250)

    def teacherManage(self):
        """老师管理"""
        admintm = AdminTeacherManage(self.adminWindow, self.con, self.cusor, self.username, self.password)

    def studentManage(self):
        """学生管理"""
        adminsm = AdminStudentManage(self.adminWindow, self.con, self.cusor, self.username, self.password)

    def classroomManage(self):
        """教室管理"""
        ...

    def courseManage(self):
        """课程管理"""
        admincm = AdminArrageClass(self.adminWindow, self.con, self.cusor, self.username, self.password)


if __name__ == '__main__':
    window = tk.Tk()
    window.title('1')
    # window.iconify()
    window.withdraw()
    AdminWindow(window, 't1', '123456')
    # window.mainloop()
