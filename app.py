from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
#from send_email import send_email
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sharinganx3000@localhost/weight_collector'
db=SQLAlchemy(app)

class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email_=db.Column(db.String(120), unique=True)
    weight_=db.Column(db.Integer)

    def __init__(self,email_,weight_):
        self.email_=email_
        self.weight_=weight_ 

    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        email = request.form["email_name"]
        weight = request.form["weight_name"]
        data=Data(email,weight)
        if db.session.query(Data).filter(Data.email_==email).count() == 0:
            db.session.add(data)
            db.session.commit()
            average_weight=db.session.query(func.avg(Data.weight_)).scalar()
            average_weight=round(average_weight,1)
            count=db.session.query(Data.weight_).count()
            #send_email(email,weight,average_weight,count)
            return render_template("success.html")
    return render_template("index.html",
    text="Seems like we have got something from that email already.")


if __name__ == '__main__':
    app.debug=True
    app.run()



