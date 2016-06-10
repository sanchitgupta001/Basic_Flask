from flask import Flask, render_template, flash, request, url_for, redirect
from content_management import Content

TOPIC_DICT = Content()


app = Flask(__name__)
app.secret_key = "super secret key"

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():

    #flash("Flash Test !!!")
    return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def Method_not_found(e):
    return render_template("405.html")
# @app.route('/slashboard/')
# def slashboard():
#     try:
#         return render_template("dashboard.html",TOPIC_DICT = slaughter)
#     except Exception as e:
#         return render_template("500.html",error=e)

#####################################    LOGIN    #############################################

@app.route('/login/',methods=['GET','POST']) # if methods are not set, Method not allowed error occurs
def login():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']
            # flash(attempted_username)
            # flash(attempted_password)
            if attempted_username == "admin" and attempted_password == "password":
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid Credentials... Plz Try Again !!!'

        return render_template('login.html',error=error)

    except Exception as e:
        return render_template("login.html",error=e)

if __name__=="__main__":
    app.run()
