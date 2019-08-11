import json
import time
from flask import Flask, Markup, render_template, Response
from flask import request
from flask import jsonify
from flask_sse import sse

app = Flask(__name__)

app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

#array to store values
# values = []

colors = [
          "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
          "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
          "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

#endpoint to receive data 
@app.route('/send-data')
def populateData():
    data = request.args.get('data')
    if(data!=None):
       data=int(data)
       if (data < 0):
           with open("values.txt", "w+") as f:
               f.write("")
       else:
            with open("values.txt", "a+") as f:
               f.write("%d " % data)
#     def generate():
       json_data = json.dumps({'value': data})
       #yield f"data:{json_data}\n\n"
#        time.sleep(0.5)
    sse.publish({"data": json_data}, type='graph')
    return Response(generate())

#root
@app.route('/')
def returnRoot():
    return '''<h1>root</h1>'''

#draws graph according to the input data
@app.route('/line')
def line():
    values = []
    with open("values.txt", "r") as f:
        values = [int(x) for x in f.read().split()]

    line_labels=labels
    line_values=values[-10:]
    return render_template('line_chart.html', title='WaterFlow Graph', max=30, labels=line_labels, values=line_values)

@app.route('/show-data') #GET requests will be blocked
def showData():

    values = []
    with open("values.txt", "r") as f:
        values = [int(x) for x in f.read().split()]
    return '''<h1>The received values are: {}</h1>'''.format(values)

@app.route('/data-json') #GET requests will be blocked
def showDataJson():

    values = []
    with open("values.txt", "r") as f:
        values = [int(x) for x in f.read().split()]
    return jsonify(values)

@app.route('/realtime-chart') 
def showRealTime():
    return render_template('realtime.html')
          
if __name__ == '__main__':

    # create an empty file before everything
    with open("values.txt", "w+") as f:
        f.write("")
       
    app.run(host='0.0.0.0', port=8080, threaded=True)

