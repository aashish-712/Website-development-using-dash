import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash
from dash import html, dcc, Input, Output

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

patients = pd.read_csv('IndividualDetails.csv')
patients['current_status'].value_counts()
Total= patients.shape[0]
Active = patients[patients['current_status'] == "Hospitalized"].shape[0]
recovered = patients[patients['current_status'] == "Recovered"].shape[0]
deceased = patients[patients['current_status'] == "Deceased"].shape[0]

options =[
    {"label" : "All", "value" : "All"},
    {"label": "Hospitalized", "value" : "Hospitalized"},
    {"label" : "Recovered", "value" : "Recovered"},
    {"label": "Deceased", "value" : "Deceased"},

]

age = pd.read_csv("AgeGroupDetails.csv")

covid = pd.read_csv("covid_19_india.csv")
covid_df = covid.groupby("Date")["Confirmed"].sum().reset_index()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server= app.server

app.layout = html.Div([
    html.H1("Corona Virus - India's Prespective", style= {"color": "#fff", "text-align": "center"}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className= "text-light"),
                    html.H4(Total, className= "text-light")
                ], className= "card-body")
            ], className= "card, bg-danger")
        ], className= "col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active", className= "text-light"),
                    html.H4(Active, className= "text-light")
                ], className= "card-body")
            ], className= "card, bg-primary")
        ], className= "col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered",className="text-light"),
                    html.H4(recovered,className="text-light")
                ], className= "card-body")
            ], className= "card, bg-warning")
        ], className= "col-md-3"),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className= "text-light"),
                    html.H4(deceased, className= "text-light")
                ], className= "card-body")
            ], className= 'card, bg-success')
        ], className= "col-md-3")
    ], className= "row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([dcc.Graph(
                    id= "Pie",
                    figure={
                        "data": [go.Pie(labels= age['AgeGroup'], values= age['TotalCases'])],
                        "layout": go.Layout(title= "Pie Chart of Distribution of Age")
                    }
                )], className= "card-body")
            ], className= "card")
        ], className= "col-md-6"),
                html.Div([
                    html.Div([
                        html.Div([
                            dcc.Graph(
                                figure= {
                                    "data" : [go.Scatter(x=covid_df["Date"], y= covid_df["Confirmed"], mode= "markers+lines")],
                                    "layout" : go.Layout(title= "Line Plot of Day by Day analysis of Corona Comfirmed Cases")
                                }
                            )
                        ], className= "card-body")
                    ], className= "card")
                ], className= "col-md-6")
    ], className= "row"),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id="picker", options=options , value="All"),
                    dcc.Graph(id="bar")
                ], className= "card-body")
            ], className= "card")
        ], className= "col-md-12")
    ], className= "row")
], className= "container")

@app.callback(Output("bar", "figure"), [Input("picker", "value")])
def update_graph(type):
    if  type == "All":
        pbar = patients["detected_state"].value_counts().reset_index()
        return {
            "data":[go.Bar(x= pbar['detected_state'], y= pbar['count'])],
            "layout" : go.Layout(title= "All States Total cases Bar Plot", xaxis ={"title": "States"}, yaxis= {"title" : "Total Cases "})
        }
    else :
        npat = patients[patients['current_status'] == type]
        pbar = npat["detected_state"].value_counts().reset_index()
        return {
                    "data":[go.Bar(x= pbar['detected_state'], y= pbar['count'])],
                    "layout" : go.Layout(title= "All States Total cases Bar Plot", xaxis ={"title": "States"}, yaxis= {"title" : "Total Cases "})

    
    }

if __name__ == "__main__":
    app.run(debug=True)