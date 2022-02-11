from flask import Flask, request, render_template, redirect, jsonify
from flask_jsglue import JSGlue # this is use for url_for() working inside javascript which is help us to navigate the url
import util
import os
from PIL import Image
import io
import base64
from werkzeug.utils import secure_filename

application = Flask(__name__ , template_folder='templates',instance_relative_config=True, static_url_path = "/static", static_folder = "static")
UPLOAD_FOLDER = './static'
application.config['UPLOAD_FOLDER'] = "C:/Users/Dell/Downloads/Awareness of waste recycling/images"
# JSGlue is use for url_for() working inside javascript which is help us to navigate the url
jsglue = JSGlue() # create a object of JsGlue
jsglue.init_app(application) # and assign the app as a init app to the instance of JsGlue

util.load_artifacts()

#home page
@application.route('/')
@application.route('/index.html')
def home():
    return render_template("index.html")

@application.route('/about')
@application.route("/about.html")
def about():
    return render_template("about.html")

@application.route('/feedback')
@application.route("/feedback.html")
def feedback():
    return render_template("feedback.html")

#classify waste
@application.route('/')
@application.route('/classify.html')
def classify():
    return render_template("classify.html")

@application.route('/classifywaste')
@application.route("/classifywaste",methods=['POST','GET'])
def classifywaste():
    if request.method =='POST':
        image_data = request.files["file"]
        if image_data.filename == "":
            print("Image must have a file name")
            return redirect(request.url)
        filename = secure_filename(image_data.filename)
        #save the image to upload
        basepath = os.path.abspath(os.path.dirname(__file__))
        image_path = os.path.join(basepath,application.config["UPLOAD_FOLDER"],filename)
        image_data.save(image_path)
        predicted_value, details, video1, video2 = util.classify_waste(image_path)
        os.remove(image_path)
        img = Image.open(application.config["UPLOAD_FOLDER"]+"/"+ filename)
        data = io.BytesIO()
        img.save(data,"JPEG")
        encode_img_data = base64.b64encode(data.getvalue())
        return jsonify(predicted_value=predicted_value, details=details, video1=video1, video2=video2)
    return render_templates("classify.html", filename=encode_img_data.decode("UTF-8"))
    

if __name__ == '__main__':
    application.debug = True
    application.run()
