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

initialized = False

def initializeDB():
    planet_2 = Planet(
        planet_id=2,
        planet_nickname="Bumblewhisp",
        planet_name="11 UMi b",
        planet_description="No: 2; Name: 11 UMi b; Num Stars: 1; Discovery Year: 2009; Orbital Period Days: 516.219. The exoplanet 11 Umi b was discovered a while back in 2009. It has 1 star in its system, and has a orbital period of 516 days.",
        planet_page_background="#000000",
        adopter_username="yangyang2ok",
        adopter_description=f"This planet is Yang's!",
    )
    db.session.add(planet_2)
    db.session.commit()
    planet_76 = Planet(
        planet_id=76,
        planet_nickname="Aplon",
        planet_name="COCONUTS-2 b",
        planet_description="No: 76; Name: COCONUTS-2 b; Num Stars: 1; Discovery Year: 2021; Orbital Period Days: 402000000. The exoplanet COCONUTS-2 b was discovered recently in 2021. It has only 1 star in its system, and has an incredibly huge rbital period of 402 million days!",
        planet_page_background="#000000",
        adopter_username="Ashij7",
        adopter_description=f"This planet is Aarushi's!",
    )
    db.session.add(planet_76)
    db.session.commit()
    planet_187 = Planet(
        planet_id=187,
        planet_nickname="Thebes",
        planet_name="GJ 180 b",
        planet_description="No: 187; Name: GJ 180 b; Num Stars: 1; Discovery Year: 2014; Orbital Period Days: 17.133. The exoplanet GJ 180 b was discovered some time ago in 2014. It has 1 star in its system, and has a really small orbital period of 17 days.",
        planet_page_background="#000000",
        adopter_username="antoniomigotto",
        adopter_description=f"This planet is Antonio's!",
    )
    db.session.add(planet_187)
    db.session.commit()
    planet_516 = Planet(
        planet_id=516,
        planet_nickname="Silara",
        planet_name="HD 12648 b",
        planet_description="No: 516; Name: HD 12648 b; Num Stars: 1; Discovery Year: 2015; Orbital Period Days: 133.6. The exoplanet HD 12648 b was discovered in 2015. It has 1 star, and has an orbital period of 133 days.",
        planet_page_background="#000000",
        adopter_username="daramtulla",
        adopter_description=f"This planet is David's!",
    )
    db.session.add(planet_187)
    db.session.commit()
    initialized = True


@app.route("/")
def dashboard():
    if any(session):
        print(f"logged_in=True")
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
            return redirect(url_for("dashboard"))
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

            new_planet = Planet(
                planet_id=planet_id,
                planet_nickname="",
                planet_name=planet_name,
                planet_description=f"The {planet_name} planet is {planet[18]} parsecs away from our Sun. It is {planet[3]} times the size of Jupiter while having a mass {planet[2]} times that of Jupiter.",
                planet_page_background="#000000",
                adopter_username=username,
                adopter_description=f"This planet has been adopted by '{username}'.",
            )
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
                identifier=planet_id,
            )
        except:
            return (
                "This user either already exists or there was an issue with your"
                " registration. Try again!"
            )
    return "How did we get here?"


@app.route("/planet/<int:planet_id>")
def planet(planet_id):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    render_template(
        "planet.html",
        planet_id=planet_id,
        nickname=planet.planet_nickname,
        name=planet.planet_name,
        description=planet.planet_description,
        page_background=planet.planet_page_background,
        adopter_username=planet.adopter_username,
        adopter_description=planet.adopter_description,
    )


@app.route("/editor")
def planet_page_editor():
    pass


if __name__ == "__main__":
    app.run(debug=True, template_folder="templates")

with app.app_context():
    db.create_all()
    if not initialized:
        initializeDB()
    # db.reflect()
