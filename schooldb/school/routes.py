from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldb import db ## initially created by __init__.py, need to be used here
from schooldb.school.forms import SchoolForm
from schooldb.school import school

@school.route("/school")
def getSchool():
    """
    Retrieve schools from database
    """
    try:
        form = SchoolForm()
        cur = db.connection.cursor()
        cur.execute("SELECT name FROM school")
        column_names = [i[0] for i in cur.description]
        school = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("school.html", school = school, pageTitle = "School Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@school.route("/school/create", methods = ["GET", "POST"]) ## "GET" by default
def createSchool():
    """
    Create new school in the database
    """
    form = SchoolForm() ## This is an object of a class that inherits FlaskForm


   
    if(request.method == "POST" and form.validate_on_submit()):
        newSchool = form.__dict__
        query = "INSERT INTO school(id,name,email,principal,librarian,city,address,zip_code,phone) VALUES (default,'{}', '{}', '{}','{}', '{}', '{}' , '{}' , '{}' );".format(newSchool['name'].data,newSchool['email'].data,newSchool['principal'].data,newSchool['librarian'].data,newSchool['city'].data,newSchool['address'].data,newSchool['zip_code'].data,newSchool['phone'].data )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("School inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_school.html", pageTitle = "Create School", form = form)

@school.route("/school/update/<int:id>", methods = ["POST"])
def updateSchool(id):
    """
    Update a school in the database, by id
    """
    form = SchoolForm() ## see create school for explanation
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE school SET principal = '{}', librarian = '{}' WHERE id = {};".format(updateData['principal'].data, updateData['librarian'].data, id)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("School updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("school.getSchool"))

@school.route("/school/delete/<int:id>", methods = ["POST"])
def deleteSchool(id):
    """
    Delete school by id from database
    """
    query = f"DELETE FROM school WHERE id = {id};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("School deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("school.getSchool"))
