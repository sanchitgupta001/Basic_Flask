from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from wtforms import Form
from dbConnect import connection
from wtforms import TextField, BooleanField, validators, PasswordField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart # For escaping SQL Injection type stuff
import gc
from passlib.apps import custom_app_context as pwd_context

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

def login_required(f): # login_required decorator
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs) #arguments and keyword arguments
        else:
            flash("You need to login first")
            return redirect(url_for('login_page'))

@app.route("/logout/")
def logout():
    session.clear()
    flash("You have been logged out!")
    gc.collect()
    return redirect(url_for('dashboard'))
# @app.route('/slashboard/')
# def slashboard():
#     try:
#         return render_template("dashboard.html",TOPIC_DICT = slaughter)
#     except Exception as e:
#         return render_template("500.html",error=e)

#####################################    LOGIN    #############################################

class RegistrationForm(Form):
    username = TextField("Username", [validators.length(min = 6, max = 20),validators.Required()])
    email = TextField("Email Address", [validators.length(min = 6, max = 50), validators.Required()])
    password  = PasswordField("password", [validators.length(min = 6, max = 100), validators.Required(),validators.EqualTo("confirm", message = "Passwords must match")])
    confirm = PasswordField('Repeat Password')



@app.route('/login/',methods=['GET','POST']) # if methods are not set, Method not allowed error occurs
def login():
    error = ''
    try:
        c, conn = connection()
        if request.method == "POST":
            data = c.execute("SELECT * FROM users where username = '%s'" % (thwart(request.form['username'])))


            if (data):
                data = c.fetchone()[2]
                if sha256_crypt.verify(request.form['password'],data):
                    session['logged_in'] = True
                    session['username'] = request.form['username']

                    flash("You are now logged in...")
                    return redirect(url_for("dashboard"))
                else:
                    error = "Invalid Credentials, try again."
            else:
                error = "Invalid Credentials"
            gc.collect()

        return render_template('login.html',error=error)

    except Exception as e:
        error = "Invalid Credentials, try again."
        return render_template("login.html",error=e)

####################################    Register    ###########################################

@app.route('/register/',methods=['GET','POST'])
def register():
    try:
        form = RegistrationForm(request.form)
        if request.method == "POST" and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str (form.password.data)),rounds = 12345)
            c, conn = connection()
            # c is the cursor here
            x = c.execute("SELECT * FROM users WHERE username = '%s'" % (thwart(username)))

            if int(x) > 0:
                flash("That username is already taken, please choose another one")
                return render_template("register.html",form=form)

            else:
                c.execute("INSERT INTO users (username, password, email, tracking) VALUES (%s, %s, %s, %s)",
                (thwart(username), thwart(password), thwart(email), thwart("/introduction-to-python-programming/")))

                conn.commit()   # data will not be saved in the database until this statement is executed
                flash("Thanx For Registering with us")

                c.close()
                conn.close()
                gc.collect() # gc : Garbage Collector

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

        return render_template("register.html",form = form)

    except Exception as e:
          return str(e)

if __name__=="__main__":
    app.run()
