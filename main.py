# Heavily based on example shown in links shared below
# https://www.youtube.com/watch?v=WRu6brI0UrQ
# https://www.youtube.com/watch?v=Vf2K6zYQmu8
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from flask import Flask,render_template
from flask import request
from math import *
from functions import *
app = Flask(__name__)

@app.route('/')
def hello():
    # Create the phase diagram
    # Save it as a png in the static folder
    # Give the location to html so website can display it
    plotCurves()
    plt.savefig('static/my_plot.png')
    plt.close()

    return render_template('index.html',plot_url = 'static/my_plot.png')

@app.route('/get_plot',methods=['GET','POST'])
def get_plot():
    if request.method =='POST':
        # Get input values
        wt = request.form["wt"]
        temp = request.form["temp"]
        
        wt = float(wt)
        temp = float(temp)

        # Figure out if inputs are valid
        # If not, get error message identifying which quantity was invalid
        valid,feedback = validateUserInput(wt,temp)

        if(valid == True):
            # Figure out which region of the phase diagram inputs are related to
            phase = findPhase(wt,temp)

            # Plot the new phase diagram, tie line, and get the output results
            data,tieLine_exists = findComposition(wt,temp,phase)
            
            # Provide all available plots
            if(tieLine_exists):
                return render_template('index.html',plot_url = 'static/my_plot.png',plot_url1 = 'static/my_plot1.png',plot_url2 = 'static/my_plot2.png',data = data)
            else:
                return render_template('index.html',plot_url = 'static/my_plot.png',data = data)
        else:
            # Fill the data array to give an error message
            data = [[],[],[]]
            data[0].append(0)
            data[1].append("Error")
            data[2].append(feedback)
            return render_template('index.html',plot_url = 'static/my_plot.png',data = data)
    else:
        return render_template('index.html')
    
app.secret_key = 'A requirement'

if __name__=="__main__":
    app.run('127.0.0.1',5000,debug=True)


