from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from send_email import send_email


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:sharinganx3000@localhost/StockX_data'
db=SQLAlchemy(app)


class Data(db.Model):
    __tablename__="user_data"
    id=db.Column(db.Integer, primary_key=True)
    user_name_=db.Column(db.String(120))
    email_=db.Column(db.String(120), unique=True)


    def __init__(self,user_name_,email_):
        self.user_name_=user_name_
        self.email_=email_
    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        name = request.form["user_name"]
        email = request.form["email_name"]
        password = request.form["pwdUser"]
        confirm_pwd = request.form["pwdConfirm"]
        if password != confirm_pwd:
            return render_template("index.html",
            text="Incorrect password")
        data=Data(name,email)
        if db.session.query(Data).filter(Data.user_name_==name, Data.email_==email).count() == 0:
            db.session.add(data)
            db.session.commit()
            send_email(email,name)
            return render_template("success.html")
    return render_template("index.html",
    text="Seems like we have got something from that email already.")


@app.route('/plot/',methods=['POST'])
def plot():    
    return render_template("plot.html")


@app.route('/graph/',methods=['POST'])
def graph():
    import datetime
    from pandas_datareader import data
    from bokeh.plotting import figure, show, output_file
    from bokeh.models import HoverTool, ColumnDataSource
    from bokeh.embed import components
    from bokeh.resources import CDN

    code_ = request.form["codex"]
    start_ = request.form["start_date"]
    end_ = request.form["end_date"]

    start_1 = start_.split(sep='/')
    end_1= end_.split(sep='/')

    mapped_1 = list(map(int,start_1))
    mapped_2 = list(map(int,end_1))

    start_y = mapped_1[0]
    start_m = mapped_1[1]
    start_d = mapped_1[2]

    end_y = mapped_2[0]
    end_m = mapped_2[1]
    end_d = mapped_2[2]

    code = code_.upper()
    src = 'yahoo'
    start_date = datetime.datetime(start_y,start_m,start_d)
    end_date = datetime.datetime(end_y,end_m,end_d)
    df = data.DataReader(name=code, data_source=src, start=start_date, end=end_date)

    def inc_dec(close, opens):
        if close > opens:
            return 'increase'
        elif close < opens:
            return 'decrease'
        else:
            return 'equal'
            

    df['Status'] = [inc_dec(close, opens) for close, opens in zip(df.Close, df.Open)]
    df['Middle'] = (df.Close + df.Open)/2 
    df['Height'] = abs(df.Close - df.Open)



    p = figure(x_axis_type='datetime', width=1000, height=300, sizing_mode='scale_width')
    p.title.text = 'CandleStick Stock Chart'
    p.xaxis.axis_label="DATE"
    p.yaxis.axis_label="VALUE"
    p.grid.grid_line_alpha = 0.3


    hours_12 = 12 * 60 * 60 * 1000

    # p.segment(smallest value of x,
    #           smallest value of y, 
    #           largest value of x, 
    #           largest value of y )

    p.segment(df.index, df.High, df.index, df.Low, color='Black', name = 'segment')

    df['Open'] = df['Open'].astype(int)
    df['High'] = df['High'].astype(int)
    df['Low'] = df['Low'].astype(int)
    df['Close'] = df['Close'].astype(int)

    # For hover
    col_data_src1 = ColumnDataSource(df[df.Status=='increase'])
    col_data_src2 = ColumnDataSource(df[df.Status=='decrease'])

    #  p.rect(central point of x_axis,
    #         central point of y axis {(open+close)/2}, 
    #         width of x axis, 
    #         height of y axis)    

    p.rect('Date', 'Middle', hours_12, 
        'Height', fill_color='green', line_color='black',
        source=col_data_src1, name='increase')

    p.rect('Date', 'Middle', hours_12, 
        'Height', fill_color='red', line_color='black',
        source=col_data_src2, name='decrease')

    hover = HoverTool(names=["increase","decrease"],
                    tooltips=[('Open','@Open'), ('Close', '@Close'), ('High', '@High'), ('Low', '@Low')])

    p.add_tools(hover)

    script1, div1 = components(p)
    cdn_js = CDN.js_files[0]
    return render_template("graph.html",
    script1=script1,
    div1=div1,
    cdn_js=cdn_js)
    


if __name__ == "__main__":
    app.run(debug=True)
