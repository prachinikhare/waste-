from flask import Flask, request, render_template, redirect, jsonify

application = Flask(__name__,template_folder='template', static_folder='static')

#home page
@application.route("/index")
@application.route("/")
def index():
    return render_template("index.html")

# here is route of 404 means page not found error
@application.errorhandler(404)
def page_not_found(e):
    # here i created my own 404 page which will be redirect when 404 error occured in this web app
    return render_template("404.html")

if __name__ == '__main__':
    application.debug = True
    application.run()
