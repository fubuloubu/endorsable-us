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
    pagedata = {}
    pagedata['error'] = error
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('register.html', **pagedata)

@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        error = webuser.login(request.form['email'], request.form['password'])
        if not error:
            return redirect(url_for('timeline'))
    pagedata = {}
    pagedata['error'] = error
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('login.html', **pagedata)

@app.route("/")
@app.route("/timeline")
def timeline():
    if not webuser.authenticated():
       return redirect(url_for('login'))
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['filtered_endorsements'] = webuser.get_all_endorsements()
    return render_template('timeline.html', **pagedata)

@app.route("/user/<uid>")
def user(uid):
    if not webuser.authenticated():
       return redirect(url_for('login'))
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['userdata'] = webuser.get_user_data(uid)
    pagedata['filtered_endorsements'] = webuser.get_endorsements_by_uid(uid)
    return render_template('user.html', **pagedata)

@app.route("/pending")
def pending():
    if not webuser.authenticated():
       return redirect(url_for('login'))
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    pagedata['pending_endorsements'] = webuser.get_pending_endorsements()
    return render_template('pending.html', **pagedata)

@app.route("/invite")
def invite():
    if not webuser.authenticated():
       return redirect(url_for('login'))
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('invite.html', **pagedata)

@app.route("/about")
def about():
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('about.html', **pagedata)

@app.route("/tos")
def tos():
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('tos.html', **pagedata)

@app.errorhandler(404)
def page_not_found(error):
    pagedata = {}
    pagedata['user_uid'] = webuser.get_uid()
    return render_template('404.html', **pagedata), 404

if __name__ == '__main__':
    app.run()
