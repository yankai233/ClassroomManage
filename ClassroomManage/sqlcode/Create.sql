create database crdb;
use crdb;
/*学生表*/
create table student(
    Sno char(10),
    Sname char(10),
    Sclass char(10),
    username char(10),
    password char(10),
    primary key (Sno)
);
/*老师表*/
create table teacher(
    Tno char(10),
    Tname char(10),
    username char(10),
    password char(10),
    primary key (Tno)
);
/*课程表*/
create table course(
    Cno char(10),
    Cname char(10),
    selectClass boolean,
    primary key (Cno)
);

/*教室*/
create table classroom(
    Classroom_id char(10),
    address char(10),
    size int(8) check ( size between 0 and 300),
    primary key (Classroom_id)
);
/*admin*/
create table admin(
    Ano char(10),
    username char(10),
    password char(10),
    primary key (Ano)
);

create table student_borrow(
    Sno char(10),
    Classroom_id char(10),
    use_to char(10),
    start datetime,
    end datetime,
    primary key (Sno, Classroom_id, start, end),
    foreign key (Sno) references student(Sno),
    foreign key (Classroom_id) references classroom(Classroom_id)
);

create table teacher_borrow(
    Tno char(10),
    Classroom_id char(10),
    Cno char(10),
    start datetime,
    end datetime,
    primary key (Tno, Classroom_id, Cno, start, end),
    foreign key (Tno) references teacher(Tno),
    foreign key (Classroom_id) references classroom(Classroom_id),
    foreign key (Cno) references course(Cno)
);

create table SC(
    Sno char(10),
    Cno char(10),
    grade int(8) check ( grade between 0 and 100),
    primary key (Sno, Cno),
    foreign key (Sno) references student(Sno),
    foreign key (Cno) references course(Cno)
);

/*视图*/
/*Sno,Sname,Cno,Cname,Tno,Tname,address,time*/
/*学生查看课表*/
create view SCS as
(
    select student.Sno, Sname,SC.Cno,Cname,teacher.Tno,Tname,address,start,end
    from student,course,SC,teacher_borrow,teacher,classroom
    where student.Sno=SC.Sno and SC.Cno=course.Cno and course.Cno=teacher_borrow.Cno and teacher.Tno=teacher_borrow.Tno and teacher_borrow.Classroom_id=classroom.Classroom_id
);
/*管理员查看学生课程*/
create view SCA as
(
    select student.Sno,Sname,Cname,Tname,grade
    from student,course,SC,teacher_borrow,teacher,classroom
    where student.Sno=SC.Sno and SC.Cno=course.Cno and course.Cno=teacher_borrow.Cno and teacher.Tno=teacher_borrow.Tno
);

/*老师情况*/
create view TSC as
(
    select teacher.Tno,Tname,course.Cno,Cname,start, end,address
    from teacher,classroom,course,teacher_borrow
    where teacher.Tno=teacher_borrow.Tno and course.Cno=teacher_borrow.Cno and classroom.Classroom_id=teacher_borrow.Classroom_id
);

# drop table student_borrow;
# drop table teacher_borrow;
# drop view TSC;
# drop view SCS;

# 修改student_borrow的主键
use crdb;
drop table student_borrow;
drop table teacher_borrow;