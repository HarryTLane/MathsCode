'''
Create an interactive dashboard where users can adjust parameters of the random walk and see the results in real time using libraries like Plotly or Panel.

For an interactive visualisation start with the Panel or Plotly libraries which integrate well with Python.

Create sliders for parameters like:
- number of steps
- bias probability
- number of walkers
- dimensions

Use callback functions to update the visualisation when parameters change. This extension gives excellent practice with modern data visualisation
techniques and creates an engaging way to present findings.

'''

import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Function to generate random walk data
def generate_random_walk(steps, walkers, bias, dimensions):
    walks = []
    for _ in range(walkers):
        walk = np.zeros((steps, dimensions))
        for step in range(1, steps):
            step_direction = np.random.choice([-1, 1], size=dimensions, p=[1-bias, bias])
            walk[step] = walk[step - 1] + step_direction
        walks.append(walk)
    return walks

# Initialize Dash app
app = Dash(__name__)

STEP_SLIDER_MARKS = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
BIAS_SLIDER_MARKERS = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
NUMBER_OF_WALKERS_SLIDER_MARKERS = list(range(1, 11, 1))
DIMENSIONS_SLIDER_MARKERS = [1, 2, 3]

# Layout with sliders for parameters
app.layout = html.Div([
    html.H1("Random Walk Simulation"),
    dcc.Graph(id='random-walk-plot'),
    html.Label(id='steps-label', children="Number of Steps:"),
    dcc.Slider(
        id='steps-slider', 
        min=10, 
        max=1000, 
        step=10, 
        value=100,
        marks={i: str(i) for i in STEP_SLIDER_MARKS},
        updatemode="drag"  # Update label while moving the slider
    ),
    html.Label(id='bias-label', children="Bias Probability:"),
    dcc.Slider(
        id='bias-slider', 
        min=0.0, 
        max=1.0, 
        step=0.01, 
        value=0.5,
        marks={i: str(i) for i in BIAS_SLIDER_MARKERS},
        updatemode="drag"  # Update label while moving the slider
    ),
    html.Label(id='walkers-label', children="Number of Walkers:"),
    dcc.Slider(
        id='walkers-slider', 
        min=1, 
        max=10, 
        step=1, 
        value=1,
        marks={i: str(i) for i in NUMBER_OF_WALKERS_SLIDER_MARKERS},
        updatemode="drag"  # Update label while moving the slider
    ),
    html.Label(id='dimensions-label', children="Dimensions:"),
    dcc.Slider(
        id='dimensions-slider', 
        min=1, 
        max=3, 
        step=1, 
        value=2,
        marks={i: str(i) for i in DIMENSIONS_SLIDER_MARKERS},
        updatemode="drag"  # Update label while moving the slider
    )
])

# Callback to update slider labels
@app.callback(
    Output('steps-label', 'children'),
    Input('steps-slider', 'value')
)
def update_steps_label(value):
    return f"Number of Steps: {value}"

@app.callback(
    Output('bias-label', 'children'),
    Input('bias-slider', 'value')
)
def update_bias_label(value):
    return f"Bias Probability: {value:.2f}"

@app.callback(
    Output('walkers-label', 'children'),
    Input('walkers-slider', 'value')
)
def update_walkers_label(value):
    return f"Number of Walkers: {value}"

@app.callback(
    Output('dimensions-label', 'children'),
    Input('dimensions-slider', 'value')
)
def update_dimensions_label(value):
    return f"Dimensions: {value}"


# Callback to update the plot
@app.callback(
    Output('random-walk-plot', 'figure'),
    Input('steps-slider', 'value'),
    Input('bias-slider', 'value'),
    Input('walkers-slider', 'value'),
    Input('dimensions-slider', 'value')
)
def update_plot(steps, bias, walkers, dimensions):
    walks = generate_random_walk(steps, walkers, bias, dimensions)
    fig = go.Figure()
    for i, walk in enumerate(walks):
        if dimensions == 1:
            fig.add_trace(go.Scatter(y=walk[:, 0], mode='lines', name=f'Walker {i+1}'))
        elif dimensions == 2:
            fig.add_trace(go.Scatter(x=walk[:, 0], y=walk[:, 1], mode='lines', name=f'Walker {i+1}'))
        elif dimensions == 3:
            fig.add_trace(go.Scatter3d(x=walk[:, 0], y=walk[:, 1], z=walk[:, 2], mode='lines', name=f'Walker {i+1}'))
    fig.update_layout(title="Random Walk Simulation", showlegend=True)
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


