# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 07:48:33 2022

@author: Phoenix
"""
#import os
#import sys
#path = "/Users/Phoenix/Documents/2022 FAll/MA 705/Dashboard/github"
#os.chdir(path)
#os.getcwd()

import dash
from dash import dcc
from dash.dependencies import Input, Output
import dash_table
import dash_html_components as html
import plotly.express as px
import pandas as pd
state = pd.read_csv("salary_by_state.csv")
code = pd.read_csv("state-abbrevs.csv")
state = state[['Area Name','Employment', 'Hourly mean wage','Annual mean wage',
            'Hourly 25th percentile wage', 'Hourly median wage',
            'Hourly 75th percentile wage','Annual 25th percentile wage',
            'Annual median wage', 'Annual 75th percentile wage',
            'Employment per 1,000 jobs']]
state_new = state[['Area Name','Employment','Employment per 1,000 jobs', 
                   'Hourly mean wage','Annual mean wage']]
state_new = pd.melt(state_new, id_vars="Area Name")
state_new = pd.merge(state_new, code, left_on="Area Name", right_on="state")
state_new = state_new[['Area Name', 'variable', 'value', 'abbreviation']]


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheet,
                prevent_initial_callbacks=True)
server = app.server

app.layout = html.Div([
    html.H1('Data Scientist Query Site',
            style = {'textAlign':'center'}),
    html.H3('Query by States',
            style = {'textAlign':'left'}),
    html.H5('The following tables shows the selected information of data scientist by states',
            style = {'textAlign':'left'}),
    dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == 'Area Name'
            else {"name": i, "id": i, "deletable": False, "selectable": True,"hideable": True}
            for i in state.columns
        ],
        data=state.to_dict('records'),  
        editable=False,             
        filter_action="native",     
        sort_action="native",      
        sort_mode="multi",        
        column_selectable=False,  
        row_selectable="multi",   
        row_deletable=False,         
        selected_columns=[],        
        selected_rows=[],           
        page_action="native",       
        style_cell_conditional=[
        {'if': {'column_id': c},
         'textAlign': 'left'
        } for c in ['Date', 'Region']
        ],
        style_data={
        'color': 'black',
        'backgroundColor': 'white',
        'whiteSpace': 'normal',
        'height': 'auto',
        'border': '1px solid blue'
        },
        style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(167, 199, 231)',
        }
        ],
        style_header={
        'backgroundColor': 'rgb(240, 255, 255)',
        'color': 'rgb(65, 105, 225)',
        'font': 'Lato, sans-serif',
        'fontWeight': 'bold',
        'border': '1px solid blue' 
         },
        style_as_list_view=True,
        fixed_rows={'headers': True},
        style_table={'overflowX': 'auto'},
        style_cell={
            'height': 'auto',
            # all three widths are needed
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal'}
    ),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="slct_variable",
                 options=[
                     {"label": "Employment", "value": "Employment"},
                     {"label": "Employment per 1,000 jobs",
                          "value": "Employment per 1,000 jobs"},
                     {"label": "Hourly mean wage", "value": "Hourly mean wage"},
                     {"label": "Annual mean wage", "value": "Annual mean wage"}],
                 multi=False,
                 value="Employment",
                 style={'width': "40%"}
                 ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    html.Br(),
    dcc.Graph(id='bar', figure={}),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="slct_variable1",
                 options=[
                     {"label": "Employment", "value": "Employment"},
                     {"label": "Employment per 1,000 jobs",
                          "value": "Employment per 1,000 jobs"},
                     {"label": "Hourly mean wage", "value": "Hourly mean wage"},
                     {"label": "Annual mean wage", "value": "Annual mean wage"}],
                 multi=False,
                 value="Employment",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container1', children=[]),
    html.Br(),

    dcc.Graph(id='geo', figure={})
])

# bar chart
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bar', component_property='figure')],
    [Input(component_id='slct_variable', component_property='value'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity', component_property='selected_rows'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity', component_property='active_cell'),
     Input(component_id='datatable-interactivity', component_property='selected_cells')]
)
def update_graph(option_slctd, slctd_row_indices,
                slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names,
               actv_cell, slctd_cell):
    print(option_slctd)
    print(type(option_slctd))

    container = "The Variable chosen by user was: {}".format(option_slctd)

    state_new2 = state_new.copy()
    state_new2 = state_new2[state_new2["variable"] == option_slctd]

    colors = ['#7FDBFF' if i in slctd_rows else '#0074D9'
              for i in range(len(state_new2))]
    # Plotly Express
    fig = px.bar(
            data_frame = state_new2,
            x = 'Area Name',
            y = 'value',
            title=f'{option_slctd} by States',
            hover_data=['Area Name', 'value'],
            template="plotly_dark"
        ).update_traces(marker_color=colors).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
    
    return container, fig

# map
@app.callback(
    [Output(component_id='output_container1', component_property='children'),
     Output(component_id='geo', component_property='figure')],
    [Input(component_id='slct_variable1', component_property='value')]
)

def update_graph1(option_slctd1):
    print(option_slctd1)
    print(type(option_slctd1))

    container = "The Variable chosen by user was: {}".format(option_slctd1)

    state_new1 = state_new.copy()
    state_new1 = state_new1[state_new1["variable"] == option_slctd1]

    fig1 = px.choropleth(
        data_frame=state_new1,
        locationmode='USA-states',
        locations='abbreviation',
        scope="usa",
        color='value',
        hover_data=['Area Name', 'value'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        template="plotly_dark"
    )
    
    return container, fig1


if __name__ == '__main__':
    app.run_server(debug=True)