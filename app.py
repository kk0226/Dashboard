# -*- coding: utf-8 -*-
"""
Created on Thu Dec  1 07:48:33 2022

@author: Phoenix
"""
"""
import os
import sys
path = "/Users/Phoenix/Documents/2022 FAll/MA 705/Dashboard/github"
os.chdir(path)
os.getcwd()
"""

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
state = state.rename(columns={'Employment': 'Employed person'})
state_new = state[['Area Name','Employed person','Employment per 1,000 jobs', 
                   'Hourly mean wage','Annual mean wage']]
state_new = pd.melt(state_new, id_vars="Area Name")
state_new = pd.merge(state_new, code, left_on="Area Name", right_on="state")
state_new = state_new[['Area Name', 'variable', 'value', 'abbreviation']]
industry = pd.read_csv('employment by industry.csv')
industry_new = pd.melt(industry, id_vars="Industry")


stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=stylesheet,
                prevent_initial_callbacks=True)
server = app.server

app.layout = html.Div([
    html.H1('Data Scientist Query Site',
            style = {'textAlign':'center','color':'rgb(0, 59, 115)'}),
    html.H3('Dashboard Summary',
            style = {'textAlign':'left','color':'rgb(0, 59, 115)'}),
    html.H6('The Dashboard is built to help data scientists and prospective data scientists to find a better place in working area.',
            style = {'textAlign':'left'}),
    html.H6('- Users can query the information related to the job, including the Number of Employed People, Hourly Mean Wage, and Annually Mean Wage.',
            style = {'textAlign':'left'}),
    html.H6('- Data scientists can utilize such information to help to position themselves against the indudstry.',
            style = {'textAlign':'left'}),
    html.H6('- Prospective data scientists can utilize such information to compare the benefit and competition between desirable industries.',
            style = {'textAlign':'left'}),
    html.Br(),
    html.H3("Users' Guide",
            style = {'textAlign':'left','color':'rgb(0, 59, 115)'}),
    html.H6("> Users can use the interactive datatable to filter, sort, or/and hide the rows by clicking near to the column's name or/and type in the row belowed the column.",
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.H6("> Users can use the interactive datatable to hide the needless columns by clicking the button 'TOGGLE COLUMNS.'",
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.H6('> Users can use the dropdown menu to modify the required variables they are comparing.',
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.H6('- For instance, users can compare the Hourly Mean Wage among states or industries according to differnet sections.',
            style = {'textAlign':'left'}),
    html.H6('> Users can use check boxs in the interactive datatable to hightlight the selected bar in the bar chart after modifying the dropdown menu.',
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.H6('> Users can check multiple check box at the same time.',
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.H6('- The highlighted bars can help to gauge the position among the whole distribution.',
            style = {'textAlign':'left'}),
    html.H6('- For instance, users can check the California and observe that it has the largest number of Employed Person.',
            style = {'textAlign':'left'}),
    html.H6('> Users can move mouse to the bar / geographic area in the figure to check specific measures for the given variable.',
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.H2('Query by States',
            style = {'textAlign':'left','color':'rgb(0, 59, 115)'}),
    html.H5('The following table shows the selected information of data scientist by states.',
            style = {'textAlign':'left'}),
    html.H5('The check box will highlight the bar shown in the graph below:',
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
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal',
            'textAlign': 'left'}
    ),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="slct_variable",
                 options=[
                     {"label": "Employed person", 
                      "value": "Employed person"},
                     {"label": "Employment per 1,000 jobs",
                          "value": "Employment per 1,000 jobs"},
                     {"label": "Hourly mean wage", "value": "Hourly mean wage"},
                     {"label": "Annual mean wage", "value": "Annual mean wage"}],
                 multi=False,
                 style={'width': "40%"},
                 clearable=False,
                 placeholder="Select a variable"
                 ),
    html.H6(id='bar_output_container', children=[],
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.Br(),
    html.Br(),
    dcc.Graph(id='bar', figure={}),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="slct_variable1",
                 options=[
                     {"label": "Employed person", "value": "Employed person"},
                     {"label": "Employment per 1,000 jobs",
                          "value": "Employment per 1,000 jobs"},
                     {"label": "Hourly mean wage", "value": "Hourly mean wage"},
                     {"label": "Annual mean wage", "value": "Annual mean wage"}],
                 multi=False,
                 style={'width': "40%"},
                 clearable=False,
                 placeholder="Select a variable"
                 ),

    html.H6(id='geo_output_container', children=[],
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.Br(),

    dcc.Graph(id='geo', figure={}),
    html.Br(),
    html.Br(),
    html.H2('Query by Industries',
            style = {'textAlign':'left','color':'rgb(0, 59, 115)'}),
    html.H5('The following table shows the selected information of data scientist by industries.',
            style = {'textAlign':'left'}),
    html.H5('The check box will highlight the bar shown in the graph below:',
            style = {'textAlign':'left'}),
    dash_table.DataTable(
        id='datatable-interactivity2',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True, "hideable": False}
            if i == 'Industry'
            else {"name": i, "id": i, "deletable": False, "selectable": True,"hideable": True}
            for i in industry.columns
        ],
        data=industry.to_dict('records'),  
        editable=False,             
        filter_action="native",     
        sort_action="native",      
        sort_mode="multi",        
        column_selectable=False,  
        row_selectable="multi",   
        row_deletable=False,         
        selected_columns=[],        
        selected_rows=[],           
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
            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
            'whiteSpace': 'normal',
            'textAlign': 'left'}
    ),
    html.Br(),
    html.Br(),
    dcc.Dropdown(id="slct_variable2",
                 options=[
                     {"label": "Employed person", "value": "Employed person"},
                     {"label": "Percent of industry employment",
                          "value": "Percent of industry employment"},
                     {"label": "Hourly mean wage", "value": "Hourly mean wage"},
                     {"label": "Annual mean wage", "value": "Annual mean wage"}],
                 multi=False,
                 style={'width': "40%"},
                 clearable=False,
                 placeholder="Select a variable"
                 ),
    html.H6(id='bar_output_container2', children=[],
            style = {'textAlign':'left','color':'rgb(210, 43, 43)'}),
    html.Br(),
    html.Br(),
    dcc.Graph(id='bar2', figure={}),
    html.Br(),
    html.Br(),
    dcc.Markdown('''
        #### Support Documentation and Acknowlegement
        This dashboard is made by Phoenix Qi at Bentley University under the Guidance
        of Professor Luke Cherveny. Data are acquired from the U.S. Bureau of Labor
        Statistics. Thanks for your interest. 
    '''),
    dcc.Markdown('''
          If you are interested in Bentley 
          University or Professor Luke, please use the link here below: 
          [Bentley University](https://www.bentley.edu/) and 
          [Professor Luke](http://lukecherveny.com/).
    ''')
])

# bar chart
@app.callback(
    [Output(component_id='bar_output_container', component_property='children'),
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

    colors = ['rgb(210, 43, 43)' if i in slctd_rows else '#0074D9'
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
    [Output(component_id='geo_output_container', component_property='children'),
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
        template="plotly_dark",
        title=f'{option_slctd1} by States'
    )
    
    return container, fig1

# bar chart 2
@app.callback(
    [Output(component_id='bar_output_container2', component_property='children'),
     Output(component_id='bar2', component_property='figure')],
    [Input(component_id='slct_variable2', component_property='value'),
     Input(component_id='datatable-interactivity2', component_property='derived_virtual_selected_rows'),
     Input(component_id='datatable-interactivity2', component_property='derived_virtual_selected_row_ids'),
     Input(component_id='datatable-interactivity2', component_property='selected_rows'),
     Input(component_id='datatable-interactivity2', component_property='derived_virtual_indices'),
     Input(component_id='datatable-interactivity2', component_property='derived_virtual_row_ids'),
     Input(component_id='datatable-interactivity2', component_property='active_cell'),
     Input(component_id='datatable-interactivity2', component_property='selected_cells')]
)
def update_graph2(option_slctd, slctd_row_indices,
                slct_rows_names, slctd_rows,
               order_of_rows_indices, order_of_rows_names,
               actv_cell, slctd_cell):
    print(option_slctd)
    print(type(option_slctd))

    container = "The Variable chosen by user was: {}".format(option_slctd)

    industry_new1 = industry_new.copy()
    industry_new1 =  industry_new1[ industry_new1["variable"] == option_slctd]

    colors = ['rgb(210, 43, 43)' if i in slctd_rows else '#0074D9'
              for i in range(len(industry_new1))]
    # Plotly Express
    fig3 = px.bar(
            data_frame =  industry_new1,
            x = 'Industry',
            y = 'value',
            title=f'{option_slctd} by Industry',
            hover_data=['Industry', 'value'],
            template="plotly_dark"
        ).update_traces(marker_color=colors).update_layout(showlegend=False, xaxis={'categoryorder': 'total ascending'})
    
    return container, fig3



if __name__ == '__main__':
    app.run_server(debug=True)
    
    
  
