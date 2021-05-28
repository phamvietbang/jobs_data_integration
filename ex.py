import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from timing import timing
from index import Index
import pandas as pd
from collections import Counter
from dataclasses import dataclass
from analysis import analyze
from SearchEx import Experience_management
from SearchSa import SalaryManagement
import search
import read_data

# Hàm lọc theo giá trị cột Work Location
def findWorkLocation(d, label, data):
    dff = d[d[label].str.contains(data[0])]
    for i in range(len(data) - 1):
        dff = pd.concat([dff, d[d[label].str.contains(data[i + 1])]])
    return dff


# Hàm lọc theo giá trị cột types
def findTypes(d, label, data):
    k = []
    for j in range(len(data)):
        for i in d.index:
            if data[j] in d[label][i] and i not in k: k.append(i)
    if k != []:
        dff = df.iloc[k]
    else:
        dff = d
    return dff


# Hàm lọc theo search:
def searchItems(df, index, data):
    # print(f'Index contains {len(index.documents)} documents')
    search_result = index.search(data, search_type='AND', rank=True)
    dff = df.iloc[search_result]
    return dff



df = read_data.read_mongo(db='local', collection='alljob_final')

with open('./list_types.txt', mode='r', encoding='utf-8') as f:
    dtype = f.read().split('\n')
with open('./list_degree.txt', mode='r', encoding='utf-8') as f:
    ddegree = f.read().split('\n')
