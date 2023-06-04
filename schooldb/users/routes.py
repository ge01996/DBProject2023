from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldb import db ## initially created by __init__.py, need to be used here
from schooldb.users.forms import UserForm,passform,form331,formid2,formbid,formbreview,formresdel,formid,formubid,formid3,formubid2,formubid3,formbid2,formbid3
from schooldb.users import users



@users.route("/users/create", methods = ["GET", "POST"]) ## "GET" by default
def createUser():
    """
    Create new user in the database
    """
    form = UserForm() 
   
    if(request.method == "POST" and form.validate_on_submit()):
        newUser = form.__dict__
        query = "INSERT INTO users(id,username,password,first_name, last_name,birthdate,address,zip_code,role_id,curr_rnt) VALUES (default,'{}', '{}', '{}','{}','{}', '{}', '{}' , '-1' , 0 );".format(newUser['username'].data,newUser['password'].data,newUser['first_name'].data, newUser['last_name'].data,newUser['birthdate'].data,newUser['address'].data,newUser['zip_code'].data )
        
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        
        flash("User inserted successfully", "success")
        
        query = "INSERT INTO schooluser(user_id,school_id) VALUES ((select id from users where username ='{}'),(select id from school where name = '{}'));".format(newUser['username'].data,newUser['school'].data)
       
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("School-User relation inserted successfully", "success")
        return redirect(url_for("index"))
        

    ## else, response for GET request
    return render_template("create_user.html", pageTitle = "Create User", form = form)

