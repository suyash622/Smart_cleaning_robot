import plotly
from plotly.graph_objs import Scatter, Layout

# plotly.offline.plot({
#     "data": [Scatter(x=[1, 2, 3, 4], y=[4, 3, 2, 1])],
#     "layout": Layout(title="hello world")
# })



# from plotly.offline import init_notebook_mode, iplot
# from IPython.display import display, HTML
import numpy as np



# t=np.linspace(-1,1,100)
# x=t+t**2
# y=t-t**2
x = [1,2,2,1]
y = [1,1,2,2]

xm=np.min(x)-1.5
xM=np.max(x)+1.5
ym=np.min(y)-1.5
yM=np.max(y)+1.5
N=50
# s=np.linspace(-1,1,N)
xx=x
yy=y


data=[dict(x=x, y=y, 
           mode='lines', 
           line=dict(width=2, color='blue')
          ),
      dict(x=x, y=y, 
           mode='lines', 
           line=dict(width=2, color='blue')
          )
    ]

layout=dict(xaxis=dict(range=[xm, xM], autorange=False, zeroline=False),
            yaxis=dict(range=[ym, yM], autorange=False, zeroline=False),
            title='Kinematic Generation of a Planar Curve', hovermode='closest',
            updatemenus= [{'type': 'buttons',
                           'buttons': [{'label': 'Play',
                                        'method': 'animate',
                                        'args': [None]}]}])

frames=[dict(data=[dict(x=[xx[k]], 
                        y=[yy[k]], 
                        mode='markers', 
                        marker=dict(color='red', size=10)
                        )
                  ]) for k in range(4)]    
          
figure1=dict(data=data, layout=layout, frames=frames)          
plotly.offline.plot(figure1)
