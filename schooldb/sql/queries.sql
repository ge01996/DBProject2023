/*admin*/
select * from rental 
    join school on school_id = select school_id from schooluser where schooluser_user_id = rental_user_id
    where trdate = '' group by rental_school_id ;

select s.id as school_id,s.name as school_name,u.id as user_id,u.first_name,.u.last_name,r.book_id,
r.trdate 
 from users  u join schooluser su on u.id = su.user_id 
        join school  s on s.id = su.school_id 
        join rental  r on r.user_id = u.id;
/*3.1.1*/
select s.id as school_id,s.name as school_name,count(s.id) as rental_count
 from users  u join schooluser su on u.id = su.user_id 
        join school  s on s.id = su.school_id 
        join rental  r on r.user_id = u.id
        group by s.id ;

/*3.1.2*/
select w.name as writer_name,c.name as category_id from writer w
    join book as b on w.book_id = b.id 
    join category as c on c.book_id = b.id
    where c.name = '2' ;

select u.id as user_id, u.first_name , u.last_name ,u.role_id ,b.title ,r.trdate as rental_date 
    from users as u join rental as r on u.id = r.user_id 
    join book as b on b.id = r.book_id 
    join category as c on b.id = c.book_id 
    where c.name = '2' and u.role_id = '1' and r.trdate like '2022%';

/*3.1.3*/
select u.id as user_id, u.first_name , u.last_name, 
    u.role_id, u.birthdate, count(u.id) as rental_count
    from users as u 
    join rental as r on r.user_id = u.id 
    where u.birthdate >= '1983-01-01' and u.role_id = '1' 
    group by u.id  
    /* limit =  */ ;

/*3.1.4*/
select w.name as writer_name from writer as w
     where w.name not in 
     (select w.name as writer_name from writer as w 
    join book as b on b.id = w.book_id 
    join rental as r on b.id = r.book_id )
    order by w.name; 
    
/*3.1.5*/
select l.id as librarian_id,l.first_name,l.last_name,cnt(l.id) as rental_count from users as l join rental as r where r.libr_id = l.id and r.trdate like '2022%' and rental_count >19 group by rental_count 
/*3.1.6*/
select count() as rental_per_category , c.name as category_1 from 
    book as b 
    join category as c on c.book_id = b.id where c.name = '1' 
    
    join select c1.name as category_2 from category as c1 
    join book as b on c1.book_id = b.id where c1.name ='2'
    join rental as r on r.book_id = b.id  
/*3.1.7*/





select name from users 
    join rental on users_id = rental_user_id 
    join category on category_book_id = rental_book_id where category_name = ''
    where users_role_id = 1;
    

/*librarian*/
/*3.2.1*/
select  b.title,w.name as writer from users as u 
    join schooluser as su on u.id = su.user_id 
    join school as s on s.id = su.school_id
    join schoolbook as sb on sb.school_id = s.id
    join book as b on b.id = sb.book_id 
    join category as c on c.book_id = b.id
    join writer as w on w.book_id = b.id
    where u.username = 'qwelch' and c.name = '' and w.name = '' and sb.copies > ;
/*3.2.2*/
select u.username , u.first_name, u.last_name from users as u 
    join rental as r on r.user_id = u.id 
    where r.flag = 1 and now - r.trdate > 0000-00-14 ;
/*3.2.3*/
/*user*/
/*3.3.1*/
select distinct b.title,s.name as school_name,sb.copies as copies from users as u 
    join schooluser as su on u.id = su.user_id 
    join school as s on s.id = su.school_id
    join schoolbook as sb on sb.school_id = s.id
    join book as b on sb.book_id = b.id
    join category as c on c.book_id = b.id
    join writer as w on w.book_id = b.id
    where u.username = 'qwelch',  and c.name = '' and w.name = '';

/*3.3.2*/
select  b.title,r.trdate as rental_date from users as u 
    join rental as r on r.user_id = u.id
    join book as b on b.id = r.book_id
    where u.username = 'qwelch' ;
    
3.1.5.Ποιοι χειριστές έχουν δανείσει τον ίδιο αριθμό βιβλίων σε διάστημα ενός έτους με
περισσότερους από 20 δανεισμούς;
3.1.6.Πολλά βιβλία καλύπτουν περισσότερες από μια κατηγορίες. Ανάμεσα σε ζεύγη πεδίων (π.χ.
ιστορία και ποίηση) που είναι κοινά στα βιβλία, βρείτε τα 3 κορυφαία (top-3) ζεύγη που
εμφανίστηκαν σε δανεισμούς.
3.1.7.βρείτε όλους τους συγγραφείς που έχουν γράψει τουλάχιστον 5 βιβλία λιγότερα από τον
συγγραφέα με τα περισσότερα βιβλία.
3.2. (Χειριστής) (15% - τα ερωτήματα είναι ισόβαθμα):
3.2.1.Παρουσίαση όλων των βιβλίων κατά Τίτλο, Συγγραφέα (Κριτήρια αναζήτησης: τίτλος/
κατηγορία/ συγγραφέας/ αντίτυπα).
3.2.2.Εύρεση όλων των δανειζόμενων που έχουν στην κατοχή τους τουλάχιστον ένα βιβλίο και
έχουν καθυστερήσει την επιστροφή του. (Κριτήρια αναζήτησης: Όνομα, Επώνυμο, Ημέρες
Καθυστέρησης).
3.2.3.Μέσος Όρος Αξιολογήσεων ανά δανειζόμενο και κατηγορία (Κριτήρια αναζήτησης:
χρήστης/ κατηγορία)
3.3. (Χρήστης) (10%)
3.3.1.Όλα τα βιβλία που έχουν καταχωριστεί (Κριτήρια αναζήτησης: τίτλος/ κατηγορία/
συγγραφέας), δυνατότητα επιλογής βιβλίου και δημιουργία αιτήματος κράτησης.
3.3.2.Λίστα όλων των βιβλίων που έχει δανειστεί ο συγκεκριμένος χρήστης.