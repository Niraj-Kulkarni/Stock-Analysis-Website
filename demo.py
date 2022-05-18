from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.embed import components
from bokeh.resources import CDN

code = 'GOOG'
start_date = datetime.datetime(2021,1, 1)
end_date = datetime.datetime(2021,2,28)
df = data.DataReader(name=code, data_source='yahoo', start=start_date, end=end_date)

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
cdn_js = CDN.js_files
cdn_css = CDN.css_files

print(cdn_js[0])
output_file("ok.html")
show(p)
 


