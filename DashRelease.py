import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Загрузка данных
df = pd.read_csv(r'C:\Users\xolox\PycharmProjects\pythonProject\csvdash.csv')

# Создание экземпляра приложения
app = dash.Dash(__name__)

# Определение структуры дашборда
app.layout = html.Div([
    html.Div([
        html.H1('Дашборд  для анализа финансовых данных', style={'textAlign': 'center'}),
        html.P('Этот дашборд предоставляет аналитику ваших финансовых данных.',
               style={'textAlign': 'center'}),
        html.Div([
            html.Label('Выберите дату:', style={'fontSize': 18}),
            dcc.Dropdown(
                id='date-dropdown',
                options=[{'label': date, 'value': date} for date in df['Дата']],
                value=df['Дата'].iloc[0],
                clearable=False,
                style={'width': '50%', 'margin': '0 auto'}
            ),
        ], style={'textAlign': 'center', 'marginBottom': '30px'}),
    ], style={'marginBottom': '30px'}),

    html.Div([
        # Линейный график
        dcc.Graph(id='line-chart'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Гистограмма
        dcc.Graph(id='histogram'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Круговая диаграмма
        dcc.Graph(id='pie-chart'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Ящик с усами
        dcc.Graph(id='box-plot'),
    ], style={'width': '48%', 'display': 'inline-block'}),

    html.Div([
        # Точечный график
        dcc.Graph(id='scatter-plot'),
    ], style={'width': '48%', 'display': 'inline-block'}),

], style={'padding': '20px'})

# Определение логики дашборда
@app.callback(
    Output('line-chart', 'figure'),
    Output('histogram', 'figure'),
    Output('pie-chart', 'figure'),
    Output('box-plot', 'figure'),
    Output('scatter-plot', 'figure'),
    [Input('date-dropdown', 'value')]
)
def update_charts(selected_date):
    # Линейный график
    line_chart = go.Figure(go.Scatter(x=df['Время'], y=df['Доходы']))
    line_chart.update_layout(title='Линейный график',
                             xaxis_title='Время',
                             yaxis_title='Доходы',
                             plot_bgcolor='rgb(230, 230, 230)')

    # Гистограмма
    histogram = go.Figure(go.Histogram(x=df['Активы']))
    histogram.update_layout(title='Гистограмма',
                            xaxis_title='',
                            yaxis_title='',
                            plot_bgcolor='rgb(230, 230, 230)')

    # Круговая диаграмма - доходы
    pie_chart = px.pie(df, names='Активы', values='Доходы',
                       title='Круговая диаграмма')

    # Ящик с усами
    box_plot = px.box(df, x='Активы', y='Доходы',
                      title='box-plot')

    # Точечный график
    scatter_plot = px.scatter(df, x='Доходы', y='Расходы',
                             title='Точечный график')

    return line_chart, histogram, pie_chart, box_plot, scatter_plot

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)

'''
Дата,Время,Расходы,Доходы,Активы
2020-06-16,2:00,989248,11200,Акции
2020-07-17,3:00,122000,120,Облигации
2020-07-18,2:00,989248,11200,Акции
2020-07-19,3:00,122000,120,Облигации
2022-11-23,12:18,116896,2719,Драгоценности
2023-05-07,20:38,175200,6981,Драгоценности
2023-08-09,18:29,16648,2414,Акции
2023-08-12,3:55,30302,11994,Облигации
2023-08-13,16:29,46433,18202,Драгоценности
2023-08-19,12:59,93577,13414,Недвижимость
2023-08-28,17:34,183809,19365,Акции
2023-09-24,18:17,163313,723,Недвижимость
'''