from flask import Flask, render_template
app = Flask(__name__)

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/")
@app.route("/timeline")
def timeline():
    return render_template('timeline.html')

@app.route("/user/<uid>")
def user(uid):
    return render_template('user.html')

@app.route("/pending")
def pending():
    return render_template('pending.html')

@app.route("/invite")
def invite():
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
