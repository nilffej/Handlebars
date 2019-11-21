from flask import Flask, render_template, request, session, url_for, redirect
import sqlite3
import os
import urllib2, json, sqlite3

DB_FILE = "Info.db"
db = sqlite3.connect(DB_FILE)
c = db.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS test (bikeNumber INTEGER PRIMARY KEY,
                                              bikeID TEXT,
                                              city TEXT,
                                              country TEXT,
                                              name TEXT,
                                              latitude FLOAT,
                                              longitude FLOAT)''')

app = Flask(__name__)

@app.route("/")
def root():
    u = urllib2.urlopen(
        "http://api.citybik.es/v2/networks"
    )
    response = u.read()
    data = json.loads(response)
    with sqlite3.connect(DB_FILE) as db:
        c = db.cursor()
        for i in data['networks']:
            # print(i['location']['city'])
            c.execute('INSERT INTO BIKES VALUES (?, ?, ?, ?, ?, ?, ?)', (None,
                                                                        i['id'],
                                                                        i['location']['city'],
                                                                        i['location']['country'],
                                                                        i['name'],
                                                                        i['location']['latitude'],
                                                                        i['location']['longitude']
                                                                        ))
    return render_template("test.html")

if __name__ == "__main__":
    app.debug = True
    app.run()

db.commit()
db.close()


# Displays specific user's page (for hyperlink on individual posts)
@app.route("/profile/<USERNAME>")
def profile2(USERNAME):
  userList = updateUsers()
  if 'user' in session:
    if (USERNAME == session["user"]):
        return redirect(url_for("profile"))
  entryList = updateSavedBikes()
  userSaved = []
  for entry in entryList:
    if entry[0] == USERNAME:
      userSaved.append()
  return render_template("entrydisplay.html",
                         title="Profile - {}".format(USERNAME), heading=USERNAME,
                         entries=userSaved, postNum=range(len(userSaved)),sessionstatus="user" in session)
