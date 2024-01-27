from Course_SQL import *


class StudentWindow(Course_SQL):
    """
    学生功能：1.选课（只能做选修课）
            2.查看课表
            3.借教室
    """

    def __init__(self, parent_window, username, password, window_size='500x500', tream_start=None, tream_long=None):
        super(StudentWindow, self).__init__(parent_window, username, password, 'student', '123456')

        self.parent_window = parent_window
        # var
        self.sc_Cname_var = tk.StringVar()
        self.sc_List_var = tk.StringVar()
        self.sc_Cno_var = tk.StringVar()
        self.cancel_sc_List_var = tk.StringVar()
        self.cancel_Cno_var = tk.StringVar()
        self.cancel_Cname_var = tk.StringVar()
        self.show_sc_tream_week_var = tk.StringVar()

        self.borrow_week_var = tk.StringVar()
        self.borrow_day_var = tk.StringVar()
        self.borrow_date_start_hour_var = tk.StringVar()
        self.borrow_date_end_hour_var = tk.StringVar()
        self.listbox_var = tk.StringVar()
        self.borrow_crid_var = tk.StringVar()
        self.borrow_size_var = tk.StringVar()

        # 取消借用var
        self.cancel_borrow_listbox_var = tk.StringVar()

        # 窗口
        self.studenWindow = tk.Toplevel(self.parent_window)
        self.studenWindow.geometry(window_size)
        self.studenWindow.title('学生登录界面')
        # 组件
        tk.Label(self.studenWindow, text=f'{self.username}同学,您好', bg='yellow', fg='red').place(x=230, y=0)
        # menu
        main_menu = tk.Menu(self.studenWindow)
        exit_menu = tk.Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label='exit', menu=exit_menu)
        exit_menu.add_command(label='exit', command=lambda: self.window_exit(self.studenWindow))
        self.studenWindow.config(menu=main_menu)
        # 选课
        tk.Button(self.studenWindow, text='选课', bg='yellow', width=45, height=2,
                  command=self.selectClass_Window).place(x=100, y=50)
        tk.Button(self.studenWindow, text='取消选课', bg='yellow', width=45, height=2,
                  command=self.cancelClass_Window).place(x=100, y=120)
        # 查看课表
        tk.Button(self.studenWindow, text='查看课表', bg='yellow', width=45, height=2,
                  command=self.student_class_Window).place(x=100, y=190)
        # 借教室
        tk.Button(self.studenWindow, text='借教室', bg='yellow', width=45, height=2,
                  command=self.borrow_classroom_Window).place(x=100, y=260)
        tk.Button(self.studenWindow, text='取消借用', bg='yellow', width=45, height=2,
                  command=self.cancelBorrowWindow).place(x=100, y=330)
        # 取消
        tk.Button(self.studenWindow, text='取消', bg='yellow', width=45, height=2,
                  command=lambda: self.window_exit(self.studenWindow)).place(x=100, y=400)

        # 登录学生的信息
        sql_res = self.sql_student_username(username, password)
        if sql_res == -1:
            self.window_exit(self.studenWindow)
            return
        print(sql_res)
        self.Sno, self.Sname, self.Sclass = sql_res[:-2]

        self.studenWindow.mainloop()
        self.con.close()
        print('连接释放完毕')

    def var_init(self):
        """清空var"""
        self.sc_Cname_var.set('')
        self.sc_List_var.set('')
        self.sc_Cno_var.set('')
        self.cancel_sc_List_var.set('')
        self.cancel_Cno_var.set('')
        self.cancel_Cname_var.set('')

        self.show_sc_tream_week_var.set('')

        self.borrow_week_var.set('')
        self.borrow_day_var.set('')
        self.borrow_date_start_hour_var.set('')
        self.borrow_date_end_hour_var.set('')
        self.listbox_var.set('')
        self.borrow_crid_var.set('')
        self.borrow_size_var.set('')
        self.cancel_borrow_listbox_var.set('')

        self.borrow_course_start_time = ''
        self.borrow_course_end_time = ''

    def sc_Combobox_bind(self, event):
        """下拉框事件,(Tname,Cname,address,start,end)"""
        # print(self.sc_Cname_var.get())
        Cname = self.sc_Cname_var.get()
        try:
            # 查已经选择的课
            self.cusor.execute("""
                select * from scs where Sno=%s;
            """, (self.Sno,))
            my_sc = self.cusor.fetchall()
            for i in range(len(my_sc)):
                # 已经选择该课程，不可重复选择
                if Cname in my_sc[i]:
                    messagebox.showerror(title='选课(sc_Combobox_bind)', message='已有该课程')
                    return
            # 找到Cname的课程信息
            self.cusor.execute("""
              select teacher.Tname,course.Cno,course.Cname,classroom.address,teacher_borrow.start,
              teacher_borrow.end
                from teacher,teacher_borrow,classroom,course
                where teacher.Tno=teacher_borrow.Tno and classroom.classroom_id=teacher_borrow.classroom_id
                and course.Cno=teacher_borrow.Cno and course.selectClass=TRUE and Cname=%s;
            """, (Cname,))
            sql_res = self.cusor.fetchall()
        except Exception as e:
            messagebox.showerror(title='学生选课', message=e)
            return
            # 未找到
        if len(sql_res) == 0:
            return
        # 事件和选课表冲突
        target_class_lst = []
        for i in range(len(sql_res)):
            for j in range(len(my_sc)):
                if not ((sql_res[i][-2] <= my_sc[j][-2] and sql_res[i][-2] <= my_sc[j][-2]) or
                        sql_res[i][-2] >= my_sc[j][-2] and sql_res[i][-1] >= my_sc[j][-1]):
                    break
            else:
                target_class_lst.append(sql_res[i])

        sql_res = target_class_lst
        print(sql_res)
        s = ''
        listbox = []
        # 遍历每门课,获得Cname对应的所有课程
        for i in range(len(sql_res)):
            for j in range(len(sql_res[0]) - 2):
                s += sql_res[i][j] + ','
            s += (sql_res[i][-2].strftime('%Y-%m-%d') + ',')
            s += (sql_res[i][-1].strftime('%Y-%m-%d'))
            # print(s)
            listbox.append(s)
        self.sc_List_var.set(listbox)

    def select_Cno_command(self):
        """选择Cno"""
        try:
            s = self.listbox.get(self.listbox.curselection())  # 获取点击的Cno
        except Exception as e:
            messagebox.showerror(title='选课（select_Cno_command）', message=e)
            return
        if len(s) == 0:
            messagebox.showwarning(title='select_Cno_command', message='请选择Cno')
            return
        Cno = s.strip().split(',')[1]
        self.sc_Cno_var.set(Cno)

    def sc_insert_command(self):
        """选课"""
        try:
            self.cusor.execute("""
                insert into SC(Sno,Cno) values(%s,%s);
            """, (self.Sno, self.sc_Cno_var.get()))
            self.con.commit()
            messagebox.showinfo(title='选课(sc_insert_command)', message=f'选课成功，选择课程{self.sc_Cno_var.get()}')
            self.var_init()
            return
        except Exception as e:
            messagebox.showerror(title='选课错误(sc_insert_command)', message=e)
            return

    def selectClass_Window(self):
        """选课,通过Cname选课，可以查看不同课的时间、老师、地点"""
        # 选课窗口
        self.scWindow = tk.Toplevel(self.studenWindow)
        self.scWindow.title('选课')
        self.scWindow.geometry('1000x700')
        # 组件
        # 课程名
        tk.Label(self.scWindow, text='课程名:').place(x=50, y=50)
        combobox = ttk.Combobox(self.scWindow, textvariable=self.sc_Cname_var, state='readonly',
                                width=25, height=1)
        combobox['values'] = ('math', 'Chinese', 'English', 'DatabBase', 'DeepLearning', 'MechineLearning')
        combobox.current(0)
        combobox.bind('<<ComboboxSelected>>', self.sc_Combobox_bind)
        combobox.place(x=150, y=50)
        # 显示课程
        tk.Label(self.scWindow, text='课程号:').place(x=50, y=150)
        self.listbox = tk.Listbox(self.scWindow, listvariable=self.sc_List_var, height=10, width=50)
        self.listbox.place(x=150, y=150)
        tk.Button(self.scWindow, text='select class', width=50, height=2,
                  command=self.select_Cno_command).place(x=150, y=350)
        tk.Label(self.scWindow, text='课程号:').place(x=50, y=400)
        tk.Entry(self.scWindow, textvariable=self.sc_Cno_var, width=50).place(x=150, y=410)

        tk.Button(self.scWindow, text='确定', command=self.sc_insert_command,
                  height=2, width=50).place(x=150, y=460)
        tk.Button(self.scWindow, text='取消', command=lambda: self.window_exit(self.scWindow),
                  height=2, width=50).place(x=150, y=550)

    #############################################################################

    def cancel_sc_Combobox_bind(self, event):
        """取消选课，将Combobox的Cname查询到Listbox中"""
        Cname = self.cancel_Cname_var.get()
        try:
            # 查已经选择的课
            my_sc = self.show_sc_by_student(self.Sno)
            for i in range(len(my_sc)):
                # 已经选择该课程，不可重复选择
                if Cname not in my_sc[i]:
                    messagebox.showerror(title='取消选课(cancel_sc_Combobox_bind)', message='未选择该门课')
                    return
            # 找到Cname的课程信息
        except Exception as e:
            messagebox.showerror(title='取消选课(cancel_sc_Combobox_bind)', message=e)
            return
        sql_res = my_sc
        if len(sql_res) == 0:
            return
        print(sql_res)
        s = ''
        listbox = []
        # 遍历每门课,获得Cname对应的所有课程
        for i in range(len(sql_res)):
            for j in range(len(sql_res[0]) - 2):
                s += sql_res[i][j] + ','
            s += (sql_res[i][-2].strftime('%Y-%m-%d') + ',')
            s += (sql_res[i][-1].strftime('%Y-%m-%d'))
            # print(s)
            listbox.append(s)
        self.cancel_sc_List_var.set(listbox)

    def select_cancel_Cno_command(self):
        """选择Cno"""
        try:
            s = self.cancel_listbox.get(self.cancel_listbox.curselection())  # 获取点击的Cno
        except Exception as e:
            messagebox.showerror(title='选课（select_Cno_command）', message=e)
            return
        if len(s) == 0:
            messagebox.showwarning(title='select_Cno_command', message='请选择Cno')
            return
        Cno = s.strip().split(',')[2]
        self.cancel_Cno_var.set(Cno)

    def cancelClass_Window(self):
        """取消选课"""
        self.ccWindow = tk.Toplevel(self.studenWindow)
        self.ccWindow.geometry('1000x600')
        self.ccWindow.title('取消选课')
        # 组件
        tk.Label(self.ccWindow, text='课程名:').place(x=50, y=50)
        combobox = ttk.Combobox(self.ccWindow, textvariable=self.cancel_Cname_var, state='readonly',
                                width=25, height=1)
        # 查询该学生已经选择的课程
        student_cs = self.show_sc_by_student(self.Sno)
        print(student_cs)
        student_class = set()
        for class_ in student_cs:
            if len(class_) == 0:
                break
            student_class.add(class_[3])

        # 将学生已选的课显示在Combobox中
        combobox['values'] = list(student_class)
        combobox.bind('<<ComboboxSelected>>', self.cancel_sc_Combobox_bind)
        combobox.place(x=150, y=50)
        # 显示课程
        tk.Label(self.ccWindow, text='课程号:').place(x=50, y=150)
        self.cancel_listbox = tk.Listbox(self.ccWindow, listvariable=self.cancel_sc_List_var, height=10, width=50)
        self.cancel_listbox.place(x=150, y=150)
        tk.Button(self.ccWindow, text='select class', width=50, height=2,
                  command=self.select_cancel_Cno_command).place(x=150, y=350)
        tk.Label(self.ccWindow, text='课程号:').place(x=50, y=400)
        tk.Entry(self.ccWindow, textvariable=self.cancel_Cno_var, width=50).place(x=150, y=410)
        tk.Button(self.ccWindow, text='确定', command=lambda: self.cancel_delete_sc(self.Sno, self.cancel_Cno_var.get()),
                  height=2, width=50).place(x=150, y=460)
        tk.Button(self.ccWindow, text='取消', command=lambda: self.window_exit(self.ccWindow),
                  height=2, width=50).place(x=150, y=550)

    ##########################################################################
    ## 选择课表

    def show_course_insert_text(self, course_lst):
        """将课程列表插入到Text中"""
        s = '\t\t星期1\t\t\t星期2\t\t\t星期3\t\t\t星期4\t\t\t星期5\t\t\t星期6\t\t\t星期7\n'
        # course_lst[i][j]:第i个星期的第j节课
        for j in range(len(course_lst[0])):  # 第j节课
            s += f'第{j}节课\t\t'
            for i in range(len(course_lst)):  # 第i个星期
                if course_lst[i][j] is None:
                    s += '无\t\t\t'
                    continue
                s += ','.join(course_lst[i][j])
                s += '\t\t\t'
            s += '\n'
        s += '\n'
        self.student_class_text.insert('end', s)

    def show_class_bind(self, event):
        """显示课表"""
        # 获取周的日期
        self.student_class_text.delete('1.0', tk.END)
        weeks = self.show_sc_tream_week_var.get()
        weeks = int(weeks.replace('第', '').replace('周', ''))
        if not (1 <= weeks <= self.tream_long):
            messagebox.showerror(title='显示(show_class_bind)', message='查看课表日期错误，该学期没有该时间')
            return
        tream_start_date = deepcopy(self.tream_start)
        week1_date = tream_start_date + datetime.timedelta(days=(weeks - 1) * 7)
        week7_date = week1_date + datetime.timedelta(days=6)
        # 课程列表
        week_course_lst = [[None] * 10 for _ in range(7)]
        # sql
        sql_res = self.sql_StartEndDatetime2SCS(self.Sno, week1_date, week7_date)
        # 发生错误
        if sql_res == -1:
            return
        for i in range(len(sql_res)):
            if len(sql_res[i]) != 0:
                Sno, Sname, Cno, Cname, Tno, Tname, address, start, end = sql_res[i]
                start: datetime.datetime = start
                end: datetime.datetime = end
                # 星期几
                course_week = start.weekday()
                # 第几节课,判断是否合法
                if start.day != end.day:
                    messagebox.showwarning(title='课程错误(show_class_bind)',
                                           message=f'太卷了!!!:{Cno},{start}--{end}')
                    continue
                elif 8 <= start.hour <= 11 and end.hour > 12:
                    messagebox.showwarning(title='课程错误(show_class_bind)',
                                           message=f'中午不能上课,课程号:{Cno},{start}--{end}')
                    continue
                elif 2 <= start.hour <= 6 and end.hour > 6:
                    messagebox.showwarning(title='课程错误(show_class_bind)',
                                           message=f'晚饭时间不能上课,课程号:{Cno},{start}--{end}')
                    continue
                # 第几节课,插入到课程列表中
                if start.hour <= 11:  # 上午的课
                    day_course_start = start.hour - 8
                    day_course_end = end.hour - 8
                    week_course_lst[course_week][day_course_start: day_course_end] = [[Cname, Tname, address] for j in
                                                                                      range(
                                                                                          day_course_end - day_course_start)]
                elif 14 <= start.hour <= 17:
                    day_course_start = start.hour - 14
                    day_course_end = end.hour - 14
                    week_course_lst[course_week][day_course_start + 4: day_course_end + 4] = [[Cname, Tname, address]
                                                                                              for j in range(
                            day_course_end - day_course_start)]
                elif 19 <= start.hour <= 20:
                    day_course_start = start.hour - 19
                    day_course_end = end.hour - 19
                    week_course_lst[course_week][day_course_start + 8: day_course_end + 8] = [[Cname, Tname, address]
                                                                                              for j in range(
                            day_course_end - day_course_start)]

                for day in range(len(week_course_lst)):
                    print(week_course_lst[day])
                # 插入到Text中
                self.show_course_insert_text(week_course_lst)

    def student_class_Window(self):
        """课表"""
        self.show_sc_window = tk.Toplevel(self.studenWindow)
        self.show_sc_window.title('学生课表')
        self.show_sc_window.geometry('2000x600')
        # 组件
        tk.Label(self.show_sc_window, text=f'{self.Sname}同学，您好', width=75, height=2, bg='yellow',
                 fg='red').place(x=250, y=0)
        tk.Label(self.show_sc_window, text=f'您的课表如下：', width=75, height=2, bg='yellow',
                 fg='red').place(x=250, y=25)
        # 选择第几周的课表
        tk.Label(self.show_sc_window, text='第几周:', width=10, height=1).place(x=400, y=100)
        self.show_sc_combobox = ttk.Combobox(self.show_sc_window, textvariable=self.show_sc_tream_week_var,
                                             values=[f'第{i}周' for i in range(1, self.tream_long + 1)], width=10,
                                             state='readonly')
        self.show_sc_combobox.place(x=550, y=100)
        self.show_sc_combobox.bind('<<ComboboxSelected>>', self.show_class_bind)
        # 显示
        self.student_class_text = tk.Text(self.show_sc_window, height=20, width=170)
        self.student_class_text.place(x=50, y=200)
        tk.Button(self.show_sc_window, text='取消', width=75, height=2, bg='yellow',
                  command=lambda: self.window_exit(self.show_sc_window)).place(x=250, y=530)

    ######################################################
    ## 借教室
    def select_classroom(self):
        """选择可以借用的教室"""
        # 接受参数
        tream_start = deepcopy(self.tream_start)
        tream_long = self.tream_long
        week = self.borrow_week_var.get()
        day = self.borrow_day_var.get()
        start_course = self.borrow_date_start_hour_var.get()
        end_course = self.borrow_date_end_hour_var.get()
        req_size = self.borrow_size_var.get()

        # 检查
        if len(week) * len(day) * len(start_course) * len(end_course) * len(req_size) == 0:
            messagebox.showerror(title='查询教室错误(select_classroom)', message='请输入完整')
            return
        # 需要的教室大小
        try:
            req_size = int(req_size)
            if req_size <= 0 or req_size > 300:
                messagebox.showwarning(title='借用教室输入错误(select_classroom)', message='教室大小不符合实际要求')
                return
        except:
            messagebox.showerror(title='借用教室输入错误(select_classroom)', message='教室大小输入错误')
            return
        # 输入日期
        week = int(week.replace('第', '').replace('周', ''))
        day = int(day.replace('星期', ''))
        start_course = int(start_course.replace('第', '').replace('节课', ''))
        end_course = int(end_course.replace('第', '').replace('节课', ''))
        course_time_lst = [8, 9, 10, 11, 14, 15, 16, 17, 19, 20]
        # start<end
        if start_course > end_course:
            messagebox.showerror(title='查找教室失败(select_classroom)', message='start>=end')
            return
        elif not (1 <= start_course <= 10 and 1 <= end_course <= 10):
            messagebox.showerror(title='查找教室失败(select_classroom)', message='start,end:1~10')
            return
        elif start_course <= 4 and end_course >= 5:
            messagebox.showerror(title='查找教室失败(select_classroom)', message='中午不能上课')
            return
        elif 5 <= start_course <= 8 and end_course >= 9:
            messagebox.showerror(title='查找教室失败(select_classroom)', message='晚饭不能上课')
            return
        # 获取具体时间
        # 具体日期
        date = tream_start + datetime.timedelta((week - 1) * 7)
        date = date + datetime.timedelta(day - 1)
        # 时间
        start_time = datetime.datetime.combine(date, datetime.time(course_time_lst[start_course - 1], 0, 0))
        end_time = datetime.datetime.combine(date, datetime.time(course_time_lst[end_course - 1] + 1, 0, 0))
        self.borrow_course_start_time = start_time
        self.borrow_course_end_time = end_time

        # sql查找start~end没有冲突,大于req_size的classroom_id
        sql_res = self.sql_StartEndSize2Classroom(start_time, end_time, req_size)
        # 报错
        if sql_res == -1:
            return
        # 将查询到的插入到listbox
        if len(sql_res) == 0:
            self.listbox_var.set('')
            return
        classroom_lst = []
        for classroom_info in sql_res:
            classroom_id, address, size = classroom_info
            classroom_lst.append(','.join([classroom_id, address, str(size)]))
        self.listbox_var.set(classroom_lst)

    def borrow_classroom(self):
        """借用教室"""
        # 获得输入
        classroom_info = self.borrow_listbox.get(self.borrow_listbox.curselection())
        classroom_id, address, size = classroom_info.strip().split(',')
        if classroom_id == '':
            messagebox.showwarning(title='借教室错误(borrow_classroom)', message='教室号为空')
            return
        print(classroom_id)
        sql_res = self.sql_insert_student_borrow(self.Sno, classroom_id, '开会', self.borrow_course_start_time, self.borrow_course_end_time)
        if sql_res == -1:
            return
        messagebox.showinfo(title='借用教室(borrow_classroom)', message=f'借用教室：{classroom_id}成功')

    def borrow_classroom_Window(self):
        """借教室,根据时间，借用教室"""
        # 窗口
        self.borrow_cr_window = tk.Toplevel(self.studenWindow)
        self.borrow_cr_window.title('借用教室')
        self.borrow_cr_window.geometry('1000x600')
        # 借用日期
        tk.Label(self.borrow_cr_window, text='借用日期:', width=10).place(x=150, y=50)
        self.borrow_combobox_date = ttk.Combobox(self.borrow_cr_window, textvariable=self.borrow_week_var,
                                                 values=[f'第{i}周' for i in range(1, self.tream_long + 1)], width=15,
                                                 state='readonly')
        self.borrow_combobox_date.place(x=250, y=50)
        # 借用星期几
        tk.Label(self.borrow_cr_window, text='星期几', width=10).place(x=400, y=50)
        self.borrow_combobox_start = ttk.Combobox(self.borrow_cr_window, textvariable=self.borrow_day_var,
                                                  values=[f'星期{i}' for i in range(1, 8)], width=15, state='readonly')
        self.borrow_combobox_start.place(x=500, y=50)

        # 从第几节课到第几节课
        tk.Label(self.borrow_cr_window, text='从第几节课借到第几节课', width=20).place(x=100, y=100)
        self.borrow_combobox_start = ttk.Combobox(self.borrow_cr_window, textvariable=self.borrow_date_start_hour_var,
                                                  values=[f'第{i}节课' for i in range(1, 11)], width=15, state='readonly')
        self.borrow_combobox_start.place(x=250, y=100)

        tk.Label(self.borrow_cr_window, text='到', width=1).place(x=425, y=100)
        self.borrow_combobox_end = ttk.Combobox(self.borrow_cr_window, textvariable=self.borrow_date_end_hour_var,
                                                values=[f'第{i}节课' for i in range(1, 11)], width=15, state='readonly')
        self.borrow_combobox_end.place(x=500, y=100)
        # 教室大小
        tk.Label(self.borrow_cr_window, text='教室大小', width=15).place(x=650, y=100)
        tk.Entry(self.borrow_cr_window, textvariable=self.borrow_size_var, width=15).place(x=750, y=100)
        # 查询按钮
        tk.Button(self.borrow_cr_window, text='查询', width=50, bg='yellow', command=self.select_classroom).place(x=300,y=150)
        # Listbox
        self.borrow_listbox = tk.Listbox(self.borrow_cr_window, listvariable=self.listbox_var, width=100, height=15)
        self.borrow_listbox.place(x=150, y=200)
        # 按钮
        tk.Button(self.borrow_cr_window, text='确定', width=50, bg='yellow',
                  command=self.borrow_classroom).place(x=300, y=500)
        tk.Button(self.borrow_cr_window, text='取消', width=50, bg='yellow',
                  command=lambda: self.window_exit(self.borrow_cr_window)).place(x=300, y=550)

    ##########################################################################
    ## 取消借用
    def cancelBorrowWindow(self):
        """取消借用窗口"""
        self.cancel_Borrow_Window = tk.Toplevel(self.studenWindow)
        self.cancel_Borrow_Window.title('取消借用')
        self.cancel_Borrow_Window.geometry('1000x600')
        # 组件
        tk.Label(self.cancel_Borrow_Window, text='您的借用信息:', width=10, height=1).place(x=200, y=10)
        # 获取该学生借用的教室信息
        student_borrow_info = self.sql_Sno2Classroom_info(self.Sno)  # sql获取借用教室信息(Sno,Cid,use_to,start, end)
        if student_borrow_info == -1:  # sql报错
            messagebox.showerror(title='取消借用错误(sql_Sno2Classroom_info)', message='取消借用错误')
            self.window_exit(self.cancel_Borrow_Window)
            return
        # 绑定到var中
        try:
            self.cancel_borrow_listbox_var.set(self.sql2str_start_end(student_borrow_info))
        except Exception as e:
            messagebox.showerror(title='取消借用失败(cancelBorrowWindow)', message='取消借用失败，请检查日期')
            self.window_exit(self.cancel_Borrow_Window)
            return
        # ListBox
        self.cancel_borrow_listbox = tk.Listbox(self.cancel_Borrow_Window, listvariable=self.cancel_borrow_listbox_var,
                                                width=50, height=10)
        self.cancel_borrow_listbox.place(x=300, y=10)
        # Button
        tk.Button(self.cancel_Borrow_Window, text='取消借用', width=50, bg='yellow',
                  command=self.cancel_borrow_command).place(x=300, y=200)
        tk.Button(self.cancel_Borrow_Window, text='取消', width=50, bg='yellow',
                  command=lambda: self.window_exit(self.cancel_Borrow_Window)).place(x=300, y=250)

    def cancel_borrow_command(self):
        """取消借用按钮"""
        # 读取信息
        sql_str: str = self.cancel_borrow_listbox.get(self.cancel_borrow_listbox.curselection())
        if len(sql_str) == 0:
            messagebox.showwarning(title='取消借用失败(cancel_borrow_command)', message='listbox点击错误')
            return
        try:
            Sno, Cid, use_to, start, end = sql_str.split(',')
            start = self.courseTime2datetime(start)
            end = self.courseTime2datetime(end)
            end = end + datetime.timedelta(hours=1)
            # sql删除student_borrow
            self.cusor.execute("""
                delete from student_borrow 
                where Sno=%s and Classroom_id=%s and use_to=%s and start=%s and end=%s; 
            """, (Sno, Cid, use_to, start, end))
            self.con.commit()
            messagebox.showinfo(title='取消借用成功(cancel_borrow_command)', message='取消借用成功')
            self.var_init()
        except Exception as e:
            messagebox.showerror(title='取消借用失败(cancel_borrow_command)', message=e)
            return


if __name__ == '__main__':
    window = tk.Tk()
    window.withdraw()
    StudentWindow(window, 's1', '123456')
