from flask import Flask, render_template, request
import json
import plotly.graph_objects as go
import sqlite3
from consultasMIS import *

app =  Flask(__name__)


@app.route("/")
def home():
    return '<p>Home Page</p>'

@app.route("/ips")
def ips():
    ips_sorted = getTopIps()
    ip_alerts_plot = []
    ip_name = []
    for ip in ips_sorted:
        ip_alerts_plot.append(ip[1])
        ip_name.append(ip[0])
    fig = go.Figure(data=[go.Bar(y=ip_alerts_plot,x=ip_name)],layout_title_text='TOP 10 IPS ALERTS',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)

@app.route("/categories")
def categories():
    alerts = getAlertsByCategory()
    alerts_types = []
    alerts_number = []
    for alertType in alerts:
        alerts_types.append(alertType)
        alerts_number.append(alerts[alertType])
    fig = go.Figure(data=[go.Bar(y=alerts_number,x=alerts_types)],layout_title_text='ALERTS BY CATEGORIES',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)

@app.route("/alerts")
def alerts():
    alerts = getAlertsInTime()
    fig = go.Figure(data=[go.Scatter(x=alerts['Date'],y=alerts['Alerts'])],layout_title_text='ALERTS DAILY',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)


@app.route("/dispositivos")
def dispositivos():
    ids, values = getDispositivosVulnerables()
    fig = go.Figure(data=[go.Table(header=dict(values=['ID',"TOTAL"]),cells= dict(values=[ids,values]))],layout_title_text='ALERTS BY DEVICE',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)

@app.route("/puertos")
def puertos():
    media_puertos, servicios_inseguros, servicios = getPuertosMetricas()
    fig = go.Figure(data=[go.Table(header=dict(values=['MEDIA PUERTOS',"TOTAL SERVICIOS INSEGUROS","TOTAL SERVICIOS"]),cells= dict(values=[[media_puertos],[servicios_inseguros],[servicios]]))],layout_title_text='PORTS METRICS',layout=go.Layout(height=800))
    import plotly
    a = plotly.utils.PlotlyJSONEncoder
    graphJSON = json.dumps(fig, cls=a)
    return render_template('home.html',graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug = True)

