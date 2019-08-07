from flask import Flask, Markup, render_template
from flask import request
app = Flask(__name__)


labels = [
          'JAN', 'FEB', 'MAR', 'APR',
          'MAY', 'JUN', 'JUL', 'AUG',
          'SEP', 'OCT', 'NOV', 'DEC'
          ]

#array to store values
values = []

colors = [
          "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
          "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
          "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]


@app.route('/send-data') #GET requests will be blocked
def populateData():
    data = request.args.get('data')
    values.append(data)
    return '''<h1>The received value is: {}</h1>'''.format(data)

@app.routeRoot('/') #GET requests will be blocked
def return():
    return '''<h1>root{}</h1>'''

#draws graph according to the input data
@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='WaterFlow Graph', max=17000, labels=line_labels, values=line_values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
