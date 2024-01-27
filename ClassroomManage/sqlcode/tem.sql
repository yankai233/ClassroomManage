select x.*
from classroom x
where x.Classroom_id in
(
    /*时间不冲突*/
    select teacher_borrow.Classroom_id from teacher_borrow, student_borrow
    where '2023-09-05 0:00:00' not between teacher_borrow.start and teacher_borrow.end and
    '2023-09-05 2:00:00' not between teacher_borrow.start and teacher_borrow.end and
    '2023-09-05 0:00:00' not between student_borrow.start and student_borrow.end and
    '2023-09-05 2:00:00' not between student_borrow.start and student_borrow.end and
    teacher_borrow.start not between'2023-09-05 0:00:00' and '2023-09-05 2:00:00' and
                    teacher_borrow.end not between '2023-09-05 0:00:00' and '2023-09-05 2:00:00' and
                    student_borrow.start not between '2023-09-05 0:00:00' and '2023-09-05 2:00:00' and
                    student_borrow.end not between '2023-09-05 0:00:00' and '2023-09-05 2:00:00'
);

select * from mysql.user;


use crdb;
select student.Sno, Sname, course.Cno, Cname
    from student,sc,course
    where student.Sno=sc.Sno and course.Cno=sc.Cno and Sclass='3班' and course.Cno in
    (
        /*与Cno相同的Cname的Cno*/
        select Cno from course
        where Cname in
        (
            select Cname from course where Cno='1'
        )
    );

insert into sc(Sno, Cno)  select Sno,'1' from student where Sclass='3班';