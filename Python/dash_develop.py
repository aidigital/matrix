from main import sort_venues

# the dash packages are in the requirements.txt file, but also you can find them here: https://plot.ly/dash/getting-started#installation
import dash
import dash_core_components as dcc
import dash_html_components as html

my_app = dash.Dash('my app')

my_app.layout = html.Div(children=[
    html.H1(children='Where Can We Go Out'),

    html.Label('INPUT people going out:'),
    dcc.Checklist(
        options=[
            {'label': 'John Davis', 'value': 'John Davis'},
            {'label': 'Gary Jones', 'value': 'Gary Jones'},
            {'label': 'Robert Webb', 'value': 'Robert Webb'},

            {'label': 'Gavin Coulson', 'value': 'Gavin Coulson'},
            {'label': 'Alan Allen', 'value': 'Alan Allen'},
            {'label': 'Bobby Robson', 'value': 'Bobby Robson'},
            {'label': 'David Lang', 'value': 'David Lang'}
          ],
          values=['John Davis', 'Gary Jones', 'Robert Webb', 'Gavin Coulson', 'Alan Allen', 'Bobby Robson','David Lang'],
          id='id_of_checklist'
    ),

    html.Label('INPUT venues open:'),
    dcc.Checklist(
        options=[
            {'label': 'El Cantina', 'value': 'El Cantina'},
            {'label': 'Twin Dynasty', 'value': 'Twin Dynasty'},
            {'label': 'Spice of life', 'value': 'Spice of life'},

            {'label': 'The Cambridge', 'value': 'The Cambridge'},
            {'label': 'Wagamama', 'value': 'Wagamama'},
            {'label': 'Sultan Sofrasi', 'value': 'Sultan Sofrasi'},

            {'label': 'Spirit House', 'value': 'Spirit House'},
            {'label': 'Tally Joe', 'value': 'Tally Joe'},
            {'label': 'Fabrique', 'value': 'Fabrique'}
        ],
        values=['El Cantina', 'Twin Dynasty', 'Spice of life', 'The Cambridge', 'Wagamama', 'Sultan Sofrasi', 'Spirit House', 'Tally Joe', 'Fabrique'],
        id='id_of_venues'
    ),

    html.Label('OUTPUT:'),
    html.Div(id='display_applicable_venues'), # -> returns the names of the venues where everyone can go
    html.Div(id='display_inapplicable_venues'), # -> returns the names of the venues where the group can't go

    html.Div(id='display_reasons_dataframe') # -> returns a dataframe listing the reasons why a venue doesn't suit someone

]
)

# -> returns the names of the venues where everyone can go
@my_app.callback(dash.dependencies.Output('display_applicable_venues', 'children'),
                 [dash.dependencies.Input('id_of_checklist', 'values'),
                  dash.dependencies.Input('id_of_venues', 'values')] )
def returner(id_of_checklist, id_of_venues):
    return sort_venues(people_going_out=id_of_checklist,
                venues_open=id_of_venues,
                explain_reason=False,
                returned_message='applicable_venues_message')

# -> returns the names of the venues where the group can't go
@my_app.callback(dash.dependencies.Output('display_inapplicable_venues', 'children'),
                 [dash.dependencies.Input('id_of_checklist', 'values'),
                  dash.dependencies.Input('id_of_venues', 'values')] )
def returner(id_of_checklist, id_of_venues):
    return sort_venues(people_going_out=id_of_checklist,
                venues_open=id_of_venues,
                explain_reason=False,
                returned_message='inapplicable_venues_message')


# -> returns a dataframe listing the reasons why a venue doesn't suit someone
@my_app.callback(dash.dependencies.Output('display_reasons_dataframe', 'children'),
                 [dash.dependencies.Input('id_of_checklist', 'values'),
                  dash.dependencies.Input('id_of_venues', 'values')] )
def generate_table(id_of_checklist, id_of_venues, max_rows=100):
    dataframe = sort_venues(people_going_out=id_of_checklist,
                venues_open=id_of_venues,
                explain_reason=False,
                returned_message='inapplicable_venues_message',
                return_reasons_dataframe=True)

    return html.Table(
            # Header
            [html.Tr([html.Th(col) for col in dataframe.columns])] +

            # Body
            [html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
           )

if __name__ == '__main__':
    my_app.run_server(debug=True)