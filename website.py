from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = 'Temporary Secret Key. Update for Prod.'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

from firebase import User
webuser = User()
@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        error = webuser.register(request.form['fullname'], request.form['email'], request.form['password'])
        if not error:
            return redirect(url_for('timeline'))
    return render_template('register.html', error=error)

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        error = webuser.login(request.form['email'], request.form['password'])
        if not error:
            return redirect(url_for('timeline'))
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
    userdata = webuser.get_user_data(uid)
    return render_template('user.html', userdata=userdata)

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
