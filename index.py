from bottle import (
    route,
    run,
    template,
    app,
    static_file,
    request,
    redirect,
    debug,
    hook,
    redirect,
    abort,
)
import requests
import json

FM4_API = "http://audioapi.orf.at/fm4/json/2.0/broadcasts/"
DOWNLOAD_URL = "http://loopstream01.apa.at/?channel=fm4&id="


@route("/")
def root():
    try:
        r = requests.get(FM4_API)
    except requests.exceptions.ConnectionError as e:
        abort(500, "Error downloading json:" + str(e.message))

    try:
        broadcasts = json.loads(r.content)
    except Exception as e:
        abort(500, "Unable to parse json content!")

    days = []
    for item in broadcasts:
        days.append(item["day"])

    if len(days) <= 0:
        abort(500, "No values from json")

    return template("templates/index.html", days=days)


@route("/broadcasts", method="POST")
def broadcasts():
    day = request.forms.get("day")

    if not day:
        abort(500, "Missing values")

    r = requests.get(FM4_API)
    broadcasts = json.loads(r.content)
    days = []
    for item in broadcasts:
        days.append(item["day"])

    r = requests.get(FM4_API + day)
    shows = json.loads(r.content)
    print(shows)

    return template("templates/shows.html", shows=shows, day=day, days=days)


@route("/program", method="GET")
def programinfo():
    programKey = request.query.get("programKey")
    day = request.query.get("day")

    if not day or not programKey:
        abort(500, "Missing values")

    r = requests.get(FM4_API + day + "/" + programKey)
    data = json.loads(r.content)

    print(data)
    if data["streams"]:
        redirect(DOWNLOAD_URL + data["streams"][0]["loopStreamId"] + "&offset=0")
    else:
        redirect("http://localhost:8080/no")


@route("/no")
def nostream():
    return template("templates/no.html")


@route("/static/dist/css/<filename>")
def static_css(filename):
    return static_file(filename, root="dist/css/")


@route("/static/dist/js/<filename>")
def server_js(filename):
    return static_file(filename, root="dist/js/")


@route("/static/images/<filename>")
def server_images(filename):
    return static_file(filename, root="images/")


run(host="localhost", port=8080, server="paste", reloader=True, debug=True)
