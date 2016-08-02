from flask import Flask, render_template, flash, request, url_for, redirect, session
from content_management import Content
from wtforms import Form
from dbConnect import connection
from wtforms import TextField, BooleanField, validators, PasswordField
from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart # For escaping SQL Injection type stuff
import gc
from passlib.apps import custom_app_context as pwd_context
from functools import wraps
import smtplib
from flask_mail import Mail, Message

TOPIC_DICT = Content()


app = Flask(__name__)
app.secret_key = "super secret key"

# Configuration for E-Mail
app.config.update(
DEBUG=True,
#EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = "yourusername@gmail.com", # Change here (Important)
    MAIL_PASSWORD = 'yourpassword'
)
mail = Mail(app) # This needs to be done only after Configurations are set

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/dashboard/')
def dashboard():
    try:
        try:
            client_name, settings, tracking, rank = userinformation()
            if len(tracking) < 10:
                tracking = "/introduction-to-python-programming/"
            gc.collect()

            if client_name == "Guest":
                flash("Welcome Guest, feel free to browse content. Progress tracking is only available for registered users")
                tracking = ['None']

            update_user_tracking()

            #completed_percentages = topic_completion_percent()

            return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)
        except Exception, e:
            return ((str(e),"Please report errors to test@qwerty.com"))
    except Exception, e:
        return ((str(e),"Please report errors to test@qwerty.com"))

    #flash("Flash Test !!!")
    #return render_template("dashboard.html",TOPIC_DICT = TOPIC_DICT)

def userinformation():

    try:
        client_name = (session['username'])
        guest = False
    except:
        guest = True
        client_name = "Guest"
    if not guest:
        settings = [0,0]
        tracking = [0,0]
        rank = [0,0]
        try:
            c, conn = connection()
            c.execute("SELECT * FROM users WHERE username = (%s)",
                    (thwart(client_name)))
            data = c.fetchone()
            settings = data[4]
            tracking = data[5]
            rank = data[6]
            #flash(data)
        except Exception, e:
            pass
            #flash(str(e))
    else:
        settings = [0,0]
        tracking = [0,0]
        rank = [0,0]


    return client_name, settings, tracking, rank

def update_user_tracking():
    try:
        completed = str(request.args['completed'])

        if completed in str(TOPIC_DICT.values()):
            client_name, settings, tracking, rank = userinformation()


            if tracking == None:
                tracking = completed
            else:
                if completed not in tracking:
                    tracking = tracking+","+completed

            c,conn = connection()
            c.execute("UPDATE users SET tracking = %s WHERE username = %s",(thwart(tracking),thwart(client_name)))
            conn.commit()
            c.close()
            conn.close()
            client_name, settings, tracking, rank = userinformation()

            #flash(str(client_name))
            #flash(str(tracking))
        else:
            pass

    except Exception, e:
        pass
        #flash(str(e))

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
            return redirect(url_for('login'))
    return wrap

@app.route("/send-mail/")
def send_mail():
    try:
        msg = Message("Forgot Password !!!",
        sender="yoursendingemail@gmail.com", #yoursendingemail@gmail.com
        recipients=["receivingemail@gmail.com"]) #receivingemail@gmail.com
        msg.body = "Yo!\n Hello "+username+', \n You or someone else has requested that a new password be generated for this email address.'
        #msg.html = render_template('/mails/reset-password.html',username=username, link=link)

        mail.send(msg)
        return 'Mail sent'

    except Exception as e:
        return str(e)

@app.route("/jinjaman/")
def jinjaman():
    try:
        gc.collect()
        data = [15,'15','Python is good',"Python, Java, PHP, SQL, C++",'<p><strong>Hey There !</strong></p>']
        return render_template('jinja-templating.html',data=data)
    except Exception, e:
        return (str(e))

@app.route("/converters/<page>/")
@app.route("/converters/<int:page>/")
@app.route("/converters/<float:page>/")
@app.route("/converters/<string:page>/")
@app.route("/converters/<path:page>/")
def converterexample(page):
    try:
        gc.collect()
        return render_template('converterexample.html',page=page)
    except Exception, e:
        return (str(e))


@app.route("/logout/")
@login_required
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
