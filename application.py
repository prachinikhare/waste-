from flask import Flask, request, render_template, redirect, jsonify

application = Flask(__name__,template_folder='templates', static_folder='static')

#home page
@application.route("/index")
@application.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    application.debug = True
    application.run()
