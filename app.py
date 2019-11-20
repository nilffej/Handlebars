# Team Handlebars
# SoftDev1 PD 9
# K25
# 11/13/2019

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from flask import flash
from flask import session
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
#Creates SAVEDBIKES
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SAVEDBIKES' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE SAVEDBIKES(username TEXT, bikeNumber INTEGER);")
#Creates REVIEWS
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='REVIEWS' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE REVIEWS(username TEXT, bikeID TEXT, location TEXT, rating INTEGER, content BLOB);")
#Creates BIKES
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BIKES' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE BIKES(bikeNumber INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, country TEXT, bikeID TEXT, name TEXT, latitude INTEGER, longitude INTEGER);")

#-----------------------------------------------------------------

@app.route("/")
def root():
    return render_template("homepage.html")
@app.route("/loggedIn")
def loggedIn():
    return render_template("loggedIn.html")
@app.route("/logout")
def logout():
    if "user" in session:
        session.pop('user')
    return redirect(url_for("root"))

@app.route("/search")
def search():
    if request.args["searchbar"]:
        u = urllib.request.urlopen("https://www.metaweather.com/api/location/search/?query={}".format(request.args["searchbar"].replace(" ","%20")))
        response = u.read()
        data = json.loads(response)
        if len(data) == 0:
            return redirect(url_for("root"))
        u = urllib.request.urlopen("https://www.metaweather.com/api/location/{}".format(data[0]["woeid"]))
        response = u.read()
        data = json.loads(response)
        weather = data['consolidated_weather'][0]
        return render_template("searchresults.html", place = data['title'],
                                latt_long = data['latt_long'],
                                applicable_date = weather['applicable_date'],
                                weather_state_name = weather['weather_state_name'],
                                image = "https://www.metaweather.com/static/img/weather/png/64/{}.png".format(weather['weather_state_abbr']))
    else:
        return redirect(url_for("root"))

@app.route("/login")
def login():
  # if user already logged in, redirects back to discover
  if 'user' in session:
    return redirect(url_for('loggedIn'))
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
          if inpUser == row[0]:
            if inpPass == row[1]:
              session['user'] = inpUser
              return(redirect(url_for("loggedIn")))
            else:
              flash('Login credentials were incorrect. Please try again.')
              return(redirect(url_for("login")))
    else:
      flash('Login unsuccessful')
      return(redirect(url_for("login")))

  return render_template("login.html")


def updateUsers():
    with sqlite3.connect(DB_FILE) as connection:
        cur = connection.cursor()
        foo = cur.execute('SELECT username, password FROM USER;') # Selects all username/password combinations
        userList = foo.fetchall()
        userList.sort() # Usernames sorted in alphabetical order
        return userList


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



if __name__ == "__main__":
    app.debug = True
    app.run()
