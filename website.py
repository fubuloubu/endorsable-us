from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

def add_user(formdata):
    #user = auth.sign_in_with_email_and_password(formdata.email, formdata.password)
    # Add email and fullname to our database under /users
    return False # If account has already been added

def validate(formdata):
    #user = auth.sign_in_with_email_and_password(formdata.email, formdata.password)
    return False # If account is not in system

def user_logged_in():
    return False

def create_link(routename, linktext):
    return '<a href="' + url_for(routename) +'">' + linktext + '</a>'

@app.route("/signup", methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        if add_user(request.form):
            return redirect(url_for('timeline'))
        else:
            error = 'The email you provided is already in use' + \
                    '<br><br>You can login ' + create_link('login', 'here')
    return render_template('signup.html', error=error)

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if validate(request.form):
            return redirect(url_for('timeline'))
        else:
            error = 'Your password is incorrect or you are not registered in the system' + \
                    '<br><br>You can sign-up ' + create_link('signup', 'here')
    return render_template('login.html', error=error)

@app.route("/")
@app.route("/timeline")
def timeline():
    if not user_logged_in():
       return redirect(url_for('login'))
    return render_template('timeline.html')

@app.route("/user/<uid>")
def user(uid):
    if not user_logged_in():
       return redirect(url_for('login'))
    return render_template('user.html')

@app.route("/pending")
def pending():
    if not user_logged_in():
       return redirect(url_for('login'))
    return render_template('pending.html')

@app.route("/invite")
def invite():
    if not user_logged_in():
       return redirect(url_for('login'))
    return render_template('invite.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/tos")
def tos():
    return render_template('tos.html')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()
