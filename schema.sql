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
    role_id char(2)not null default '-1',
    curr_rnt int(1),
    PRIMARY KEY (id)  ,
    
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
    
create view q316 AS (select c.id as category ,r.book_id , r.trdate  from category as c
	join bookcat as bc on c.id = bc.cat_id
    join book as b on b.id = bc.book_id
    join rental as r on r.book_id = b.id );
    
create view  q317 as (select w.name as writer,count(w.name) as books_written from writer as w join 
	bwriter as bw on bw.writer_id = w.id
    group by w.name);
delimiter $$


CREATE UNIQUE INDEX idx_writer ON bwriter (book_id,writer_id);

CREATE UNIQUE INDEX idx_user ON users (first_name, last_name);

CREATE UNIQUE INDEX idx_school ON school (name);

CREATE UNIQUE INDEX idx_category ON bookcat (book_id,cat_id);

CREATE UNIQUE INDEX idx_keyword ON keyword (book_id,word);

CREATE UNIQUE INDEX idx_schooluser ON schooluser (school_id,user_id);

CREATE UNIQUE INDEX idx_schoolbook ON schoolbook (school_id,book_id);

   delimiter $$

CREATE DEFINER = CURRENT_USER TRIGGER schooldb.users_BEFORE_UPDATE BEFORE UPDATE ON users 
FOR EACH ROW
 
BEGIN
    
   IF role_id > 0 AND OLD.curr_rnt < 1 THEN          
      SET NEW.curr_rnt = 1;       
   ELSEIF role_id = 0 AND OLD.curr_rnt < 2 THEN          
      SET NEW.curr_rnt = OLD.curr_rnt + 1;          
   ELSE          
      SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Book limit reached';    
   END IF; 
END

;

delimiter $$

CREATE DEFINER = CURRENT_USER TRIGGER schooldb.schoolbook_BEFORE_UPDATE BEFORE UPDATE ON schoolbook
 FOR EACH ROW
BEGIN
      IF OLD.curr_copies = 0 THEN
          SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not available';
      ELSE
         SET NEW.curr_copies = OLD.curr_copies - 1;
      END IF
      ;
END;       
    
delimiter $$

CREATE DEFINER = CURRENT_USER TRIGGER schooldb.reservation_BEFORE_INSERT BEFORE INSERT ON reservation 
FOR EACH ROW
BEGIN

 IF  NEW.status = -1 THEN
         INSERT INTO users (curr_rnt) values ( curr_rnt - 1);
    ELSEIF  NEW.status = 1 THEN
        INSERT INTO users (curr_rnt) values ( curr_rnt + 1);    
    END IF     
         ;
END;


 delimiter $$

CREATE DEFINER = CURRENT_USER TRIGGER schooldb.rental_BEFORE_UPDATE BEFORE UPDATE ON rental 
FOR EACH ROW
BEGIN
 IF  NEW.status = 2 THEN
        INSERT INTO schoolbook (curr_copies) values ( curr_copies + 1);
        INSERT INTO users (curr_rnt) values ( curr_rnt - 1);
     END IF
         ;
END ;    