from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

#from flask_debugtoolbar import DebugToolbarExtension
#app.config['SECRET_KEY'] = 'Temporary Secret Key. Update for Prod.'
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#toolbar = DebugToolbarExtension(app)

from user import User
webuser = User()
from functools import wraps
# This decorator redirects user to login
def logged_in_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not webuser.authenticated():
           return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# This decorator redirects user to the timeline
def logged_out_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if webuser.authenticated():
           return redirect(url_for('timeline'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/register", methods=['GET', 'POST'])
@logged_out_only
def register():
    error = None
    if request.method == 'POST':
        error = webuser.register(request.form)
        if not error:
            return redirect(url_for('timeline'))
    return render_template('register.html', error=error)

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        error = webuser.login(request.form)
        if not error:
            return redirect(url_for('timeline'))
    else:
        webuser.logout()
    return render_template('login.html', error=error)

@app.route("/")
@app.route("/timeline")
@logged_in_only
def timeline():
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['filtered_endorsements'] = webuser.get_timeline_endorsements()
    return render_template('timeline.html', **pagedata)

@app.route("/user/<uid>")
@logged_in_only
def user(uid):
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['userdata'] = webuser.get_user_data(uid)
    pagedata['filtered_endorsements'] = webuser.get_user_endorsements(uid)
    return render_template('user.html', **pagedata)

@app.route("/pending")
@logged_in_only
def pending():
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['pending_endorsements'] = webuser.get_pending_endorsements()
    return render_template('pending.html', **pagedata)

@app.route("/invite")
@logged_in_only
def invite():
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('invite.html', **pagedata)

@app.route("/about")
def about():
    pagedata = {}
    if webuser.authenticated():
        pagedata['user_uid'] = webuser.get_uid()
    return render_template('about.html', **pagedata)

@app.route("/tos")
def tos():
    pagedata = {}
    if webuser.authenticated():
        pagedata['user_uid'] = webuser.get_uid()
    return render_template('tos.html', **pagedata)

@app.errorhandler(404)
def page_not_found(error):
    pagedata = {}
    if webuser.authenticated():
        pagedata['user_uid'] = webuser.get_uid()
    return render_template('404.html', **pagedata), 404

if __name__ == '__main__':
    app.run()
