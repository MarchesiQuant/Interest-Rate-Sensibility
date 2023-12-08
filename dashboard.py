import numpy as np
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from bond_funcs import price, sensibility, convexity, duration

# Set initial bond parameters 
n = 20
c = 0.04
A = 1000
y = 0.05
delta_y = np.arange(-0.05, 0.05, 0.0005)
y_range = np.arange(0, 0.1, 0.00001)

# Initial calculation
delta = sensibility(n, c, A, y, delta_y)
B = price(n, c, A, y_range)
C = convexity(n,c,A,y)
D = duration(n,c,A,y)

# Create Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div(style={'backgroundColor': '#f5f5f5', 'color': '#333', 'padding': '20px'}, children=[

    html.H1("Bond Sensitivity Dashboard", style={'fontSize': '50px'}),
    
    # Input sliders
    html.Label("Select Bond Parameters: ", style={'fontSize': '30px', 'marginBottom': '1px'}),
    
    html.Div([
        html.Label("Maturity (years): ", style={'fontSize': '16px'}),
        dcc.Input(id='maturity-input', type='number', value=n, step=1, min=1, max=50, placeholder="Enter Maturity"),
    ]),
    html.Div([
        html.Label("Coupon Rate (%): ", style={'fontSize': '16px'}),
        dcc.Input(id='coupon-input', type='number', value=c, step=0.001, min=0, max=1, placeholder="Enter Coupon Rate"),
    ]),
    html.Div([
        html.Label("Principal ($): ", style={'fontSize': '16px'}),
        dcc.Input(id='principal-input', type='number', value=A, step=10, min=0, max=100000, placeholder="Enter Principal"),
    ]),
    html.Div([
        html.Label("Discount Rate (%): ", style={'fontSize': '16px'}),
        dcc.Input(id='rate-input', type='number', value=y, step=0.001, min=0, max=1, placeholder="Enter Discount Rate"),
    ]),

    # Calculation boxes for the first graph
    html.Div([
        html.P(id='duration-box', children=f"Duration: {D}"),
    ], style={'marginBottom': '10px', 'fontSize': '18px', 'fontWeight': 'bold'}),

    html.Div([
        html.P(id='convexity-box', children=f"Convexity: {C}"),
    ], style={'marginBottom': '5px','fontSize': '18px', 'fontWeight': 'bold'}),

    # Graphs
    html.Label("Second-Order Approximation of Bond Price Movements", style={'fontSize': '30px', 'marginBottom': '1px'}),
    dcc.Graph(id='bond-sensitivity-chart', style={'margin': 'auto', 'textAlign': 'center'}),
    html.Label("Bond Price for Different Interest Rates", style={'fontSize': '30px', 'marginBottom': '1px'}),
    dcc.Graph(id='bond-value-chart'),
])


# Define callback to update the first graph
@app.callback(
    Output('bond-sensitivity-chart', 'figure'),
    [Input('maturity-input', 'value'),
     Input('coupon-input', 'value'),
     Input('principal-input', 'value'),
     Input('rate-input', 'value')]
)
def update_graph_1(maturity, coupon, principal, rate):
    delta_y_range = np.arange(-0.05, 0.05, 0.0005)
    risk = sensibility(maturity, coupon, principal, rate, delta_y_range)
    
    fig = px.line(x= 10000*delta_y_range, y=risk, labels={'x': 'Change in Interest Rates (bps)', 'y': 'Price Change (%)'},
                  title=f'{maturity} year bond with {round(100 * coupon, 2)}% coupon at {round(100 * rate, 2)}% interest rate')
    
    fig.update_layout(yaxis_tickformat='%')
    fig.update_yaxes(tickformat=".2%")
    fig.update_layout(paper_bgcolor='#f5f5f5')
    return fig

# Define callback to update the second graph
@app.callback(
    Output('bond-value-chart', 'figure'),
    [Input('maturity-input', 'value'),
     Input('coupon-input', 'value'),
     Input('principal-input', 'value')]
)
def update_graph_2(maturity, coupon, principal):
    y_range = np.arange(0, 0.1, 0.00001)
    bond_values = price(maturity, coupon, principal, y_range)
    
    fig = px.line(x=y_range, y=bond_values, labels={'x': 'Interest Rate', 'y': 'Bond Value ($)'},
                  title=f'{maturity} year bond with {round(100 * coupon, 2)}% coupon')
    
    fig.update_layout(xaxis_tickformat='%')
    fig.update_xaxes(tickformat=".2%")
    fig.update_layout(paper_bgcolor='#f5f5f5')
    return fig

# Define callback to update the calculation boxes
@app.callback(
    [Output('duration-box', 'children'),
     Output('convexity-box', 'children')],
    [Input('maturity-input', 'value'),
     Input('coupon-input', 'value'),
     Input('principal-input', 'value'),
     Input('rate-input', 'value')]
)

def update_calculation_boxes(maturity, coupon, principal, rate):
    C = convexity(maturity,coupon,principal,rate)
    D = duration(maturity,coupon,principal,rate)
    duration_text = f"Duration: {round(D,2)}"
    convexity_text = f"Convexity: {round(C,2)}"
    return duration_text, convexity_text

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
