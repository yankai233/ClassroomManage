use crdb;
insert into admin
values ('1', 'admin', '123456');

insert into classroom
values ('1', '明理101', 10);

insert into course
values ('1', 'math', TRUE);

insert into teacher
values ('1', 'ls', 't1', '123456');

insert into student
values ('1', 'zs', '3班', 's1', '123456');

insert into sc
values ('1', '1', 10);

insert into student_borrow
values ('1', '1', '开会', '2021-01-10 10:20:10', '2021-01-10 10:30:20');

insert into teacher_borrow
values ('1', '1', '1', '2021-10-01 10:20:10', '2021-01-10 12:50:10');


delete from student_borrow where start='2021-01-10 10:20:10';


