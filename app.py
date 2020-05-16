# This app collects user heights
# and sends this to a database
# this then emails back the user with
# the average height of the dataset 
# 
# Python required modules 
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
# working with PostGreSQL with Flask applications
# like PsycoPG2
from sqlalchemy.sql import func

app=Flask(__name__)
#database address
#localhost PostGreSQL
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/height_collector'
# Local DB
# app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:postgres@localhost/height_collector'
#instantiate the DB
db=SQLAlchemy(app)

# The data Model class
# instantiate the object
class Data(db.Model):
    # Name the table
    __tablename__="data"
    # Create the column schema
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    height_=db.Column(db.Integer)

    # initializing the instance variables
    def __init__(self, email_, height_):
        self.email_=email_
        self.height_=height_

# Return the index homepage
@app.route("/")
def index():
    return render_template("index.html")

# Return success route on POST 
# Explicitly declare POST method
@app.route("/success", methods=['POST'])
def success():
    # If the method is POST 
    if request.method=='POST':
        # Assign email variable to html form element with [name]
        # Assign height variable to html form element with [name]
        email=request.form["email_name"]
        height=request.form["height_name"]
        # print the height an email to console
        # print the entire form
        print(request.form)
        print(email, height)
        # if same email record does not exist
        # create
        # session query (object) filter (object value)
        if db.session.query(Data).filter(Data.email_ == email).count()== 0:
            # assign the "data" variable to the email and height values
            # create an instance of the class with the two parameters
            # see above init method
            data=Data(email,height)
            # Add the db "data" object to the database
            db.session.add(data)
            # commit the session to the databse
            db.session.commit()
            
            # DB functions
            # average
            # rounding
            # count of objects
            average_height=db.session.query(func.avg(Data.height_)).scalar()
            average_height=round(average_height, 1)
            count = db.session.query(Data.height_).count()
            # Invoke method to send email
            send_email(email, height, average_height, count)
            # print the average height
            print(average_height)
            # render page
            return render_template("success.html")
            # variable passed to template
    return render_template('index.html', text="Seems like we got something from that email already!")

# Running the dev environment 
if __name__ == '__main__':
    app.debug=True
    app.run(port=5005)