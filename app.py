from flask import Flask, Markup, render_template
from flask import request
from flask import jsonify

app = Flask(__name__)


labels = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

#array to store values
values = []

colors = [
          "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
          "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
          "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

#endpoint to receive data 
@app.route('/send-data')
def populateData():
    data = int(request.args.get('data'))
    # if(data<0):
    #      values.clear()
    # elif(len(values)>=10): #shift the graph
    #      values.pop(0)
    #      values.append(data)
    # else:
    #      values.append(data)
    # return jsonify(values[-1])

    if (data < 0):
        with open("values.txt", "w+") as f:
            f.write("")
    else:
        with open("values.txt", "a+") as f:
            f.write("%d " % data)
    #get the most recent value, return it as json: For realtime graph
    return Response(jsonify(data), mimetype='text/event-stream')

#root
@app.route('/')
def returnRoot():
    return '''<h1>root</h1>'''

#draws graph according to the input data
@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('line_chart.html', title='WaterFlow Graph', max=3000, labels=line_labels, values=line_values)

@app.route('/show-data') #GET requests will be blocked
def showData():
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
    app.run(host='0.0.0.0', port=8080)

