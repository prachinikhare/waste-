from flask import Flask, request, render_template, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_jsglue import JSGlue # this is use for url_for() working inside javascript which is help us to navigate the url
import util
import os
from werkzeug.utils import secure_filename

application = Flask(__name__, template_folder='template')
application.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///feedback.db"
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

class Feedback(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.name}"

# JSGlue is use for url_for() working inside javascript which is help us to navigate the url
jsglue = JSGlue() # create a object of JsGlue
jsglue.init_app(application) # and assign the app as a init app to the instance of JsGlue

util.load_artifacts()
#home page
@application.route("/index")
def home():
    return render_template("index.html")

@application.route("/about")
def about():
    return render_template("about.html")

#classify waste
@application.route("/classify", methods = ["GET","POST"])
def classify():
    image_data = request.files["file"]
    #save the image to upload
    basepath = os.path.dirname(__file__)
    image_path = os.path.join(basepath, "uploads", secure_filename(image_data.filename))
    image_data.save(image_path)

    predicted_value, details, video1, video2 = util.classify_waste(image_path)
    os.remove(image_path)
    return jsonify(predicted_value=predicted_value, details=details, video1=video1, video2=video2)

@application.route("/feedback", methods=['GET', 'POST'])
def feedback():
    if request.method=='POST':
        name = request.form['name']
        email = request.form['email']
        message  = request.form['message']
        feedback = Feedback(name=name, email=email, message = message)
        db.session.add(feedback)
        db.session.commit()
        
    allFeedback = Feedback.query.all() 
    return render_template('feedback.html', allFeedback=allFeedback)  

#@application.route('/show')
#def waste_products():
    #allFeedback = Feedback.query.all()
    #print(allFeedback)
    #return 'this is waste products page'

@application.route('/delete/<int:sno>')
def delete(sno):
    feedback = Feedback.query.filter_by(sno=sno).first()
    db.session.delete(feedback)
    db.session.commit()
    return redirect("/")        

# here is route of 404 means page not found error
@application.errorhandler(404)
def page_not_found(e):
    # here i created my own 404 page which will be redirect when 404 error occured in this web app
    return render_template("404.html")

if __name__ == "__main__":
    application.run(debug=True)
