from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldb import db ## initially created by __init__.py, need to be used here
from schooldb.book.forms import BookForm,BookForm3
from schooldb.book import book
from schooldb.keyword.forms import KeywordForm
from schooldb.writer.forms import WriterForm
'''@book.route("/book")
def getBook():
    """
    Retrieve books from database
    """
    try:
        form = BookForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM book")
        column_names = [i[0] for i in cur.description]
        book = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("book.html", book = book, pageTitle = "books Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)'''

@book.route("/book/create", methods = ["GET", "POST"]) ## "GET" by default
def createBook():
    """
    Create new book in the database
    """
    form = BookForm()
    form1 = KeywordForm()
    form2 = WriterForm()
    form3 = BookForm3()
    addexbook = form3.__dict__
    addexb = addexbook['id'].data
    addexschool = addexbook['school3'].data
    addexcopies = addexbook['copies3'].data
    newwb = form2.__dict__
    writer =newwb['name'].data
    writerbook = newwb['book'].data
    newkey = form1.__dict__
    key = newkey['word'].data
    book = newkey['book'].data
    cur = db.connection.cursor()
    if addexb and addexbook and addexcopies:
        query = "INSERT INTO schoolbook(school_id,book_id,curr_opies,tot_copies) VALUES ('{}','{}','{}','{});".format(addexschool,addexbook,addexcopies,addexcopies)
        cur.execute(query)
        db.connection.commit()
    if key and book :
        query="INSERT INTO keyword (book_id,word) VALUES ('{}', '{}');".format(book,key)
        cur.execute(query)
        db.connection.commit()
    if writer and writerbook :
        query = "INSERT INTO writer(id,name) VALUES (default,'{}');".format(writer)
        query+= "INSERT INTO bwriter(book_id,(SELECT id from writer where name = '{}')) VALUES ('{}',(SELECT id from writer where name ='{}'));".format(writerbook,writer,writerbook,writer)
        cur.execute(query)
        db.connection.commit()
    if(request.method == "POST" and form.validate_on_submit()):
        newBook = form.__dict__
        query = "INSERT INTO book(id,isbn,title,publisher,summary,lang,pages,coverurl) VALUES (default,'{}','{}','{}','{}','{}','{}',default);".format(newBook['isbn'].data, newBook['title'].data, newBook['publisher'].data, newBook['summary'].data, newBook['lang'].data)
        try:
           
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Book inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
        query = "INSERT INTO schoolbook(school_id,book_id,curr_opies,tot_copies) VALUES ('{}',(select id from book where title ='{}','{}','{});".format(newBook['school'].data, newBook['title'].data,  newBook['copies'].data, newBook['copies'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Book inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
    ## else, response for GET request
    return render_template("create_book.html", pageTitle = "Create book", form3 = form3,form = form,form1 = form1,form2=form2)



@book.route("/book/update/<id>", methods = ["POST"])
def updatebook(id):
    """
    Update a book in the database, by id
    """
    form = BookForm() ## see createBook for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "INSERT schoolbook(school_id,book_id,curr_copies,tot_copies) VALUES () = {};".format(updateData['school'].data, id,updateData['copies'].data,updateData['copies'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Book updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return render_template("create_book.html", pageTitle = "Update book", form = form)

@book.route("/book/delete/<int:id>", methods = ["POST"])
def deleteBook(id):
    """
    Delete book by id from database
    """
    query = f"DELETE FROM book WHERE id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("book deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("book.getBook"))
