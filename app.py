# Team Handlebars
# SoftDev1 PD 9
# K25
# 11/13/2019

from flask import Flask, render_template, request, session, redirect, url_for, redirect
import sqlite3
import os
from flask import flash
import urllib.request, json
from os import urandom
app = Flask(__name__)
app.secret_key = urandom(32)

#-----------------------------------------------------------------

#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
#Creates USER
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='USER' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE USER(username TEXT, password TEXT);")
    # TESTS
    c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu00","hi"))
    c.execute("INSERT INTO USER VALUES ('{}', '{}')".format("hliu01","hi"))

#Creates SAVEDBIKES
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SAVEDBIKES' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE SAVEDBIKES(username TEXT, bikeNumber INTEGER);")
    # TESTS
    c.execute("INSERT INTO SAVEDBIKES VALUES ('{}', '{}')".format("hliu00",2))
    c.execute("INSERT INTO SAVEDBIKES VALUES ('{}', '{}')".format("hliu00",1))
    c.execute("INSERT INTO SAVEDBIKES VALUES ('{}', '{}')".format("hliu01",2))
    c.execute("INSERT INTO SAVEDBIKES VALUES ('{}', '{}')".format("hliu01",1))

#Creates REVIEWS
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='REVIEWS' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE REVIEWS(username TEXT, bikeNumber INTEGER, rating INTEGER, content BLOB);")
    # TESTS
    c.execute("INSERT INTO REVIEWS VALUES ('{}', '{}', '{}', '{}')".format("hliu00", 2, 5, "0dswdwdw"))
    c.execute("INSERT INTO REVIEWS VALUES ('{}', '{}', '{}', '{}')".format("hliu01", 2, 5, "1dswdwdw"))
    c.execute("INSERT INTO REVIEWS VALUES ('{}', '{}', '{}', '{}')".format("hliu00", 1, 4, "2dswdwdw"))
    c.execute("INSERT INTO REVIEWS VALUES ('{}', '{}', '{}', '{}')".format("hliu01", 1, 4, "3dswdwdw"))

#Creates BIKES
c.execute(" SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BIKES' ")
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE BIKES(bikeNumber INTEGER PRIMARY KEY AUTOINCREMENT, bikeID TEXT, city TEXT, name TEXT, coors TEXT, address TEXT);")
    bikeapi = urllib.request.urlopen("http://api.citybik.es/v2/networks")
    bikeresponse = bikeapi.read()
    bikedata = json.loads(bikeresponse)
    for i in bikedata['networks']:
        coors = "{},{}".format(i['location']['latitude'],i['location']['longitude'])
        weatherapi = urllib.request.urlopen("https://www.metaweather.com/api/location/search/?lattlong={}".format(coors))
        response = weatherapi.read()
        weatherdata = json.loads(response)
        mapapi = urllib.request.urlopen("https://www.mapquestapi.com/geocoding/v1/reverse?key=GiP6vYcbAdnVUtnHGJwYdvAdAxupOahM&location={}".format(coors))
        response = mapapi.read()
        mapdata = json.loads(response)
        spotinfo = mapdata["results"][0]["locations"][0]
        address = "{}, {}".format(spotinfo["street"],spotinfo["adminArea5"])
        c.execute('INSERT INTO BIKES VALUES (?, ?, ?, ?, ?, ?)', (None, i['id'], weatherdata[0]["title"], i['name'], coors, address))
    db.commit()
    db.commit()
    db.close()

#-----------------------------------------------------------------

def updateSavedBikes():
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT * from SAVEDBIKES;') # Selects the title, username, date and content from all posts
        savedBikes = foo.fetchall()
        savedBikes.reverse() # Reverse for recent posts at top
        return savedBikes

def updateUsers():
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT * FROM USER;') # Selects all username/password combinations
        userList = foo.fetchall()
        userList.sort() # Usernames sorted in alphabetical order
        return userList

#-----------------------------------------------------------------

# DICTIONARY FOR IMPORTANT SEARCH DATA
searchdict = {}

@app.route("/")
def root():
    return render_template("homepage.html", sessionstatus = "user" in session)

