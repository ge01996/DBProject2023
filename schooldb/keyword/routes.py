from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldbdb import db ## initially created by __init__.py, need to be used here
from schooldbdb.keyword.forms import KeywordForm
from schooldbdb.keyword import keyword

@keyword.route("/keyword")
def getkeyword():
    """
    Retrieve keywords from database
    """
    try:
        form = KeywordForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM keyword")
        column_names = [i[0] for i in cur.description]
        keyword = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("keyword.html", keyword = keyword, pageTitle = "keywords Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@keyword.route("/keyword/create", methods = ["GET", "POST"]) ## "GET" by default
def createKeyword():
    """
    Create new keyword in the database
    """
    form = KeywordForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain keyword input, whereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")

    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newKeyword = form.__dict__
        query = "INSERT INTO keyword(book_id,word) VALUES ('{}','{}');".format(newKeyword['book'].data),format(newKeyword['word'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("keyword inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
       

    ## else, response for GET request
    return render_template("create_keyword.html", pageTitle = "Create keyword", form = form)

'''@keyword.route("/keyword/update/<int:id>", methods = ["POST"])
def updatekeyword(id):
    """
    Update a keyword in the database, by id
    """
    form = KeywordForm() ## see createkeyword for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE keyword SET publisher = '{}' WHERE id = {};".format(updateData['publisher'].data, id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("keyword updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("keyword.getkeyword"))'''

@keyword.route("/keyword/delete/<int:id>", methods = ["POST"])
def deleteKeyword(id,word):
    """
    Delete keyword by id from database
    """
    query = f"DELETE FROM keyword WHERE book_id = {id} and word = {word};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("keyword deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("keyword.getKeyword"))
