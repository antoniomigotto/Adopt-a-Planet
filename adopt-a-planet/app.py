from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

import os.path
import json

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///adoptaplanet.db'
db.init_app(app)

class User(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    planet = db.Column(db.Integer)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_submit', methods=['GET', 'POST'])
def login_submit():
    if request.method == 'GET':
        flash('''Something went wrong. Was everything done within the 
              confines of the site? If so, report as error GET_ME_IN''')
        redirect(url_for('login'))

    username = request.form['username'] 
    password = request.form['password']

    if request.form['account_type'] == 'Login':
        try:
            user = User.query.filter_by(username=username).first()
            if user.password != password:
                return 'Incorrect password! Try again.'
            response = make_response(render_template('dashboard.html'))
            response.set_cookie('username_cookie', username)
            return response
        except:
            return 'Username not found! Or something else went wrong, perhaps.'


    if request.form['account_type'] == 'Register':
        new_user = User(username=username, password=password)
        try:
            db.session.add(new_user)
            print(new_user.username)
            db.session.commit()
            return "Registering!"
            # return render_template(url_for('meet_your_planet')) 
        except: 
            return 'This user either already exists or there was an issue with your registration. Try again!' 
    return 'How did we get here?'

@app.route('/meet_your_planet', methods=['GET', 'POST'])
def meet_your_planet():
    pass

if __name__=="__main__":
    app.run(debug=True, template_folder='templates')

with app.app_context():
    db.create_all()
    # db.reflect()

