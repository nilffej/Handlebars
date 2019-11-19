# Team Handlebars
# SoftDev1 PD 9
# K25
# 11/13/2019

from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import urllib.request, json
app = Flask(__name__)

#-----------------------------------------------------------------
#DATABASE SETUP
DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
#Creates USERNAMES
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='USERNAMES' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE USERNAMES(userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT);")
#Creates SAVED
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='SAVED' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE SAVED(userID INTEGER, bikeNumber INTEGER);")
#Creates REVIEWS
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='REVIEWS' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE REVIEWS(userID INTEGER, bikeID TEXT, location TEXT, rating INTEGER, content BLOB);")
#Creates BIKES
c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='BIKES' ''')
if c.fetchone()[0] < 1:
    c.execute("CREATE TABLE BIKES(bikeNumber INTEGER PRIMARY KEY AUTOINCREMENT, city TEXT, country TEXT, bikeID TEXT, name TEXT, latitude INTEGER, longitude INTEGER);")

#-----------------------------------------------------------------

@app.route("/")
def root():
    return render_template("homepage.html")

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
    return redirect(url_for('root'))
  # checking to see if things were submitted
  if (request.args):
    if (bool(request.args["username"]) and bool(request.args["password"])):
      # setting request.args to variables to make life easier
      inpUser = request.args["username"]
      inpPass = request.args["password"]
      with sqlite3.connect(Info.db) as connection:
        cur = connection.cursor()
        q = 'SELECT username, password FROM USERNAMES;'
        foo = cur.execute(q)
        userList = foo.fetchall()
        for row in userList:
          if inpUser == row[0]:
            if inpPass == row[1]:
              session['user'] = inpUser
              return(redirect(url_for("profile")))
            else:
              flash('Login credentials were incorrect. Please try again.')
              return(redirect(url_for("login")))
    else:
      flash('Login unsuccessful')
      return(redirect(url_for("login")))

  return render_template("login.html")


if __name__ == "__main__":
    app.debug = True
    app.run()
