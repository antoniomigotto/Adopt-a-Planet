from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    make_response,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from csv_reader import *

import os.path
import json

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///adopt-a-planet.db"
db.init_app(app)

app.secret_key = "temporarily here"


class User(db.Model):
    username = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    planet = db.Column(db.String(256))

class Planet(db.Model):
    planet_id = db.Column(db.Integer, primary_key=True)
    planet_nickname = db.Column(db.String(256))
    planet_name = db.Column(db.String(256))
    planet_description = db.Column(db.String(2048))
    planet_page_background = db.Column(db.String(7))
    adopter_username = db.Column(db.String(32), primary_key=True)
    adopter_description = db.Column(db.String(2048))

@app.route("/")
def dashboard():
    if any(session):
        print(f'logged_in=True')
        return render_template("dashboard.html", logged_in=True)
    return render_template("dashboard.html", logged_in=False)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_submit", methods=["GET", "POST"])
def login_submit():
    if request.method == "GET":
        flash(
            """Something went wrong. Was everything done within the 
              confines of the site? If so, report as error GET_ME_IN"""
        )
        redirect(url_for("login"))

    username = request.form["username"]
    password = request.form["password"]

    if request.form["account_type"] == "Login":
        try:
            user = User.query.filter_by(username=username).first()
            if user.password != password:
                return "Incorrect password! Try again."
            session["username"] = user.username
            return redirect(url_for('dashboard'))
        except:
            return "Username not found! Or something else went wrong, perhaps."

    if request.form["account_type"] == "Register":
        try:
            planet = planet_finder()
            planet_name = planet[0]
            planet_id = planet[26]

            new_user = User(username=username, password=password, planet=planet_id)
            db.session.add(new_user)
            db.session.commit()

            new_planet = Planet(planet_id=planet_id, planet_nickname='', planet_name=planet_name, planet_description=f'The {planet_name} planet is {planet[18]} parsecs away from our Sun. It is {planet[3]} times the size of Jupiter while having a mass {planet[2]} times that of Jupiter.', planet_page_background='#000000', adopter_username=username, adopter_description=f'This planet has been adopted by \'{username}\'.')
            db.session.add(new_planet)
            db.session.commit()

            return render_template(
                "meet_your_planet.html",
                PlanetName=planet[0],
                TypeFlag=planet[1],
                PlanetaryMassJpt=planet[2],
                RadiusJpt=planet[3],
                PeriodDays=planet[4],
                SemiMajorAxisAU=planet[5],
                Eccentricity=planet[6],
                PeriastronDeg=planet[7],
                LongitudeDeg=planet[8],
                AscendingNodeDeg=planet[9],
                InclinationDeg=planet[10],
                SurfaceTempK=planet[11],
                AgeGyr=planet[12],
                DiscoveryMethod=planet[13],
                DiscoveryYear=planet[14],
                LastUpdated=planet[15],
                RightAscension=planet[16],
                Declination=planet[17],
                DistFromSunParsec=planet[18],
                HostStarMassSlrMass=planet[19],
                HostStarRadiusSlrRad=planet[20],
                HostStarMetallicity=planet[21],
                HostStarTempK=planet[22],
                HostStarAgeGyr=planet[23],
                ListsPlanetIsOn=planet[24],
                identifier=planet_id
            )
        except:
            return (
                "This user either already exists or there was an issue with your"
                " registration. Try again!"
            )
    return "How did we get here?"


@app.route("/planet/<int:planet_id>")
def planet(planet_id):

    render_template('planet.html')
    # No: 2; Name: 11 Umi b; Num Stars: 1; Discovery Year: 2009; Orbital Period Days: 516.219
    # The exoplanet 11 Umi b was discovered a while back in 2009. It has 1 star in its system, and has a orbital period of 516 days.

    # No: 76; Name: COCONUTS-2 b; Num Stars: 1; Discovery Year: 2021; Orbital Period Days: 402000000
    # The exoplanet COCONUTS-2 b was discovered recently in 2021. It has only 1 star in its system, and has an incredibly huge rbital period of 402 million days!

    # No: 187; Name: GJ 180 b; Num Stars: 1; Discovery Year: 2014; Orbital Period Days: 17.133
    # The exoplanet GJ 180 b was discovered some time ago in 2014. It has 1 star in its system, and has a really small orbital period of 17 days

    # No: 516; Name: HD 12648 b; Num Stars: 1; Discovery Year: 2015; Orbital Period Days: 133.6
    # The exoplanet HD 12648 b was discovered in 2015. It has 1 star, and has an orbital period of 133 days.


@app.route("/editor")
def planet_page_editor():
    pass


if __name__ == "__main__":
    app.run(debug=True, template_folder="templates")

with app.app_context():
    db.create_all()
    # db.reflect()