@app.route("/search")
def search():
    if request.args and request.args["searchbar"]:
        # GEOCODE API - COORDINATE TRACK
        u = urllib.request.urlopen("http://open.mapquestapi.com/geocoding/v1/address?key=GiP6vYcbAdnVUtnHGJwYdvAdAxupOahM&location={}".format(request.args["searchbar"].replace(" ","%20")))
        response = u.read()
        data = json.loads(response)
        if len(data) == 0:
            return redirect(url_for("root"))
        firstresult = data["results"][0]["locations"][0]
        searchdict["longlat"] = "{},{}".format(firstresult["latLng"]["lat"],firstresult["latLng"]["lng"])

        # WEATHER API - WEATHER SEARCH
        u = urllib.request.urlopen("https://www.metaweather.com/api/location/search/?lattlong={}".format(searchdict["longlat"]))
        response = u.read()
        data = json.loads(response)
        city = data[0]["title"]
        u = urllib.request.urlopen("https://www.metaweather.com/api/location/{}".format(data[0]["woeid"]))
        response = u.read()
        data = json.loads(response)
        weather = data['consolidated_weather'][0]

        # BIKE DATABASE + API
        with sqlite3.connect(DB_FILE) as connection:
           cur = connection.cursor()
           q = "SELECT * FROM BIKES WHERE city = '{}'".format(city)
           foo = cur.execute(q)
           bikeList = foo.fetchall()
           bikes = []
           addresses = []
           for bike in bikeList:
               bikes.append(bike)


        # with sqlite3.connect(DB_FILE) as connection:
        #    cur = connection.cursor()
        #    q = "SELECT * FROM REVIEWS"
        #    foo = cur.execute(q)
        #    reviewList = foo.fetchall()
        #    specificBikeReviews = []
        #    if len(bikes) > 0:
        #        for review in reviewList:
        #            if review[1] == bikes[0][0]:
        #                specificBikeReviews.append(review)
        # numberOfRatings = 0
        # sum = 0
        # formattedReviews = []
        # temp = []
        # for specificBikeReview in specificBikeReviews:
        #     temp.append("Stars : {}".format(specificBikeReview[2]))
        #     temp.append("Review : {}".format(specificBikeReview[3]))
        #     formattedReviews.append(temp)
        #     sum += specificBikeReview[2]
        #     numberOfRatings += 1
        #     connection.commit()
        #     temp = []
        # if numberOfRatings == 0:
        #     rating = "No Reviews written yet"
        # else: rating = sum / numberOfRatings
        # session["bikeID"] = "2";
        # print(session["bikeID"]);
        return render_template("searchresults.html", place = data['title'],
                                applicable_date = weather['applicable_date'], celsius = int(weather['the_temp']), farenheit = int(weather['the_temp']*9.0/5+32),
                                bikes = bikes,
                                weather_state_name = weather['weather_state_name'], weatherimage = "https://www.metaweather.com/static/img/weather/png/64/{}.png".format(weather['weather_state_abbr']),
                                # reviews = formattedReviews, rating = rating,
                                mapimage = "https://www.mapquestapi.com/staticmap/v4/getmap?key=GiP6vYcbAdnVUtnHGJwYdvAdAxupOahM&size=600,600&type=map&imagetype=jpg&zoom=13&scalebar=true&traffic=FLOW|CON|INC&center={}&xis=&ellipse=fill:0x70ff0000|color:0xff0000|width:2|40.00,-105.25,40.04,-105.30".format(searchdict['longlat']),
                                sessionstatus = "user" in session)
    else:
        return redirect(url_for("root"))

@app.route("/login")
def login():
    # if user already logged in, redirects back to discover
    if 'user' in session:
        return redirect(url_for('root'))
    # checking to see if things were submitted
    if (request.args):
        if (bool(request.args["username"]) and bool(request.args["password"])):
            # setting request.args to variables to make life easier
            inpUser = request.args["username"]
            inpPass = request.args["password"]
            with sqlite3.connect(DB_FILE) as connection:
                cur = connection.cursor()
                q = 'SELECT username, password FROM USER;'
                foo = cur.execute(q)
                userList = foo.fetchall()
                for row in userList:
                    if inpUser == row[0] and inpPass == row[1]:
                        session['user'] = inpUser
                        return(redirect(url_for("root")))
                flash('Username not found or login credentials incorrect.')
                return(redirect(url_for("login")))
        else:
            flash('Login unsuccessful')
            return(redirect(url_for("login")))
    return render_template("login.html")

@app.route("/register")
def register():
  # if user already logged in, redirects back to discover
  if 'user' in session:
    return redirect(url_for('root'))

  # checking to see if things were submitted
  if (request.args):
    if (bool(request.args["username"]) and bool(request.args["password"])):
      # setting request.args to variables to make life easier
      inpUser = request.args["username"]
      inpPass = request.args["password"]
      inpConf = request.args["confirmPass"]

      if(addUser(inpUser, inpPass, inpConf)):
        flash('Success! Please login.')
        return redirect(url_for("login"))
      else:
        return(redirect(url_for("register")))
    else:
      flash('Please make sure to fill all fields!')
  return render_template("register.html")


