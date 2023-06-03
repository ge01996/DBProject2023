#3.1.1
select s.id as school_id,s.name as school_name,count(s.id) as rental_count
 from users  u join schooluser su on u.id = su.user_id 
        join school  s on s.id = su.school_id 
        join rental  r on r.user_id = u.id
        group by s.id ;
 
 #3.1.2.a       
select w.name as writer_name,c.name as category from writer w
	join bwriter on w.id = bwriter.writer_id
    join book as b on bwriter.book_id = b.id 
    join bookcat on bookcat.book_id = b.id
    join category as c on c.id = bookcat.cat_id
    where c.id = '2' ;
#3.1.2.b
select u.id as user_id, u.first_name , u.last_name ,u.role_id ,c.name as category
    from users as u join rental as r on u.id = r.user_id 
    join book as b on b.id = r.book_id 
    join bookcat on b.id = bookcat.book_id 
    join category as c on c.id = bookcat.cat_id
    where c.id = '2' and  u.role_id = '0' and r.trdate like '2023%';    
 
#3.1.3
select u.id as user_id, u.first_name , u.last_name, 
    u.role_id, u.birthdate, count(u.id) as rental_count
    from users as u 
    join rental as r on r.user_id = u.id 
    where u.birthdate >= '1983-01-01' and u.role_id = '1' 
    group by u.id ; #limit = 
  
#3.1.4
select w.name as writer_name from writer as w
     where w.name not in 
     (select w.name as writer_name from writer as w 
     join bwriter as bw on bw.writer_id = w.id
     join book as b on b.id = bw.book_id 
     join rental as r on b.id = r.book_id )
	 order by w.name; 
     
#select book.title from book join bookcat on bookcat.book_id = book.id join bwriter on bwriter.book_id = book.id join writer on bwriter.writer_id = writer.id where writer.name ='Jennifer West';

#3.1.5
#select l.id as librarian_id,l.first_name,l.last_name,cnt(l.id) as rental_count 
#from users as l join rental as r 
#where r.libr_id = l.id and r.trdate like '2022%' and rental_count >19 group by rental_count ;


select s.librarian ,count(r.trdate) from users as u 
	join schooluser as su on su.user_id = u.id
    join school as s on s.id = su.school_id 
	join rental as r on r.user_id = u.id
    join book as b on r.book_id = b.id
    group by s.librarian;
    
#select book.title ,rental.user_id, rental.trdate from book join rental on book.id = rental.book_id
#select school.id from school join schooluser on school.id = schooluser.school_id join users on schooluser.user_id=users.id where users.id 

#3.1.6
create view q316 AS (select c.id as category ,r.book_id , r.trdate  from category as c
	join bookcat as bc on c.id = bc.cat_id
    join book as b on b.id = bc.book_id
    join rental as r on r.book_id = b.id );
    
select c1.category as category_1 ,c2.category as category_2 ,count(c1.book_id) as rental_num from q316 c1 join
	q316 c2 on c1.book_id = c2.book_id
    where c1.category > c2.category
    group by c1.category,c2.category
    order by rental_num desc
    limit 3;
    
#select c1.category,c2.category,c1.book_id,c1.trdate from q316 c1 join
	#q316 c2 on c1.book_id = c2.book_id
    #where c1.category > c2.category

#3.1.7

create view  q317 as (select w.name as writer,count(w.name) as books_written from writer as w join 
	bwriter as bw on bw.writer_id = w.id
    group by w.name);
    
select w.writer,w.books_written from q317 w 
    where w.books_written <(select count(w.name) as books_written from writer as w join 
	bwriter as bw on bw.writer_id = w.id
    group by w.name order by count(w.name) desc limit 1)-5
    order by books_written;
    
    
#3.2.1
select  b.title,c.name  from school as s 
	join schoolbook as sb on sb.school_id = s.id
	join book as b on b.id = sb.book_id
    join bookcat as bc on bc.book_id = b.id
    join category as c on c.id = bc.cat_id
    join bwriter as bw on bw.book_id = b.id
    join writer as w on w.id = bw.writer_id
    #where s.id = and b.title = and c.name = and sb.curr_copies = and w.name =
    ;
    
    
#3.2.2
select u.id as user_id,u.first_name,u.last_name,b.title as book_title,r.trdate as rental_date from
		users as u join rental as r on r.user_id = u.id 
        join book as b on b.id = r.book_id 
        where r.trdate > current_date() - (0000-00-14) and r.status = 1;
        
#3.2.3a
select u.id,u.username,avg(r.likert) from users as u 
	join rating as r on u.id = r.user_id 
    join schooluser as su on su.user_id = u.id
    
    where su.school_id = '1'
    group by u.id
    
    ;
#3.2.3b
select avg(r.likert) from category as c
	join bookcat as bc on bc.cat_id = c.id
    join rating as r on r.book_id = bc.book_id
    where c.name = 'Novel';
    
#3.3.1
select b.title from users as u 
	join schooluser as su on su.user_id = u.id
	#join school as s on su.school_id = s.id
    join schoolbook as sb on sb.school_id = su.school_id
    join book as b on b.id = sb.book_id 
    join bookcat as bc on bc.book_id = b.id
    join category as c on c.id = bc.cat_id
    join bwriter as bw on bw.book_id = b.id
    join writer as w on w.id = bw.writer_id
    #where u.id = and b.title = and w.name = and c.name = 
    ;
#3.3.2    
select  b.title from users as u 
	join rental as r on r.user_id = u.id
    join book as b on b.id = r.book_id
    where u.username ='gpayne' 
    ;
select u.username ,u.password from users as u where u.role_id ='0' and exists(select * from rental as r where r.user_id = u.id)