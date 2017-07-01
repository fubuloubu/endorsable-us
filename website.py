from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'Temporary Secret Key. Update for Prod.'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

def create_link(route, text):
    return text

from firebase import User
webuser = User()
@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if webuser.register(request.form['fullname'], request.form['email'], request.form['password']):
            return redirect(url_for('timeline'))
        else:
            error = 'The email you provided is already in use' + \
                    '<br><br>You can login ' + create_link('login', 'here')
    return render_template('register.html', error=error)

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if webuser.login(request.form['email'], request.form['password']):
            return redirect(url_for('timeline'))
        else:
            error = 'Your password is incorrect or you are not registered in the system' + \
                    '<br><br>You can register ' + create_link('register', 'here')
    return render_template('login.html', error=error)

@app.route("/")
@app.route("/timeline")
def timeline():
    if not webuser.authenticated():
       return redirect(url_for('login'))
    return render_template('timeline.html')

@app.route("/user/<uid>")
def user(uid):
    if not webuser.authenticated():
       return redirect(url_for('login'))
    return render_template('user.html')

@app.route("/pending")
def pending():
    if not webuser.authenticated():
       return redirect(url_for('login'))
    return render_template('pending.html')

@app.route("/invite")
def invite():
    if not webuser.authenticated():
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