index = search.index_documents(search.load_documents(df), Index())
df1 = df.head(7000)
# page layout
app = dash.Dash(external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div(children=[
        html.Div(children=[
            # chưa làm được hàm search
            html.Label('Search'),
            dcc.Input(id='search', value='Kinh doanh Hà Nội', type='text'),
            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
            html.Label('Working_location'),
            dcc.Dropdown(
                id='location',
                # Nên sử dụng dạng sau:
                # options=[{'label': i, 'value': i} for i in available_indicators],
                options=[
                    {'label': 'An Giang', 'value': 'An Giang'},
                    {'label': 'Bà rịa – Vũng tàu', 'value': 'Bà rịa – Vũng tàu'},
                    {'label': 'Bắc Giang', 'value': 'Bắc Giang'},
                    {'label': 'Bắc Kạn', 'value': 'Bắc Kạn'},
                    {'label': 'Bạc Liêu', 'value': 'Bạc Liêu'},
                    {'label': 'Bắc Ninh', 'value': 'Bắc Ninh'},
                    {'label': 'Bến Tre', 'value': 'Bến Tre'},
                    {'label': 'Bình Định', 'value': 'Bình Định'},
                    {'label': 'Bình Dương', 'value': 'Bình Dương'},
                    {'label': 'Bình Phước', 'value': 'Bình Phước'},
                    {'label': 'Bình Thuận', 'value': 'Bình Thuận'},
                    {'label': 'Cà Mau', 'value': 'Cà Mau'},
                    {'label': 'Cần Thơ', 'value': 'Cần Thơ'},
                    {'label': 'Cao Bằng', 'value': 'Cao Bằng'},
                    {'label': 'Đà Nẵng', 'value': 'Đà Nẵng'},
                    {'label': 'Đắk Lắk', 'value': 'Đắk Lắk'},
                    {'label': 'Đắk Nông', 'value': 'Đắk Nông'},
                    {'label': 'Điện Biên', 'value': 'Điện Biên'},
                    {'label': 'Đồng Nai', 'value': 'Đồng Nai'},
                    {'label': 'Đồng Tháp', 'value': 'Đồng Tháp'},
                    {'label': 'Gia Lai', 'value': 'Gia Lai'},
                    {'label': 'Hà Giang', 'value': 'Hà Giang'},
                    {'label': 'Hà Nam', 'value': 'Hà Nam'},
                    {'label': u'Hà Nội', 'value': 'Hà Nội'},
                    {'label': 'Hà Tĩnh', 'value': 'Hà Tĩnh'},
                    {'label': 'Hải Dương', 'value': 'Hải Dương'},
                    {'label': 'Hải Phòng', 'value': 'Hải Phòng'},
                    {'label': 'Hậu Giang', 'value': 'Hậu Giang'},
                    {'label': 'Hòa Bình', 'value': 'Hòa Bình'},
                    {'label': 'Hưng Yên', 'value': 'Hưng Yên'},
                    {'label': 'Khánh Hòa', 'value': 'Khánh Hòa'},
                    {'label': 'Kiên Giang', 'value': 'Kiên Giang'},
                    {'label': 'Kon Tum', 'value': 'Kon Tum'},
                    {'label': 'Lai Châu', 'value': 'Lai Châu'},
                    {'label': 'Lâm Đồng', 'value': 'Lâm Đồng'},
                    {'label': 'Lạng Sơn', 'value': 'Lạng Sơn'},
                    {'label': 'Lào Cai', 'value': 'Lào Cai'},
                    {'label': 'Long An', 'value': 'Long An'},
                    {'label': 'Nam Định', 'value': 'Nam Định'},
                    {'label': 'Nghệ An', 'value': 'Nghệ An'},
                    {'label': 'Ninh Bình', 'value': 'Ninh Bình'},
                    {'label': 'Ninh Thuận', 'value': 'Ninh Thuận'},
                    {'label': 'Phú Thọ', 'value': 'Phú Thọ'},
                    {'label': 'Phú Yên', 'value': 'Phú Yên'},
                    {'label': 'Quảng Bình', 'value': 'Quảng Bình'},
                    {'label': 'Quảng Nam', 'value': 'Quảng Nam'},
                    {'label': 'Quảng Ngãi', 'value': 'Quảng Ngãi'},
                    {'label': 'Quảng Ninh', 'value': 'Quảng Ninh'},
                    {'label': 'Quảng Trị', 'value': 'Quảng Trị'},
                    {'label': 'Sóc Trăng', 'value': 'Sóc Trăng'},
                    {'label': 'Sơn La', 'value': 'Sơn La'},
                    {'label': 'Tây Ninh', 'value': 'Tây Ninh'},
                    {'label': 'Thái Bình', 'value': 'Thái Nguyên'},
                    {'label': 'Thái Nguyên', 'value': 'Thái Nguyên'},
                    {'label': 'Thanh Hóa', 'value': 'Thanh Hóa'},
                    {'label': 'Thừa Thiên Huế', 'value': 'Thừa Thiên Huế'},
                    {'label': 'Tiền Giang', 'value': 'Tiền Giang'},
                    {'label': 'Hồ Chí Minh', 'value': 'Hồ Chí Minh'},
                    {'label': 'Trà Vinh', 'value': 'Trà Vinh'},
                    {'label': 'Tuyên Quang', 'value': 'Tuyên Quang'},
                    {'label': 'Vĩnh Long', 'value': 'Vĩnh Long'},
                    {'label': 'Vĩnh Phúc', 'value': 'Vĩnh Phúc'},
                    {'label': 'Yên Bái', 'value': 'Yên Bái'},
                ],
                value="Hà Nội",
                multi=True
            ),
            html.Label('Type'),

            dcc.Dropdown(
                id='types',
                # Nên sử dụng dạng sau:
                options=[{'label': i, 'value': i} for i in dtype],
                value="Chăm Sóc Khách Hàng",
                multi=True
            ),

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
        html.Div(children=[
            html.Label('Salary'),
            'From ',
            dcc.Input(
                id="s1",
                value=1,
                type="number"
            ),
            ' to ',
            dcc.Input(
                id="s2",
                value=5,
                type="number",
                size='15'
            ),
            ' Triệu VNĐ',
            html.Label('Experience'),
            'From ',
            dcc.Input(
                id="e1",
                value=1,
                type="number"
            ),
            ' to ',
            dcc.Input(
                id="e2",
                value=5,
                type="number",
            ),
            ' Years',
            html.Label('Degree'),
            dcc.Dropdown(
                id='degree',
                options=[{'label': i, 'value': i} for i in ddegree],
                value='Không yêu cầu',
                multi=True
            ),

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '10%', 'margin-top': '3vw'}),
        html.Div(children=[
            html.Label('Gender'),
            dcc.RadioItems(
                id='gender',
                options=[
                    {'label': 'Nam', 'value': 'Nam'},
                    {'label': u'Nữ', 'value': 'Nữ'},
                    {'label': 'Không yêu cầu', 'value': 'Không yêu cầu'},
                ],
                value='Nữ',
                labelStyle={'display': 'block'}
            )

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
    ], className='row'),

    # second row
    html.Div(children=[
        html.H3(children='DATA JOB TABLE'),
        dash_table.DataTable(
            id='datatable-interactivity',
            style_data={
                'whiteSpace': 'normal',
            },
            data=df1.to_dict('records'),
            columns=[
                {"name": i, "id": i, } for i in df1.columns
            ],
            css=[{
                'selector': '.dash-spreadsheet td div',
                'rule': '''
								line-height: 15px;
								max-height: 30px; min-height: 30px; height: 30px;
								display: block;
								overflow-y: hidden;
						'''
            }],
            tooltip_data=[
                {
                    column: {'value': str(value), 'type': 'markdown'}
                    for column, value in row.items()
                } for row in df1.to_dict('records')
            ],
            tooltip_duration=None,

            style_cell={
                'textAlign': 'left',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'whiteSpace': 'normal',
                'minWidth': '80px', 'width': '80px', 'maxWidth': '80px',
            },
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            page_action="native",
            page_current=0,
            page_size=10,
        ),

    ], className='row', style={'display': 'inline-block', 'vertical-align': 'top'}),

])


# Hàm callback đưa ra dữ liệu sau mỗi lần lựa chọn thay đổi giá trị trong bảng
@app.callback(
    Output(component_id='datatable-interactivity', component_property='data'),
    Output(component_id='datatable-interactivity', component_property='tooltip_data'),
    Input(component_id='location', component_property='value'),
    Input(component_id='types', component_property='value'),
    Input(component_id='degree', component_property='value'),
    Input(component_id='gender', component_property='value'),
    Input(component_id='s1', component_property='value'),
    Input(component_id='s2', component_property='value'),
    Input(component_id='e1', component_property='value'),
    Input(component_id='e2', component_property='value'),
    Input('submit-button-state', 'n_clicks'),
    State('search', 'value'),
)
# def update_data(search_, location_, types_, degree_, experience_, gender_):
def update_data(location_, types_, degree_, gender_, s1, s2, e1, e2, n_click, search_):
    dff = df
    if search_ != '':
        dff = searchItems(dff, index, search_)
    if gender_ != '':
        dff = dff[dff['gender'] == gender_]
    if degree_ != '':
        dff = findTypes(dff, 'degree', degree_)
    if location_ != []:
        dff = findWorkLocation(dff, 'working_location', location_)
    if types_ != []:
        dff = findTypes(dff, 'types', types_)
    if e1 >= 0 and e2 >= 0:
        experience_management = Experience_management(dff)
        valid_records = experience_management.get_experience(e1, e2, 70000)
        if valid_records != []:
            dff = pd.concat(valid_records)
    if s1 >= 0 and s2 >= 0:
        salarymanagement = SalaryManagement(dff)
        min_salary = float(s1 * 1000000)
        max_salary = float(s2 * 1000000)
        valid_records = salarymanagement.get_salary(min_salary, max_salary, 70000)
        if valid_records != []:
            dff = pd.concat(valid_records)
    dff = dff.head(7000)
    data = dff.to_dict('records')
    tooltip_data = [
        {
            column: {'value': str(value), 'type': 'markdown'}
            for column, value in row.items()
        } for row in dff.to_dict('records')
    ]
    return data, tooltip_data


if __name__ == "__main__":
    app.run_server(debug=True)
