# admin
create user 'admin'@'localhost' identified by '123456';
grant all privileges on *.* to 'admin'@'localhost';
flush privileges ;

# student
create user 'student'@'localhost' identified by '123456';
grant all privileges on crdb.* to 'student'@'localhost';
flush privileges ;

# teacher
create user 'teacher'@'localhost' identified by '123456';
grant all privileges on *.* to 'teacher'@'localhost';
flush privileges ;

select * from mysql.user;