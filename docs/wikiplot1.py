# Get this figure: fig = py.get_figure("https://plot.ly/~sarenseeley/21/")
# Get this figure's data: data = py.get_figure("https://plot.ly/~sarenseeley/21/").get_data()
# Add data to this figure: py.plot(Data([Scatter(x=[1, 2], y=[2, 3])]), filename ="Plot 21", fileopt="extend")
# Get y data of first trace: y1 = py.get_figure("https://plot.ly/~sarenseeley/21/").get_data()[0]["y"]

# Get figure documentation: https://plot.ly/python/get-requests/
# Add data documentation: https://plot.ly/python/file-options/

# If you're using unicode in your file, you may need to specify the encoding.
# You can reproduce this figure in Python with the following code!

# Learn about API authentication here: https://plot.ly/python/getting-started
# Find your api_key here: https://plot.ly/settings/api

import plotly.plotly as py
from plotly.graph_objs import *
py.sign_in('username', 'api_key')
trace1 = {
      "line": {"color": "rgba(31,119,180,1)"}, 
      "name": "data", 
      "type": "box", 
      "xsrc": "sarenseeley:20:4e046e", 
      "x": ["example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1", "example 1"], 
      "ysrc": "sarenseeley:20:ab17b2", 
      "y": [0.062761749, 0.069548301, 1.2, 0.106722959, 0.107913332, 0.098811028, 0.147040802, 0.145063702, 0.124137486, 0.085251371, 0.102119294, 0.110388611, 0.061137365, 0.06445587, 0.060540812, 0.040621786, 0.041287255, 0.042188746], 
      "frame": None, 
      "xaxis": "x", 
      "yaxis": "y", 
      "jitter": 0.3, 
      "marker": {
        "line": {
          "color": "black", 
          "width": 1
        }, 
        "size": 12, 
        "color": "rgba(31,119,180,1)"
      }, 
      "pointpos": -1.8, 
      "boxpoints": "all", 
      "fillcolor": "rgba(31,119,180,0.5)"
    }
data = Data([trace1])
layout = {
      "xaxis": {
        "type": "category", 
        "title": "data", 
        "domain": [0, 1], 
        "titlefont": {
          "size": 18, 
          "color": "black", 
          "family": "Arial, sans-serif"
        }, 
        "automargin": True, 
        "categoryarray": ["example 1"], 
        "categoryorder": "array"
      }, 
      "yaxis": {
        "title": "fd_mean", 
        "domain": [0, 1], 
        "titlefont": {
          "size": 18, 
          "color": "black", 
          "family": "Arial, sans-serif"
        }, 
        "automargin": True
      }, 
      "margin": {
        "b": 40, 
        "l": 60, 
        "r": 10, 
        "t": 25
      }, 
      "hovermode": "closest", 
      "showlegend": False
    }
fig = Figure(data=data, layout=layout)
plot_url = py.plot(fig)