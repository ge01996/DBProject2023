from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldb import db ## initially created by __init__.py, need to be used here
from schooldbdb.writer.forms import WriterForm
from schooldbdb.writer import writer

@writer.route("/writer")
def getWriter():
    """
    Retrieve writers from database
    """
    try:
        form = WriterForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM writer")
        column_names = [i[0] for i in cur.description]
        writer = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("writer.html", writer = writer, pageTitle = "writers Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@writer.route("/writer/create", methods = ["GET", "POST"]) ## "GET" by default
def createWriter():
    """
    Create new writer in the database
    """
    form = WriterForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain writer input, whereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")

    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newWriter = form.__dict__
        query = "INSERT INTO writer(id,name) VALUES (default,'{}');".format(newWriter['name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("writer inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
       
        query = "INSERT INTO bwriter(book_id,(SELECT id from writer where name = '{}')) VALUES ('{}',(SELECT id from writer where name ='{}'));".format(newWriter['name'].data),format(newWriter['book'].data),format(newWriter['name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("writer-book relation inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_writer.html", pageTitle = "Create writer", form = form)

'''@writer.route("/writer/update/<int:id>", methods = ["POST"])
def updatewriter(id):
    """
    Update a writer in the database, by id
    """
    form = WriterForm() ## see createWriter for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE writer SET publisher = '{}' WHERE id = {};".format(updateData['publisher'].data, id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("writer updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("writer.getWriter"))'''

@writer.route("/writer/delete/<int:id>", methods = ["POST"])
def deleteWriter(id):
    """
    Delete writer by id from database
    """
    query = f"DELETE FROM writer WHERE id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("writer deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("writer.getWriter"))
