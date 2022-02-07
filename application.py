from flask import Flask, request, render_template, redirect, jsonify
from flask_jsglue import JSGlue # this is use for url_for() working inside javascript which is help us to navigate the url
import util
import os
from werkzeug.utils import secure_filename
from flask_cors import cross_origin


application = Flask(__name__, template_folder='template')

# JSGlue is use for url_for() working inside javascript which is help us to navigate the url
jsglue = JSGlue() # create a object of JsGlue
jsglue.init_app(application) # and assign the app as a init app to the instance of JsGlue

util.load_artifacts()

#home page
@application.route("/",methods=['GET','POST'])
@cross_origin()
def home():
    return render_template("index.html")
    
# here is route of 404 means page not found error
@application.errorhandler(404)
@cross_origin()
def page_not_found(e):
    # here i created my own 404 page which will be redirect when 404 error occured in this web app
    return render_template("404.html")

if __name__ == "__main__":
    application.run(debug=True)
