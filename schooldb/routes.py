from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from schooldb import app, db ## initially created by __init__.py, need to be used here
from schooldb.users import users
from schooldb.users.forms import formid

@app.route("/")
def index():
    try:
        ## create connection to database
        cur = db.connection.cursor()
        ## execute query
        cur.execute("SELECT name from school")
        ## cursor.fetchone() does not return the column names, only the row values
        ## thus we manually create a mapping between the two, the dictionary res
        column_names = [i[0] for i in cur.description]
        res = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        #print(res)
        cur.close()    
        return render_template("landing.html", pageTitle = "Home Page",school = res)                        
    except Exception as e:
        print(e)
        return render_template("landing.html", pageTitle = "Home Page")

@app.route("/login", methods=['GET', 'POST'])
def login():
    global role
    global username 
    username = request.form['username']
    password = request.form['password']
    if request.method == 'POST' and username and password :
        if username!='admin':
            query = "SELECT u.password from users as u where u.username ='{}'".format(username)
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            data1 =cur.fetchone()   
            passw = data1[0]
            print(passw)
            print (passw,username,password)
            cur.close()
            if password!= passw :
                flash("Invalid password", "danger")
            else: 
                query = "SELECT u.role_id from users as u where u.username ='{}'".format(username)
                cur = db.connection.cursor()
                cur.execute(query)
                db.connection.commit()
                data1 =cur.fetchone()   
                role = data1[0]
                flash("Logged in", "success")
                if role == '2' :
                    return redirect(url_for("users.libservices",username = username,role = role))
                cur.close()
                if role == '0' or role =='1':
                    return redirect(url_for("users.services",username = username,role = role))
                
        elif  username == 'admin' and  password == 'admin':
            
            flash("Logged in as administrator", "success")
            
            
            return render_template("adminhome.html")
    return redirect(url_for("index"))

@app.route("/logout", methods=['GET', 'POST'])
def logout():
   flash("Logged out", "success")
   return redirect(url_for("index"))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500

@app.route("/manual", methods=['GET', 'POST'])
def manual():
    return render_template("manual.html", pageTitle = "USER MANUAL")
