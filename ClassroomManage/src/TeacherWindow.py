from Course_SQL import *


class TeacherWindow(Course_SQL):
    """
    老师需求：1.根据学生数量借教室
            2.查看课程学生
            3.为该课程的学生打分
            4.查看教室信息
            5.查看自己的课表：视图
    """
    def __init__(self, parent_window, username, password, window_size='500x500'):
        super(TeacherWindow, self).__init__(parent_window, username, password, 'teacher', '123456')
        self.parent_window: tk.Tk = parent_window
        # 学生用户mysql连接
        self.con = Connect(
            host='localhost',
            user='teacher',
            password='123456',
            database='crdb'
        )
        self.username = username
        self.password = password
        # 窗口
        self.teacherWindow = tk.Toplevel(self.parent_window)
        self.teacherWindow.geometry(window_size)
        self.teacherWindow.title('老师登录界面')
 
        self.teacherWindow.mainloop()