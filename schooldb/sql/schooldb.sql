drop database schooldb;
create database schooldb;

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE SCHEMA IF NOT EXISTS `schooldb` DEFAULT CHARACTER SET utf8 ;
USE `schooldb` ;


CREATE TABLE role (
    id char(1)not null,
    role_desc text(1000)not null,
    primary key (id)
);
CREATE TABLE users (
    id INT(10)AUTO_INCREMENT ,
    username varchar(30)not null,
	password varchar(30)not null,
    first_name varchar(20)not null,
    last_name varchar(20)not null,
    birthdate date,
    address varchar(100)not null,
    zip_code char(5)not null,
    role_id char(1)not null,
    curr_rnt int(1),
    PRIMARY KEY (id)  ,
    FOREIGN KEY (role_id) REFERENCES role(id) on update cascade,
    constraint check (curr_rnt>=0 and curr_rnt<=2)    
);

CREATE TABLE book (
    id INT(10)AUTO_INCREMENT,
    isbn char(20)not null,
    title varchar(30)not null,
	publisher varchar(50)not null,
    summary text(1000) not null,
    lang varchar(20)not null,
    pages SMALLINT(5)not null,
    coverurl varchar(100) default "C:\dbproject-main\images.png" ,
    primary key (id)
);

CREATE TABLE school (
    id INT(10)AUTO_INCREMENT,
    name varchar(50)not null,
	email varchar(30)not null,
    principal varchar(40)not null,
    librarian varchar(40)not null,
	city varchar(20)not null,   
    address varchar(60)not null,
    zip_code char(5)not null,
    phone char(30)not null,
    primary key (id)
);
CREATE TABLE schoolbook (
    school_id INT(10)not null,
    book_id INT(10)not null,
    curr_copies int(3)not null,
	tot_copies int(3)not null,
    primary key (school_id,book_id),
    foreign key (school_id) REFERENCES school(id) on update cascade ,
    FOREIGN KEY (book_id) REFERENCES book(id) on update cascade
);
CREATE TABLE schooluser (
    user_id INT(10)not null,
    school_id INT(10)not null,
	primary KEY (user_id,school_id),
    FOREIGN KEY (user_id) REFERENCES users(id) on update cascade,
	FOREIGN KEY (school_id) REFERENCES school(id) on update cascade
);
CREATE TABLE writer (
    id INT(10)AUTO_INCREMENT,
    name varchar(50)not null,
    PRIMARY KEY (id,name)
);
CREATE TABLE bwriter (
    book_id INT(10)not null,
    writer_id INT(10)not null,
    PRIMARY KEY (book_id,writer_id),
    FOREIGN KEY (book_id) REFERENCES book(id) on update cascade,
    FOREIGN KEY (writer_id) REFERENCES writer(id) on update cascade
);

CREATE TABLE category (
    id INT(10)AUTO_INCREMENT,
    name varchar(30)not null,
    PRIMARY KEY (id)
);
CREATE TABLE bookcat (
    book_id INT(10)not null,
    cat_id int(10)not null,
    PRIMARY KEY (book_id,cat_id),
    FOREIGN KEY (cat_id) REFERENCES category(id) on update cascade,
    FOREIGN KEY (book_id) REFERENCES book(id) on update cascade    
);

CREATE TABLE keyword (
    book_id INT(10)not null,
    word varchar(30)not null,
    PRIMARY KEY (book_id,word),
    FOREIGN KEY (book_id) REFERENCES book(id)
);
CREATE TABLE rental (
    user_id INT(10)not null,
    book_id INT(10)not null,
    trdate datetime default CURRENT_TIMESTAMP ,
    status char(1)not null,
    libr_id INT(10)default null,
    PRIMARY KEY (user_id,book_id,trdate),
    FOREIGN KEY (user_id) REFERENCES users(id) on update cascade,
    FOREIGN KEY (book_id) REFERENCES book(id) on update cascade,
    FOREIGN KEY (libr_id) REFERENCES users(id) on update cascade
    
    );
CREATE TABLE reservation (
    user_id INT(10)not null,
    book_id INT(10)not null,
    trdate datetime default CURRENT_TIMESTAMP ,
    status char(1)not null,
    PRIMARY KEY (user_id,book_id,trdate),
    FOREIGN KEY (user_id) REFERENCES users(id) on update cascade,
    FOREIGN KEY (book_id) REFERENCES book(id) on update cascade
    
    )  ;  
CREATE TABLE rating (
    user_id INT(10)not null,
    book_id INT(10)not null,
    trdate datetime default CURRENT_TIMESTAMP ,
    ratetext text(1000) ,
    likert tinyint(1) ,
    PRIMARY KEY (user_id,book_id),
    FOREIGN KEY (user_id) REFERENCES users(id) on update cascade,
    FOREIGN KEY (book_id) REFERENCES book(id) on update cascade
    
    );

delimiter $$



delimiter $$

'''create trigger delete_user
after delete on users
for each row
begin
	delete from schooluser where schooluser.user_id = old.user_id;
end $$
CONSTRAINT check  (exist(select r.trdate from rental as r where r.book_id = book_id and r.user_id = user_id ))

for each row
begin
	delete from rating where rating.user_id = old.user_id;
end $$'''

'''create trigger delete_book
after delete on book

for each row
begin
	delete from schoolbook where schoolbook.book_id = old.book_id;
end $$

for each row
begin
	delete from bwriter where bwriter.book_id = old.book_id;
end $$
'''
create trigger update_rental after update on rental 
begin
    if (new.status = 1)
    then
    update users 
        set curr_rnt = old.curr_rnt+1
        where id = new.user_id 
    END IF;
    if (new.status = 2)
    then 
    update users
        set curr_rnt = old.curr_rnt-1
        where id = new.user_id
    END IF;
END


create trigger update_reserv after update on rental 
begin
    if (new.status = 0) and (select schoolbook.curr_copies = 0 where schoolbook.book_id = rental.book_id)
    then
    insert into reservation (user_id,book_id,trdate) VALUES 
    ( new.user_id , new.book_id ,default , 0)
    END IF;
    if (new.status = 1) and exist(select trdate from reservation where user_id = new.user_id and book_id = new.book_id)
    then 
    update reservation as r
        set r.status = 1
        where r.user_id = old.user_id
    END IF;
END