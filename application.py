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
from flask import Flask, request, render_template, redirect, jsonify
from flask_jsglue import JSGlue # this is use for url_for() working inside javascript which is help us to navigate the url
import util
import os
from werkzeug.utils import secure_filename

application = Flask(__name__,template_folder='templates', static_folder='static')

# JSGlue is use for url_for() working inside javascript which is help us to navigate the url
jsglue = JSGlue() # create a object of JsGlue
jsglue.init_app(application) # and assign the app as a init app to the instance of JsGlue

util.load_artifacts()
#home page
@application.route("/index")
@application.route("/")
def index():
    return render_template("index.html",methods=['GET'])

@application.route("/about",methods=['GET'])
def about():
    return render_template("about.html")

#classify waste
@application.route("/classifywaste",methods=['GET', 'POST'])
def classifywaste():
    image_data = request.files["file"]
    #save the image to upload
    basepath = os.path.dirname(__file__)
    image_path = os.path.join(basepath, "uploads", secure_filename(image_data.filename))
    image_data.save(image_path)

    predicted_value, details, video1, video2 = util.classifywaste(image_path)
    os.remove(image_path)
    return jsonify(predicted_value=predicted_value, details=details, video1=video1, video2=video2)

if __name__ == '__main__':
    application.debug = True
    application.run()
