from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldb import db ## initially created by __init__.py, need to be used here
from schooldb.category.forms import categoryForm
from schooldb.category import category

@category.route("/category")
def getCategory():
    """
    Retrieve categorys from database
    """
    try:
        form = categoryForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM category")
        column_names = [i[0] for i in cur.description]
        category = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("category.html", category = category, pageTitle = "categorys Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@category.route("/category/create", methods = ["GET", "POST"]) ## "GET" by default
def createCategory():
    """
    Create new category in the database
    """
    form = categoryForm() ## This is an object of a class that inherits FlaskForm
    ## which in turn inherits Form from wtforms
    ## https://flask-wtf.readthedocs.io/en/0.15.x/api/#flask_wtf.FlaskForm
    ## https://wtforms.readthedocs.io/en/2.3.x/forms/#wtforms.form.Form
    ## If no form data is specified via the formdata parameter of Form
    ## (it isn't here) it will implicitly use flask.request.form and flask.request.files.
    ## So when this method is called because of a GET request, the request
    ## object's form field will not contain category input, whereas if the HTTP
    ## request type is POST, it will implicitly retrieve the data.
    ## https://flask-wtf.readthedocs.io/en/0.15.x/form/
    ## Alternatively, in the case of a POST request, the data could have between
    ## retrieved directly from the request object: request.form.get("key name")

    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newcategory = form.__dict__
        query = "INSERT INTO bookcat(book_id,cat_id ) VALUES ('{}','{}');".format(newcategory['book'].data),format(newcategory['catid'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("category inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")
       
        '''query = "INSERT INTO bookcat(book_id,(SELECT id from category where name = '{}')) VALUES ('{}',(SELECT id from category where name ='{}'));".format(newcategory['name'].data),format(newcategory['id'].data),format(newcategory['name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("category-book relation inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger") '''

    ## else, response for GET request
    return render_template("create_category.html", pageTitle = "Create category", form = form)

'''@category.route("/category/update/<int:id>", methods = ["POST"])
def updatecategory(id):
    """
    Update a category in the database, by id
    """
    form = categoryForm() ## see createcategory for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE category SET publisher = '{}' WHERE id = {};".format(updateData['publisher'].data, id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("category updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("category.getcategory"))

@category.route("/category/delete/<int:id>", methods = ["POST"])
def deleteCategory(id):
    """
    Delete category by id from database
    """
    query = f"DELETE FROM category WHERE id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("category deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("category.getcategory"))'''