@app.route("/logout")
def logout():
    if "user" in session:
        session.pop('user')
    return redirect(url_for("root"))

def addUser(user, pswd, conf):
  userList = updateUsers()
  for row in userList:
        if user == row[0]:
          flash('Username already taken. Please try again.')
          return False
  if (pswd == conf):
    # SQLite3 is being weird with threading, so I've created a separate object
    with sqlite3.connect(DB_FILE) as connection:
      cur = connection.cursor()
      q = "INSERT INTO USER VALUES('{}', '{}');".format(user, pswd) # Successfully registers new user
      cur.execute(q)
      connection.commit()
    return True
  else:
    flash('Passwords do not match. Please try again.')
    return False

@app.route("/addBike")
def addBike():
    with sqlite3.connect(DB_FILE) as connection:
        c = connection.cursor()
        c.execute("INSERT INTO SAVEDBIKES VALUES ('{}', '{}')".format(session['user'],2))
        connection.commit()
    return redirect(url_for("profile"))

@app.route("/addReview")
def addReview():
    if "user" not in session:
        return redirect(url_for('root'))
    if (len(request.args) == 1):
        with sqlite3.connect(DB_FILE) as connection:
            c = connection.cursor()
            n = c.execute("SELECT * FROM BIKES WHERE bikeNumber = (?)", (request.args["id"],)).fetchone()[3]
            loc = c.execute("SELECT * FROM BIKES WHERE bikeNumber = (?)", (request.args["id"],)).fetchone()[2]
            c.execute("SELECT * FROM REVIEWS WHERE username = (?) AND bikeNumber = (?)", (session['user'], request.args["id"]))
            l = c.fetchall()
            if (len(l) > 0) :
                return render_template("addreview.html", name = n, location = loc, i = request.args["id"], b = l[0][3])
            else: return render_template("addreview.html", name = n, location = loc, i = request.args["id"])
    if (len(request.args) >= 2):
        if (len(request.args["body"]) == 0):
            flash('Cannot leave body empty.')
            return redirect("http://127.0.0.1:5000/addReview?id=" + request.args["id"])
        else:
            if (len(request.args) == 2): rating = 0
            else: rating = request.args["rate"]
            with sqlite3.connect(DB_FILE) as connection:
                c = connection.cursor()
                c.execute("DELETE FROM REVIEWS WHERE username = (?) AND bikeNumber = (?)", (session["user"], request.args["id"]))
                c.execute("INSERT INTO REVIEWS VALUES (?, ?, ?, ?)", (session['user'], request.args["id"], rating, request.args["body"]))
                connection.commit()
            return redirect(url_for("profile"))
    with sqlite3.connect(DB_FILE) as connection:
        c = connection.cursor()
        c.execute("INSERT INTO REVIEWS VALUES ('{}', '{}', '{}', '{}')".format(session['user'], 2, 5, "dswdwdw"))
        connection.commit()
    return redirect(url_for("profile"))

# Dispalys user's personal blog page and loads HTML with blog writing form
@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for('root'))
    if (len(request.args) == 1):
        with sqlite3.connect(DB_FILE) as connection:
            c = connection.cursor()
            if ("id" in request.args.keys()):
                c.execute("SELECT * FROM SAVEDBIKES WHERE username = (?) AND bikeNumber = (?)", (session["user"], request.args["id"]))
                if (len(c.fetchall()) == 0):
                    c.execute("INSERT INTO SAVEDBIKES VALUES (?, ?)", (session["user"], request.args["id"]))
            else if ("rid" in request.args.keys()):

            connection.commit()
    entryList = updateSavedBikes()
    userList = updateUsers()
    # userSaved is filtered list of all entries by specific user
    userSaved = []
    toprint = []
    # goes through Saved bikes and if it is the users it appends it
    for entry in entryList:
        if entry[0] == session['user']:
            userSaved.append(entry)
    for entry in userSaved:
        cityName = ""
        with sqlite3.connect(DB_FILE) as connection:
          cur = connection.cursor()
          q = "SELECT * FROM BIKES"
          foo = cur.execute(q)
          bikeList = foo.fetchall()
          for x in bikeList:
              if x[0] == entry[1]:
                  toprint.append(x)
                  break
    return render_template("profile.html",
    title = "Profile - {}".format(session["user"]), heading = session["user"],
    entries = userSaved, toprint = toprint, sessionstatus = "user" in session)

if __name__ == "__main__":
    app.debug = True
    app.run()
