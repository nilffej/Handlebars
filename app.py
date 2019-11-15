# Team Handlebars
# SoftDev1 PD 9
# K25
# 11/13/2019

from flask import Flask, render_template, request, redirect, url_for
import urllib.request, json
app = Flask(__name__)

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



if __name__ == "__main__":
    app.debug = True
    app.run()
