from flask import Flask, render_template, redirect, url_for, request
app = Flask(__name__)

#from flask_debugtoolbar import DebugToolbarExtension
#app.config['SECRET_KEY'] = 'Temporary Secret Key. Update for Prod.'
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#toolbar = DebugToolbarExtension(app)

from web_user import WebUser
webuser = WebUser()
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

@app.route("/", methods=['GET', 'POST'])
@app.route("/timeline", methods=['GET', 'POST'])
@logged_in_only
def timeline():
    error = None
    if request.method == 'POST':
        print('Form data: {}'.format(request.form))
        function = request.form['function']
        if function == 'Add Endorsement':
            error = webuser.add_endorsement(request.form)
    pagedata = {}
    pagedata['error'] = error
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['my_relationships'] = webuser.get_relationships()
    pagedata['filtered_endorsements'] = webuser.get_timeline_endorsements()
    return render_template('timeline.html', **pagedata)

@app.route("/user/<uid>", methods=['GET', 'POST'])
@logged_in_only
def user(uid):
    error = None
    if request.method == 'POST':
        print('Form data: {}'.format(request.form))
        function = request.form['function']
        if function == 'Add Friend':
            error = webuser.add_relationship(request.form)
        elif function == 'Add Endorsement':
            error = webuser.add_endorsement(request.form)
    pagedata = {}
    pagedata['error'] = error
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['userdata'] = webuser.get_user_data(uid)
    pagedata['my_relationships'] = webuser.get_relationships()
    pagedata['filtered_endorsements'] = webuser.get_user_endorsements(uid)
    pagedata['allow_add'] = not webuser.is_friend(uid)
    return render_template('user.html', **pagedata)

@app.route("/pending", methods=['GET', 'POST'])
@logged_in_only
def pending():
    error = None
    if request.method == 'POST':
        print('Form data: {}'.format(request.form))
        function = request.form['function']
        if function == 'Accept':
            error = webuser.accept_pending(request.form)
        elif function == 'Reject':
            error = webuser.reject_pending(request.form)
        elif function == 'Amend':
            error = webuser.amend_pending(request.form)
    pagedata = {}
    pagedata['error'] = error
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['pending_endorsements'] = webuser.get_pending_endorsements()
    return render_template('pending.html', **pagedata)

@app.route("/search")
@logged_in_only
def search():
    pagedata = {}
    pagedata['all_users'] = webuser.get_all_users()
    return render_template('search.html', **pagedata)

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
