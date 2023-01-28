from flask import Flask, render_template
import os.path

app = Flask(__name__)

@app.route('/')
def dashboard():
    """TODO: Docstring for dashboad.
    :returns: TODO
    """
    return render_template('dashboard.html')

@app.route('/login')
def login():
    """TODO: Docstring for login.
    :returns: TODO
    """
    return render_template('login.html')

if __name__=="__main__":
    app.run(debug=True)
