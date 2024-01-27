import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from pymysql import *
import datetime
from copy import deepcopy


class Course_SQL:
    def __init__(self, parent_window, username, password, sql_user, sql_password,
                 datebase='crdb', host='localhost', tream_start=None, tream_long=None):
        # student用户mysql连接
        self.con = Connect(
            host=host,
            user=sql_user,
            password=sql_password,
            database=datebase
        )
        self.cusor = self.con.cursor()
        self.username = username
        self.password = password

        # 学期开始时间
        self.tream_start = tream_start
        # 学期持续时间
        self.tream_long = tream_long
        if tream_start is None:  # 默认值
            self.tream_start = datetime.date(2023, 9, 4)  # 星期一
        else:
            # 判断是否为星期1
            if self.tream_start.weekday() != 0:
                self.tream_start -= datetime.timedelta(self.tream_start.weekday())
        if tream_long is None or tream_long <= 0:
            self.tream_long = 20  # 20周
        elif type(tream_long) == type(float):
            self.tream_long = int(self.tream_long) + 1
        print(f'开学日期为{self.tream_start},持续{self.tream_long}周')
        # 上课时间
        self.course_start_time_lst = [8, 9, 10, 11, 14, 15, 16, 17, 19, 20]

    def var_init(self):
        """清空var"""
        ...

    def window_exit(self, window):
        self.var_init()
        window.destroy()

    def sql_student_username(self, username, password):
        """
        select * from student
        :param username:
        :param password:
        :return:
        """
        # 获得学生学号
        try:
            self.cusor.execute("""
                                 select * from student where username=%s and password=%s;
                             """, (username, password))
            sql_res = self.cusor.fetchall()
            if len(sql_res) == 0:
                return []
            return sql_res[0]
        except Exception as e:
            messagebox.showerror(title='(sql_student_username)', message=e)
            return -1

    def sql_student_all_info(self):
        """
        所有学生信息
        :return:
        """
        try:
            self.cusor.execute("""
                                    select * from student;
                                """)
            sql_res = self.cusor.fetchall()
            if len(sql_res) == 0:
                return []
            return sql_res
        except Exception as e:
            messagebox.showerror(title='(sql_student_username)', message=e)
            return -1

    def sql2str(self, sql_res):
        """sql->str"""
        sql_str_lst = []
        for i in range(len(sql_res)):
            if len(sql_res[i]) == 0:
                continue
            sql_str_lst.append(','.join(list(sql_res[i])))
        return sql_str_lst

    def sql_insert_student(self, Sno, Sname, Sclass, Susername, Spassword):
        """
        插入到student
        insert into student:Sno,Sname,Sclass,Susername,Spassword
        :param Sno:
        :param Sname:
        :param Sclass:
        :param Susername:
        :param Spassword:
        :return:
        """
        try:
            self.cusor.execute("""
                insert into student values(%s,%s,%s,%s,%s)
            """, (Sno, Sname, Sclass, Susername, Spassword))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='插入学生错误(sql_insert_student)', message=e)
            return -1

    def sql_delete_student_Sno(self, Sno):
        """
        delete student:Sno
        :return:
        """
        try:
            self.cusor.execute("""
                delete from student where Sno=%s;
            """, (Sno,))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='(sql_delete_student_Sno)', message=e)
            return -1

    def sql_update_student_Sno(self, Sno, info_type, info):
        """
        update student:Sno
        :param Sno:
        :param info_type:
        :param info:
        :return:
        """
        try:
            self.cusor.execute("""
                update student set {}=%s where Sno=%s;
            """.format(info_type), (info, Sno))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='(sql_update_student_Sno)', message=e)
            return -1

    def sql_admin_username(self, username, password):
        """admin信息"""
        try:
            self.cusor.execute("""
                select * from admin where username=%s and password=%s;
            """, (username, password))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='老师信息错误(sql_teacher_username)', message=e)
            return -1

    def show_sc_by_student(self, Sno):
        """
        Sno->课程
        Sno,Sname,Tno,Tname,Cno,Cname,address,start,end
        """
        try:
            self.cusor.execute("""
                select * from scs 
                where Sno=%s ;
            """, (Sno,))
            sql_tuple = self.cusor.fetchall()
            # print(sql_tuple)
            return sql_tuple
        except Exception as e:
            messagebox.showerror(title='取消错误(show_sc_by_student)', message=e)
            return -1

    def cancel_delete_sc(self, Sno, Cno):
        """
        从数据库中删除选课
        delete from sc:Sno,Cno
        """
        try:
            self.cusor.execute("""
                delete from sc where Sno=%s and Cno=%s
            """, (Sno, Cno))
            self.con.commit()
            messagebox.showinfo(title='取消选课(cancel_delete_sc)', message=f'取消选课成功,课程号{Cno}')
            self.var_init()
            return 1
        except Exception as e:
            messagebox.showerror(title='取消选课(cancel_delete_sc)', message=e)
            return -1

    def sql_StartEndDatetime2SCS(self, Sno, week1_date: datetime.datetime, week7_date: datetime.datetime):
        """
        Sno,start,end->Sno,Sname,Cno,Cname,Tno,Tname,address,start,end
        :param Sno: 学号
        :param week1_date: start
        :param week7_date: end
        :return: sql_res
        """
        try:
            # 数据库中查询从week1_date~week7_date的该学生课程，视图(scs)
            self.cusor.execute("""
                       select * from scs where scs.start>=%s and scs.end<=%s and Sno=%s
                   """, (week1_date, week7_date, Sno))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='查看课表错误(show_class_bind)', message=e)
            return -1

    def sql_StartEndSize2Classroom(self, start_time, end_time, req_size):
        """
        满足要求的classroom_id
        start_time,end_time,size->classroom_id
        :param start_time:
        :param end_time:
        :param req_size:
        :return:
        """
        # # 数据库中查找
        try:
            self.cusor.execute("""
                     select x.*
                       from classroom x
                       where x.Classroom_id not in
                       (
                           /*时间冲突*/
                           select teacher_borrow.Classroom_id from teacher_borrow, student_borrow
                           where not ((%s<=teacher_borrow.start or %s>=teacher_borrow.end) and
                           (%s<=student_borrow.start or %s>=student_borrow.end))
                       ) and %s<=x.size;
                   """, (end_time, start_time, end_time, start_time, req_size))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='借教室错误(select_classroom)', message=e)
            return -1

    def sql_insert_student_borrow(self, Sno, classroom_id, use_to, borrow_course_start_time, borrow_course_end_time):
        """
        insert into student_borrow: Sno,classroom_id,use_to,start,end
        :param Sno:
        :param classroom_id:
        :param use_to:
        :param borrow_course_start_time:
        :param borrow_course_end_time:
        :return:
        """
        try:
            # 插入到student_borrow
            self.cusor.execute("""
                       insert into student_borrow(Sno,Classroom_id,use_to,start,end) 
                       values (%s,%s,%s,%s,%s) 
                   """, (Sno, classroom_id, use_to, borrow_course_start_time, borrow_course_end_time,))
            self.con.commit()
            self.var_init()
            return 1
        except Exception as e:
            messagebox.showerror(title='借用教室(borrow_classroom)', message=e)
            return -1

    def sql_Sno2Classroom_info(self, Sno):
        """
        Sno->student_borrow
        Sno,Classroom_id,use_to,start,end
        """
        try:
            self.cusor.execute("""
                select * from student_borrow where Sno=%s;
            """, (Sno,))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            return -1

    def sql2str_start_end(self, sql_res):
        """
        sql->str
        Sno,Classroom_id,use_to,start,end->str
        """
        if len(sql_res) == 0:
            return []
        sql_str_lst = []
        for i in range(len(sql_res)):
            if len(sql_res[i]) == 0:
                continue
            # 将(Sno,Cid,use_to,start, end)->str
            Sno, Cid, use_to, start, end = sql_res[i]
            start = self.datetime2courseTime(start)
            end = self.datetime2courseTime(end - datetime.timedelta(hours=1))
            # 报错
            if start == -1 or end == -1:
                return -1
            sql_str_lst.append(','.join([Sno, Cid, use_to, start, end]))
        return sql_str_lst

    def datetime2courseTime(self, time: datetime.datetime):
        """将datetime->courseTime"""
        tream_start = self.tream_start
        tream_long = self.tream_long
        tream_end = tream_start + datetime.timedelta(days=tream_long * 7)
        if time.date() < tream_start or time.date() > tream_end:
            raise Exception('(datetime2courseTime),time.date不在本学期的日期中')
        # 周
        weeks = (time.date() - tream_start).days // 7 + 1
        # 星期几
        days = (time.date() - tream_start).days % 7 + 1
        # 第几节课
        hour = time.hour
        course_time = -1
        course_start_time_lst = self.course_start_time_lst
        for i in range(len(course_start_time_lst)):
            if course_start_time_lst[i] == hour:
                course_time = i + 1
                break
        if course_time == -1:
            raise Exception('(datetime2courseTime),time.hour不在本学期的日期中')
        # 变为字符串
        s = f'第{weeks}周 星期{days} 第{course_time}节课'
        return s

    def courseTime2datetime(self, courseTime):
        """str->datetime"""
        weeks_str, days_str, course_str = courseTime.split(' ')
        weeks = int(weeks_str[1: -1])
        days = int(days_str[2:])
        course = int(course_str[1: -2])
        tream_start = deepcopy(self.tream_start)
        tream_long = deepcopy(self.tream_long)
        # date
        tream_start += datetime.timedelta(days=(weeks - 1) * 7 + days - 1)
        # time
        time = datetime.time(hour=self.course_start_time_lst[course - 1])
        date_time = datetime.datetime.combine(tream_start, time)
        return date_time

    def sql_teacher_username(self, username, password):
        """老师信息"""
        try:
            self.cusor.execute("""
                select * from teacher where username=%s and password=%s;
            """, (username, password))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='老师信息错误(sql_teacher_username)', message=e)
            return -1

    def sql_insert_teacher_user(self, Tno, Tname, username, password):
        """
        insert into teacher: Tno, Tname, username, password
        :param Tno:
        :param Tname:
        :param username:
        :param password:
        :return:
        """
        try:
            self.cusor.execute("""
                insert into teacher values(%s,%s,%s,%s);
            """, (Tno, Tname, username, password))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_insert_teacher_user', message=e)
            return -1

    def sql_teacher_all_info(self):
        """
        select * from teacher
        :return:
        """
        try:
            self.cusor.execute("""
                select * from teacher;
            """)
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='sql_teacher_all_info', message=e)
            return -1

    def sql_delete_teacher_Tno(self, Tno):
        """
        delete teacher:Tno
        :param Tno:
        :return:
        """
        try:
            self.cusor.execute("""
                delete from teacher where Tno=%s;
            """, (Tno, ))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_delete_teacher_Tno', message=e)
            return -1

    def sql_update_teacher_Sno(self, Tno, info_type, info):
        """
        update teacher type=info where Tno;
        :param Tno:
        :param info_type:
        :param info:
        :return:
        """
        try:
            self.cusor.execute("""
                update teacher set {}=%s where Tno=%s;
            """.format(info_type), (info, Tno))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_update_teacher_Sno', message=e)
            return -1

    def sql_course_all_info(self):
        """
        select * from course
        :return:
        """
        try:
            self.cusor.execute("""
                select * from course;
            """)
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='sql_course_all_info', message=e)
            return -1

    def sql_course_Cno_info(self):
        """
        select Cno from course
        :return:
        """
        try:
            self.cusor.execute("""
                select Cno from course;
            """)
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='sql_course_Cno_info', message=e)
            return -1

    def sql_insert_sc(self, Sno, Cno, grade):
        """
        insert into sc;
        :param Sno:
        :param Cno:
        :param grade:
        :return:
        """
        try:
            if len(grade) == 0:
                self.cusor.execute("""
                    insert into sc(Sno,Cno) values(%s,%s);
                """, (Sno, Cno))
            else:
                self.cusor.execute("""
                    insert into sc values(%s,%s,%s);
                """, (Sno, Cno, grade))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_insert_sc', message=e)
            return -1

    def sql_check_select_Class_Cname(self, Class, Cno):
        """
        检查该班级中是否有学生已选择相同的课程
        :return:
        """
        try:
            self.cusor.execute("""
           select student.Sno, Sname, course.Cno, Cname
            from student,sc,course
            where student.Sno=sc.Sno and course.Cno=sc.Cno and Sclass=%s and course.Cno in
            (
                /*与Cno相同的Cname的Cno*/
                select Cno from course
                where Cname in
                (
                    select Cname from course where Cno=%s
                )
            );
            """, (Class, Cno))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='sql_check_select_Class_Cname', message=e)
            return -1

    def sql_insert_sc_by_Class(self, Sclass, Cno):
        """
        insert into sc where Sclass=%s;
        :param Sclass:
        :param Cno:
        :return:
        """
        try:
            self.cusor.execute("""
                insert into sc(Sno, Cno)
                select Sno,%s from student where Sclass=%s;
            """, (Cno, Sclass))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_insert_sc_by_Class', message=e)
            return -1

    def sql_select_sc_by_Sno_Cno(self, Sno, Cno):
        """
        select * from sc where Sno,Cno
        :param Sno:
        :param Cno:
        :return:
        """
        try:
            self.cusor.execute("""
                select * from sc where Sno=%s and Cno=%s;
            """, (Sno, Cno))
            sql_res = self.cusor.fetchall()
            return sql_res
        except Exception as e:
            messagebox.showerror(title='sql_select_sc_by_Sno_Cno', message=e)
            return -1

    def sql_delete_sc_by_Sno_Cno(self, Sno, Cno):
        """
        delete from sc where Sno,Cno
        :param Sno:
        :param Cno:
        :return:
        """
        try:
            self.cusor.execute("""
                delete from sc where Sno=%s and Cno=%s;
            """, (Sno, Cno))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_delete_sc_by_Sno_Cno', message=e)
            return -1

    def sql_delete_sc_by_Sclass_Cno(self, Sclass, Cno):
        """
        delete from sc where Sclass,Sno
        :param Sclass:
        :param Cno:
        :return:
        """
        try:
            self.cusor.execute("""
                delete from sc where Sno in 
                (
                    select Sno from student where Sclass=%s
                ) and Cno=%s
            """, (Sclass, Cno))
            self.con.commit()
            return 1
        except Exception as e:
            messagebox.showerror(title='sql_delete_sc_by_Sclass_Cno', message=e)
            return -1

