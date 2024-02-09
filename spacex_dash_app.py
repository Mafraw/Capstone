# Import required libraries
#python3.8 -m pip install pandas dash
#Get CSV file:
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#get skeleton:
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_3/spacex_dash_app.py"
#run app
#python3.8 spacex_dash_app.py


import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
l_sites = spacex_df['Launch Site'].unique()
l_sites = np.append(l_sites,'All')
print(l_sites)
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',options = l_sites, value='All'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div(dcc.RangeSlider(id='payload-slider', min=0, max=10000, step=1000)),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == "All":
        df = spacex_df.groupby("Launch Site", as_index = False).agg({"class":"sum"})
        fig = px.pie(df, values='class', names='Launch Site', title='Launches by site')
        return fig
    else:
        df = spacex_df[spacex_df['Launch Site'] == entered_site].groupby("class", as_index = False).agg({"Launch Site":"count"})
        fig = px.pie(df, values='Launch Site', names='class', title='Successful vs failed')
        return fig       

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure')
              ,Input(component_id='site-dropdown', component_property='value')
              ,Input(component_id="payload-slider", component_property="value")
              )

def get_success_payload_scatter_chart(site_dropdown,payload_slider):
    if site_dropdown == "All":
        df1 = spacex_df[ (spacex_df['Payload Mass (kg)']>=payload_slider[0]) & (spacex_df['Payload Mass (kg)']<=payload_slider[1])]
    else:
        df1 = spacex_df[(spacex_df['Launch Site'] == site_dropdown ) & ( spacex_df['Payload Mass (kg)']>=payload_slider[0] ) & (spacex_df['Payload Mass (kg)']<=payload_slider[1])]
    fig = px.scatter(df1, x="Payload Mass (kg)", y="class", color="Booster Version Category")
    print(payload_slider[0])
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
