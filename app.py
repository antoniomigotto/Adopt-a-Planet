from flask import Flask, render_template
from csv_reader import *
import os.path

app = Flask(__name__)

new_id = planet_finder()

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


@app.route('/meetyourplanet')
def meetyourplanet():
    """TODO: Docstring for planet.
    :returns: TODO
    """
    arrays = planet_finder()
    return render_template('meet_your_planet.html', PlanetIdentifier=arrays[0], TypeFlag=arrays[1],
                           PlanetaryMassJpt=arrays[2], RadiusJpt=arrays[3], PeriodDays=arrays[4],
                           SemiMajorAxisAU=arrays[5], Eccentricity=arrays[6], PeriastronDeg=arrays[7],
                           LongitudeDeg=arrays[8], AscendingNodeDeg=arrays[9], InclinationDeg=arrays[10],
                           SurfaceTempK=arrays[11], AgeGyr=arrays[12], DiscoveryMethod=arrays[13],
                           DiscoveryYear=arrays[14], LastUpdated=arrays[15], RightAscension=arrays[16],
                           Declination=arrays[17], DistFromSunParsec=arrays[18],
                           HostStarMassSlrMass=arrays[19], HostStarRadiusSlrRad=arrays[20],
                           HostStarMetallicity=arrays[21], HostStarTempK=arrays[22], HostStarAgeGyr=arrays[23],
                           ListsPlanetIsOn=arrays[24])

@app.route('/adopt')
def adopt():
    arrays = planet_finder()
    csv_changer(arrays[26])
    return render_template('dashboard.html')


if __name__ == "__main__":
    app.run(debug=True)
