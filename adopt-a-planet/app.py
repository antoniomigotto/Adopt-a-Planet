from flask import Flask, render_template
import os.path

app = Flask(__name__)

if __name__=="__main__":
    app.run(debug=True, template_folder='templates')

@app.route('/')
def dashboard():
    """TODO: Docstring for dashboard.
    :returns: TODO
    """
    return render_template('dashboard.html')

@app.route('/login')
def login():
    """TODO: Docstring for login.
    :returns: TODO
    """

    return render_template('login.html')