@users.route("/users/createlib", methods = ["GET", "POST"]) ## "GET" by default
def createUserl():
    """
    Create new user in the database
    """
    form = UserForm() 
   
    if(request.method == "POST" and form.validate_on_submit()):
        newUser = form.__dict__
        query = "INSERT INTO users(id,username,password,first_name, last_name,birthdate,address,zip_code,role_id,curr_rnt) VALUES (default,'{}', '{}','{}', '{}','{}', '{}', '{}' , '-2' , 0 );".format(newUser['username'].data,newUser['password'].data,newUser['first_name'].data, newUser['last_name'].data,newUser['birthdate'].data,newUser['address'].data,newUser['zip_code'].data )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("User inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
        query = "INSERT INTO schooluser(user_id,school_id) VALUES ((select id from users where username ='{}'),(select id from school where name = '{}'));".format(newUser['username'].data,newUser['school'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("School-User relation inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_user.html", pageTitle = "Create Librarian", form = form)

@users.route("/users/update/<int:id>", methods = ["POST"])
def updateUser(id):
    """
    Update a user in the database, by id
    """
    form = UserForm() ## see createUser for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE users SET  last_name = '{}', address = '{}' WHERE id = {};".format(updateData['last_name'].data, updateData['address'].data, id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("User updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("user.getUser"))

@users.route("/users/delete/<int:id>", methods = ["POST"])
def deleteUser(id):
    """
    Delete user by id from database
    """
    query = f"DELETE FROM users WHERE id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("User deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("user.getUser"))


@users.route("/users/admin/backup",methods=[ 'GET','POST'])
def adminbackup():
  query = "SELECT * INTO OUTFILE 'C:\backup.txt' FROM book,users,school,schooluser,schoolbook,category,bookcat,writer,bwriter,keyword,rental,reservation,rating;"
  cur = db.connection.cursor()
  cur.execute(query)
  db.connection.commit()
  cur.close()
  flash("Backup file created successfully", "primary")


@users.route("/users/admin/restore",methods=['POST'])
def adminrestore():
  query = "SELECT * LOAD_FILE('C:\\backup.txt')"
  cur = db.connection.cursor()
  cur.execute(query)
  db.connection.commit()
  cur.close()
  flash("Restore was successfull", "primary")
  
@users.route("/users/admin/librarianactivation",methods=['GET','POST'])
def adminlibrarianactivation():
  query = "SELECT u.id,u.username,u.first_name,u.last_name from users as u where u.role_id = '-2' ;"
  cur = db.connection.cursor()
  cur.execute(query)
  db.connection.commit()
  column_names = [i[0] for i in cur.description]
  res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

  form = formid()
  dummy = form.__dict__
  id = dummy['id'].data
  if id :
     query = "UPDATE users SET role_id = '2' where id = '{}' ".format(id)
     cur.execute(query)
     db.connection.commit()

  cur.close()
  flash("Activation was successfull", "primary")
  return render_template("adminlibrarian.html",res = res,form = form)
   
    
    

@users.route("/q311",methods=['POST'])
def get311():
    '''
    get list of total number of rentals per school from database
    '''
    year = request.form.get('year')
    month = request.form.get('month')
    #print(month)
    if year :
        date = year
        if month:
            date+= month 
    elif month:
         date = '%'+month
    
    
    query = "select s.id as school_id,s.name as school_name,count(s.id) as rental_count from users  u join schooluser su on u.id = su.user_id   join school s on s.id = su.school_id   join rental r on r.user_id = u.id "
    if year or month :
        date+='%'
        query+= " where r.trdate like '{}'".format(date)
    query+= " group by s.id order by s.id;"
    cur = db.connection.cursor()
    cur.execute(query)
    db.connection.commit()
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    flash("List was created successfully", "success")
    return render_template("adminq1.html",pageTitle = "Total rentals per school",school = res)
 

@users.route("/q312",methods=['GET', 'POST'])
def get312():

    category = request.form.get('category')
    #print(category)
    query = "select w.name as writer_name,c.name as category from writer w join bwriter on w.id = bwriter.writer_id join book as b on bwriter.book_id = b.id  join bookcat on bookcat.book_id = b.id  join category as c on c.id = bookcat.cat_id  where c.id = '{}' ;".format(category)
    cur = db.connection.cursor()
    cur.execute(query)
    db.connection.commit()
    column_names = [i[0] for i in cur.description]
    res1 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    
    query = "select u.id as user_id, u.first_name , u.last_name ,u.role_id from users as u join rental as r on u.id = r.user_id  join book as b on b.id = r.book_id join bookcat as bc on bc.book_id = b.id join category as c on c.id = bc.cat_id  where c.id = '{}' and u.role_id = '1' and r.trdate like '2022%';".format(category)
    cur.execute(query)
    db.connection.commit()
    column_names = [i[0] for i in cur.description]
    res2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
      
    return render_template("adminq2.html",pageTitle = "Writers of requested category & Teachers that borrowed a book belonging there",writer = res1,user = res2)

@users.route("/q313",methods=['GET', 'POST'])
def get313():
  

  query = "select u.id as user_id, u.first_name , u.last_name, u.role_id, u.birthdate, count(u.id) as rental_count from users as u join rental as r on r.user_id = u.id where u.birthdate >= '1983-01-01' and (u.role_id = '1' or u.role_id = '2') group by u.id "
  cur = db.connection.cursor()
  cur.execute(query)
  db.connection.commit()
  column_names = [i[0] for i in cur.description]
  res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
  cur.close()        
  
  return render_template("adminq3.html",pageTitle = "Young(under 40 y.o.) teachers have borrowed the most books",user = res)

@users.route("/q314",methods=['GET', 'POST'])
def get314():
  query ="select w.name as writer_name from writer as w where w.name not in (select w.name as writer_name from writer as w join bwriter as bw on bw.writer_id = w.id join book as b on b.id = bw.book_id join rental as r on b.id = r.book_id ) order by w.name;  "
  cur = db.connection.cursor()
  cur.execute(query)
  db.connection.commit()
  column_names = [i[0] for i in cur.description]
  res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
  cur.close() 

  return render_template("adminq4.html",pageTitle = "Writer without a borrowed book :( ",writer = res)
    

@users.route("/q315",methods=['GET', 'POST'])
def get315():
    query ="select s.librarian ,count(r.trdate) as rentals from users as u join schooluser as su on su.user_id = u.id join school as s on s.id = su.school_id 	join rental as r on r.user_id = u.id  join book as b on r.book_id = b.id  group by s.librarian;"
    cur = db.connection.cursor()
    cur.execute(query)
    db.connection.commit()
    column_names = [i[0] for i in cur.description]
    res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
    cur.close()
    return render_template("adminq5.html",pageTitle = "Librarian with over 20 loanings",school = res)

@users.route("/q317",methods=['GET', 'POST'])
def get317():
 
 query ="select w.writer,w.books_written from q317 w where w.books_written <(select count(w.name) as books_written from writer as w join bwriter as bw on bw.writer_id = w.id  group by w.name order by count(w.name) desc limit 1)-5  order by books_written; "
 cur = db.connection.cursor()
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 cur.close()
 return render_template("adminq7.html",pageTitle = "Writers with at least 5 less books than the writer with the most books",writer = res)

@users.route("/q316",methods=['GET', 'POST'])
def get316():
 
 query ="select c1.category as category_1 ,c2.category as category_2 ,count(c1.book_id) as rental_num from q316 c1 join	q316 c2 on c1.book_id = c2.book_id where c1.category > c2.category group by c1.category,c2.category  order by rental_num desc limit 3;"
 cur = db.connection.cursor()
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 
 cur.close()

 return render_template("adminq6.html",pageTitle = "Top 3 category pairs",category = res)

@users.route("/q321/<username>",methods=[ 'GET','POST'])
def get321(username):

 fwriter = request.form.get('fwriter')
 ftitle = request.form.get('ftitle')
 category = request.form.get('category')
 title = request.form.get('title')
 writer = request.form.get('writer')
 copies = request.form.get('copies')
 query ="select s.id from school as s join schooluser as su on su.school_id = s.id join users as u on u.username ='{}'".format(username)
 cur = db.connection.cursor()
 cur.execute(query)
 db.connection.commit()
 data = cur.fetchone()
 school = data[0]
 query ="select  b.title from school as s join schoolbook as sb on sb.school_id = s.id join book as b on b.id = sb.book_id   "
 
 if writer:
    query+= " join bwriter as bw on bw.book_id = sb.book_id join writer as w on w.id = bw.writer_id "
 if category:
    query+= " join bookcat as bc on bc.book_id = sb.book_id join category as c on c.id= bc.cat_id "
 if school :
    query+="where s.id ='{}' ".format(school)
 if category:
    query+= "and c.name = '{}' ".format(category)
 if title:
    query+= "and b.title like '{}' ".format(title)
 if writer:
    query+= "and w.name like '{}' ".format(writer)
 if copies:
    query+= "and sb.curr_copies = '{}' ".format(copies)
 if fwriter:
    query+= "order by w.name "
 if ftitle:
    query+= "order by b.title "

 #print('username:',username,'writerfilter',fwriter,'titlefilter',ftitle,'category',category,'title',title,'writer',writer,'copies',copies,query)
 
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 cur.close()

 return render_template("librarianq1.html",pageTitle = "Books of your School",data = res)

@users.route("/q322/<username>",methods=['GET','POST'])
def get322(username):
 
 first_name = request.form.get('first_name')
 last_name = request.form.get('last_name')
 days = request.form.get('days')
 query ="select s.id from school as s join schooluser as su on su.school_id = s.id join users as u on u.username ='{}'".format(username)
 cur = db.connection.cursor()
 cur.execute(query)
 db.connection.commit()
 data = cur.fetchone()
 school = data[0]
 query ="select u.id as user_id,u.first_name,u.last_name,b.title as book_title,r.trdate as rental_date from users as u join rental as r on r.user_id = u.id join book as b on b.id = r.book_id  join schooluser as su on su.user_id = u.id where su.school_id ='{}' and  r.status = 1 ".format(school)
 if first_name:
    query+= "and u.first_name like '{}'".format(first_name)
 if last_name:
    query+= "and u.last_name like '{}'".format(last_name)
 if days:
    if days >'10': days = '0'+days
    query+= "and r.trdate > current_date() - (0000-00-'{}')".format(days)
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 cur.close()

 return render_template("librarianq2.html",pageTitle = "Users with books past their return date",data = res)

@users.route("/q323/<username>",methods=['POST'])
def get323(username ):
 user = request.form.get('username')
 category = request.form.get('category')
 query ="select s.id from school as s join schooluser as su on su.school_id = s.id join users as u on u.username ='{}'".format(username)
 cur = db.connection.cursor()
 cur.execute(query)
 db.connection.commit()
 data = cur.fetchone()
 school = data[0]
 query ="select u.id,u.username ,avg(r.likert) as average_rating from users as u join rating as r on u.id = r.user_id join schooluser as su on su.user_id = u.id where su.school_id ='{}' ".format(school)
 if user :
    query+= " and u.username = '{}'".format(user)
 query+= " group by u.id ;" 
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res1 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 query = "select c.name,avg(r.likert) as average_rating from category as c join bookcat as bc on bc.cat_id = c.id  join rating as r on r.book_id = bc.book_id join schoolbook as sb on sb.book_id = bc.book_id where sb.school_id = '{}' ".format(school)
 if category:
    query+= "and c.name = '{}'".format(category)
 query+= " group by c.id ;"
 
 cur.execute(query)
 column_names = [i[0] for i in cur.description]
 res2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 cur.close()
 #print(username,user,category,school,'\n',res1,'\n',res2)
 return render_template("librarianq3.html",pageTitle = "Average ratings",data1 = res1,data2 = res2)

@users.route("/users")
def getUser():
    try:
        form = UserForm()
        newUser = form.__dict__
        cur = db.connection.cursor()
        query = "SELECT * FROM users where username = '{}';".format(username)
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        users = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("user.html", users = users, pageTitle = "Users Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@users.route("/users/services/<username>/<role>",methods=['GET', 'POST'])
def services(username,role):
 form = UserForm()
 cur = db.connection.cursor()
 #get user data
 query = "SELECT u.id,u.first_name,u.last_name,u.username,u.birthdate,u.address,u.zip_code FROM users as u where username = '{}';".format(username)
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 user = [dict(zip(column_names, entry)) for entry in cur.fetchall()]

 form2= form331()
 formborrowbook = formbid()
 formreservebook = formbid2()
 formreview = formbreview()
 formreviewsee = formbid3()
 criteria = form2.__dict__
 #get the titles of the books in user's school
 query = "select distinct b.title from users as u join schooluser as su on su.user_id = u.id join schoolbook as sb on su.school_id = sb.school_id  join book as b on b.id = sb.book_id join bookcat as bc on bc.book_id = b.id join category as c on c.id = bc.cat_id join bwriter as bw on bw.book_id = b.id join writer as w on w.id = bw.writer_id where u.username ='{}'".format(username)
 if(request.method == "POST" and form2.validate_on_submit()):
    title = criteria['title'].data
    category = criteria['category'].data
    writer = criteria['writer'].data
    if title:
      query+=" and b.title like '{}'".format(title)
    if category:
      query+=" and c.name = '{}'".format(category)
    if writer:
      query+=" and w.name = '{}'".format(writer)
    
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 book = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 #get the titles of the books the user has borrowed in the past
 query = "select b.title ,r.trdate as rental_date from users as u join rental as r on r.user_id = u.id join book as b on b.id = r.book_id where u.username ='{}' ".format(username) 
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 book2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 dummy1 = formborrowbook.__dict__
 title = dummy1['title'].data
 #print(title)
 if title:
    query = "Select u.id from users as u where u.username ='{}'".format(username)
    cur.execute(query)
    db.connection.commit()
    data1 =cur.fetchone()   
    id = data1[0]
    query = "Select b.id from book as b where b.title ='{}'".format(title)
    cur.execute(query)
    db.connection.commit()
    data2 =cur.fetchone()  
    bid = data2[0]
    #insert the rental into the table, but with status 0, so the librarian has to  confirm it 
    query = "INSERT into rental (user_id,book_id,trdate,status,libr_id) VALUES ('{}', '{}',default,0,default); ".format(id,bid)
    cur.execute(query)
    db.connection.commit()
 dummy2 = formreservebook.__dict__
 title2 = dummy2['title2'].data

 if title2:
    query = "Select u.id from users as u where u.username ='{}'".format(username)
    cur.execute(query)
    db.connection.commit()
    data1 =cur.fetchone()   
    id = data1[0]
    query = "Select b.id from book as b where b.title ='{}'".format(title2)
    cur.execute(query)
    db.connection.commit()
    data2 =cur.fetchone()  
    bid = data2[0]
    #insert the reservation , same as rental, in case the aren't any available copies
    query = "INSERT into reservation (user_id,book_id,trdate,status) VALUES ('{}', '{}',default,0); ".format(id,bid)
    cur.execute(query)
    db.connection.commit()

 dummy3 = formreview.__dict__
 title3 = dummy3['title'].data
 text = dummy3['text'].data
 rating = dummy3['rating'].data
 if title3 and rating and text :
    query = "Select u.id from users as u where u.username ='{}'".format(username)
    cur.execute(query)
    db.connection.commit()
    data1 =cur.fetchone()   
    id = data1[0]
    query = "Select b.id from book as b where b.title ='{}'".format(title3)
    cur.execute(query)
    db.connection.commit()
    data2 =cur.fetchone()  
    bid = data2[0]
    #insert review
    query = "INSERT into review (user_id,book_id,trdate,status,libr_id) VALUES ('{}', '{}',default,0,default); ".format(id,bid)
    cur.execute(query)
    db.connection.commit()

 dummy4 = formreviewsee.__dict__
 title4 = dummy4['title3'].data
 review = ''
 if title4:
    query = "Select u.id from users as u where u.username ='{}'".format(username)
    cur.execute(query)
    db.connection.commit()
    data1 =cur.fetchone()   
    id = data1[0]
    query = "Select b.id from book as b where b.title ='{}'".format(title4)
    cur.execute(query)
    db.connection.commit()
    data2 =cur.fetchone()  
    bid = data2[0]
    #get users review of a specific book to show it to him
    query = "Select r.ratetext from rating as r where r.user_id ='{}' and r.book_id= '{}' ; ".format(id,bid)
    cur.execute(query)
    db.connection.commit()
    data3 =cur.fetchone() 
    if data3: 
        review = data3[0]
    
    #print (title4)
 #change password
 formpass = passform()
 dummy5 = formpass.__dict__
 newpass = dummy5['pass1'].data
 
 if newpass:
    query ="UPDATE users SET password = '{}' where username ='{}' ; ".format(newpass,username)
    cur.execute(query)
    db.connection.commit()

 #get user's reservations
 query = "select b.title ,r.trdate  from users as u join reservation as r on r.user_id = u.id join book as b on b.id = r.book_id where u.username ='{}' and r.status ='0' ".format(username) 
 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 
 #delete a reservation
 formresdelete = formresdel()
 dummy6 = formresdelete.__dict__
 restitle = dummy6['title'].data
 resdate = dummy6['date'].data
 if restitle and resdate:
    query = "SELECT id from book where title ='{}' ; ".format(restitle)
   
    cur.execute(query)
    db.connection.commit()
    data4 =cur.fetchone() 
    resid = data4[0]
    #print(resid)
    query = "DELETE from reservation where book_id ='{}'  and trdate='{}' ;".format(resid,resdate)
    cur.execute(query)
    db.connection.commit()
 cur.close()     
 return render_template("user.html",pageTitle = "User Profile and Services",user = user,form=form,form2 = form2,book=book,book2=book2,data3=review,formborrowbook = formborrowbook ,formreservebook = formreservebook ,formrev = formreview ,formreviewsee = formreviewsee,formpass = formpass,res=res,formresdelete = formresdelete)  
    



@users.route("/q332/<username>",methods=['POST'])
def get332(username ):
 
 cur = db.connection.cursor()

 query ="select  b.title from users as u join rental as r on r.user_id = u.id join book as b on b.id = r.book_id where u.username = '{}' ".format(username)


 cur.execute(query)
 db.connection.commit()
 column_names = [i[0] for i in cur.description]
 res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
 
 cur.close()
 
 return render_template("userq2.html",pageTitle = "User Profile and Services",data = res)





@users.route("/librarian/services/<username>/<role>",methods=['GET', 'POST'])
def libservices(username,role):
                     cur = db.connection.cursor()
                     query = "SELECT s.school_id from users as u join schooluser as s on s.user_id = u.id where u.username ='{}'".format(username)
                     cur.execute(query)
                     db.connection.commit()
                     data1 =cur.fetchone()   
                     school = data1[0]
                     query = "SELECT u.id,u.username,u.role_id from users as u join schooluser as su on su.user_id = u.id where su.school_id ='{}' and (u.role_id = '-1' or u.role_id = '-3' )".format(school)
                     cur.execute(query)
                     db.connection.commit()
                     column_names = [i[0] for i in cur.description]
                     data = [dict(zip(column_names, entry)) for entry in cur.fetchall()] 
                     
                     formuseractivate = formid()
                     dummy1 = formuseractivate.__dict__
                     uid1 = dummy1['id'].data
                     #activate a normal user
                     #print(uid1)
                     if uid1: 
                        query = "UPDATE users SET role_id = '0' where id = '{}' ;".format(uid1)
                        cur.execute(query)
                        flash("Activated", "success")
                     formuserdeactivate = formid2()
                     dummy2= formuserdeactivate.__dict__
                     uid2 = dummy2['id2'].data
                     #print(uid2)
                     #deactivate a user
                     if (uid2):
                        query = "UPDATE users SET role_id = '-3' where id = '{}' ".format(uid2)
                        cur.execute(query)
                        flash("Dectivated", "success")
                     formuserdelete = formid3()
                     dummy3= formuserdelete.__dict__
                     uid3 = dummy3['id3'].data 
                     #delete a user
                     if uid3:
                        query = "Delete from users where id = '{}' ".format(uid3)
                        cur.execute(query)
                     #get rentals awaiting confirmation   
                     query = "SELECT u.id as uid ,b.id as bid,u.curr_rnt as cr ,r.trdate as rd from users as u join schooluser as su on su.user_id = u.id join rental as r on r.user_id = u.id join book as b on b.id = r.book_id where su.school_id ='{}' and r.status = '0' ".format(school)
                     cur.execute(query)
                     db.connection.commit()
                     column_names = [i[0] for i in cur.description]
                     data2 = [dict(zip(column_names, entry)) for entry in cur.fetchall()]               
                     #get reservations awaiting confirmation     
                     query = "SELECT u.id as uid,u.curr_rnt as cr ,b.id as bid,r.trdate as rd from users as u join schooluser as su on su.user_id = u.id join reservation as r on r.user_id = u.id join book as b on b.id = r.book_id where su.school_id ='{}' and r.status = '0' ".format(school)
                     cur.execute(query)
                     db.connection.commit()
                     column_names = [i[0] for i in cur.description]
                     data3 = [dict(zip(column_names, entry)) for entry in cur.fetchall()] 
                     #insert/confirm a rental from the reservations
                     formreservationconfirm = formubid()
                     dummy4= formreservationconfirm.__dict__
                     uid4 = dummy4['uid'].data
                     bid4 = dummy4['bid'].data
                     if uid4 and bid4 :
                        query = "INSERT INTO rental (user_id,book_id,trdate,status,libr_id) VALUES ('{}', '{}',default,1,default); ".format(uid4,bid4)
                        query += "  UPDATE reservation SET status = '1' where book_id ='{}' and user_id = '{}' ".format(bid4,uid4)
                        cur.execute(query)
                        db.connection.commit()
                     #confirm the return of a book
                     formreturn = formubid2()
                     dummy5= formreturn.__dict__
                     uid5 = dummy5['uid2'].data
                     bid5 = dummy5['bid2'].data
                     if uid5 and bid5 :
                        query = "UPDATE rental SET status = '2' where user_id='{}' and book_id ='{}' and status ='1' ; ".format(uid5,bid5)
                        cur.execute(query)
                        db.connection.commit()
                    #confirm a rental from rentals awaiting confirmation
                     formrentalconfirm = formubid3()
                     dummy6= formrentalconfirm.__dict__
                     uid6 = dummy6['uid3'].data
                     bid6 = dummy6['bid3'].data
                     if uid6 and bid6 :
                        query = "UPDATE rental SET status = '1' where user_id='{}' and book_id ='{}' and status ='0' ; ".format(uid6,bid6)
                        cur.execute(query)
                        db.connection.commit()
                     cur.close() 
                     return render_template("librarian.html",un = username,role=role ,data = data,data2 = data2,data3 = data3, formuserdeactivate = formuserdeactivate, formuseractivate = formuseractivate,formrentalconfirm=formrentalconfirm,formreturn = formreturn,formreservationconfirm = formreservationconfirm,formuserdelete = formuserdelete)