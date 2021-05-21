import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import numpy as np
import pandas as pd
#Hàm lọc theo giá trị cột
def find_df(d, label, data):
  dff = d[d[label] == data[0]]
  for i in range(len(data)-1):
    dff = pd.concat([dff, d[d[label] == data[i+1]]])
  return dff
#Hàm lọc theo search:
# def search(df, data):

df = pd.read_json('./job_news.json')
df = df.drop('_id', 1)
df = df.drop('crawled_time', 1)
dff = df
# page layout
app = dash.Dash(external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css'])

app.layout = html.Div([
    html.Div(children=[
            html.Div(children=[
              # chưa làm được hàm search
              dcc.Input(id='search', value='Hà Nội', type='text'),
              html.Button('search', id='submit-val', n_clicks=0),
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
                  value = "Hà Nội",
                  multi=True
              ),
              html.Label('Type'),

              dcc.Dropdown(
                  id='types',
                  # Nên sử dụng dạng sau:
                  # options=[{'label': i, 'value': i} for i in available_indicators],
                  options=[
                      {'label': 'Bán hàng', 'value': 'Bán hàng'},
                      {'label': 'Quản trị kinh doanh', 'value': 'Quản trị kinh doanh'},
                      {'label': 'Khách sạn - Nhà hàng', 'value': 'Khách sạn - Nhà hàng'},
                      {'label': 'Marketing - PR', 'value': 'Marketing - PR'},
                      {'label': 'Xây dựng', 'value': 'Xây dựng'},
                      {'label': 'Kế toán - Kiểm toán', 'value': 'Kế toán - Kiểm toán'},
                      {'label': 'Nhân sự', 'value': 'Nhân sự'},
                      {'label': 'Hành chính - văn phòng', 'value': 'Hành chính - văn phòng'},
                      {'label': 'KD bất động sản', 'value': 'KD bất động sản'},
                      {'label': 'An ninh - Bảo vệ', 'value': 'An ninh - Bảo vệ'},
                      {'label': 'Báo chí - Truyền hình', 'value': 'Báo chí - Truyền hình'},
                      {'label': 'Bảo hiểm', 'value': 'Bảo hiểm'},
                      {'label': 'Biên - Phiên dịch', 'value': 'Biên - Phiên dịch'},
                      {'label': 'Bưu chính', 'value': 'Bưu chính'},
                      {'label': 'Chứng khoán - vàng', 'value': 'Chứng khoán - vàng'},
                      {'label': 'Cơ khí - Chế tạo', 'value': 'Cơ khí - Chế tạo'},
                      {'label': 'Công nghệ cao', 'value': 'Công nghệ cao'},
                      {'label': 'Công nghiệp', 'value': 'Công nghiệp'},
                      {'label': 'Dầu khí - Hóa chất', 'value': 'Dầu khí - Hóa chất'},
                      {'label': 'Dệt may - Da giày', 'value': 'Dệt may - Da giày'},
                      {'label': 'Dịch vụ', 'value': 'Dịch vụ'},
                      {'label': 'Du lịch', 'value': 'Du lịch'},
                      {'label': 'Điện tử viễn thông', 'value': 'Điện tử viễn thông'},
                      {'label': 'Điện - Điện tử - Điện lạnh', 'value': 'Điện - Điện tử - Điện lạnh'},
                      {'label': 'Game', 'value': 'Game'},
                      {'label': 'Giáo dục - Đào tạo', 'value': 'Giáo dục - Đào tạo'},
                      {'label': 'Hàng gia dụng', 'value': 'Hàng gia dụng'},
                      {'label': 'Hàng hải', 'value': 'Hàng hải'},
                      {'label': 'Hàng không', 'value': 'Hàng không'},
                      {'label': 'Hóa hoc - Sinh học', 'value': 'Hóa hoc - Sinh học'},
                      {'label': 'Hoạch định dự án', 'value': 'Hoạch định dự án'},
                      {'label': 'In ấn - Xuất bản', 'value': 'In ấn - Xuất bản'},
                      {'label': 'IT phần cứng/mạng', 'value': 'IT phần cứng/mạng'},
                      {'label': 'IT phần mềm', 'value': 'IT phần mềm'},
                      {'label': 'Kho vận - Vật tư', 'value': 'Kho vận - Vật tư'},
                      {'label': 'Kiến trúc - TK nội thất', 'value': 'Kiến trúc - TK nội thất'},
                      {'label': 'Kỹ thuật', 'value': 'Kỹ thuật'},
                      {'label': 'Kỹ thuật ứng dụng', 'value': 'Kỹ thuật ứng dụng'},
                      {'label': 'Làm bán thời gian', 'value': 'Làm bán thời gian'},
                      {'label': 'Lao động phổ thông', 'value': 'Lao động phổ thông'},
                      {'label': 'Mỹ phẩm - Trang sức', 'value': 'Mỹ phẩm - Trang sức'},
                      {'label': 'Ngân hàng', 'value': 'Ngân hàng'},
                      {'label': 'Ngành nghề khác', 'value': 'Ngành nghề khác'},
                      {'label': 'Nghệ thuật - Điện ảnh', 'value': 'Nghệ thuật - Điện ảnh'},
                      {'label': 'Ngoại thương - Xuất nhập', 'value': 'Ngoại thương - Xuất nhập'},
                      {'label': 'Người giúp việc', 'value': 'Người giúp việc'},
                      {'label': 'Nhân viên kinh doanh', 'value': 'Nhân viên kinh doanh'},
                      {'label': 'Nông - Lâm - Ngư nghiệp', 'value': 'Nông - Lâm - Ngư nghiệp'},
                      {'label': 'NV trông quán Internet', 'value': 'NV trông quán Internet'},
                      {'label': 'Ô tô - Xe máy', 'value': 'Ô tô - Xe máy'},
                      {'label': 'Pháp lý - Luật', 'value': 'Pháp lý - Luật'},
                      {'label': 'Promotion Girl', 'value': 'Promotion Girl'},
                      {'label': 'Quan hệ đối ngoại', 'value': 'Quan hệ đối ngoại'},
                      {'label': 'Sinh viên làm thêm', 'value': 'Sinh viên làm thêm'},
                      {'label': 'Tài chính đầu tư', 'value': 'Tài chính đầu tư'},
                      {'label': 'Thiết kế đồ họa', 'value': 'Thiết kế đồ họa'},
                      {'label': 'Thiết kế - Mỹ thuật', 'value': 'Thiết kế - Mỹ thuật'},
                      {'label': 'Thời trang', 'value': 'Thời trang'},
                      {'label': 'Thủ công mỹ nghệ', 'value': 'Thủ công mỹ nghệ'},
                      {'label': 'Thư ký - Trợ lý', 'value': 'Thư ký - Trợ lý'},
                      {'label': 'Thực phẩm - Đồ uống', 'value': 'Thực phẩm - Đồ uống'},
                      {'label': 'Thực tập', 'value': 'Thực tập'},
                      {'label': 'Thương mại điện tử', 'value': 'Thương mại điện tử'},
                      {'label': 'Tiếp thị - Quảng cáo', 'value': 'Tiếp thị - Quảng cáo'},
                      {'label': 'Tổ chức sự kiện - Quà tặng', 'value': 'Tổ chức sự kiện - Quà tặng'},
                      {'label': 'Tư vấn', 'value': 'Tư vấn'},
                      {'label': 'Vận tải lái xe', 'value': 'Vận tải lái xe'},
                      {'label': 'Y tế - Dược', 'value': 'Y tế - Dược'},
                  ],
                  value = "Y tế - Dược",
                  multi=True
              ),
              
          ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
          html.Div(children=[
            html.Label('Salary'),
            dcc.RadioItems(
              # chưa đưa ra được option chính xác về lương
                options=[
                    {'label': '<1 triệu', 'value': '1'},
                    {'label': u'1-10 triệu', 'value': '2'},
                    {'label': '10-50 triệu', 'value': '3'},
                    {'label': '>50 triệu', 'value': '4'},
                    {'label': 'thương lượng', 'value': '5'}
                ],
                value='2',
                labelStyle={'display': 'block'}
            ),

        ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '10%', 'margin-top': '3vw'}),
          # third column of first row
          html.Div(children=[
              html.Label('Degree'),
              dcc.RadioItems(
                # chưa đưa ra được chính xác option về bằng cấp
                  id='degree', 
                  options=[
                      {'label': 'Không yêu cầu', 'value': 'Không yêu cầu'},
                      {'label': u'Trung học', 'value': 'Trung học'},
                      {'label': 'Trung cấp', 'value': 'Trung cấp'},
                      {'label': 'Cao đẳng', 'value': 'Cao đẳng'},
                      {'label': 'Đại học', 'value': 'Đại học'},
                      {'label': 'Trên đại học', 'value': 'Trên đại học'}

                  ],
                  value='Trung học',
                  labelStyle={'display': 'block'}
              ),

          ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
          html.Div(children=[
              html.Label('Experience'),
              dcc.RadioItems(
                id='experience',
                  options=[
                      {'label': u'dưới 1 năm', 'value': 'dưới 1 năm'},
                      {'label': '1-5 năm', 'value': '1-5 năm'},
                      {'label': 'trên 5 năm', 'value': 'trên 5 năm'}
                  ],
                  value='dưới 1 năm',
                  labelStyle={'display': 'block'}
              ),

          ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
          html.Div(children=[
              html.Label('Gender'),
              dcc.RadioItems(
                  id='gender',
                  options=[
                      {'label': 'Nam', 'value': 'Nam'},
                      {'label': u'Nữ', 'value': 'Nữ'},
                      {'label': 'Không yêu cầu', 'value':'Không yêu cầu'},
                  ],
                  value='Nữ',
                  labelStyle={'display': 'block'}
              )

          ], style={'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '5%', 'margin-top': '3vw'}),
        ],className='row'),

    # second row
    html.Div(children=[
        html.H3(children='DATA JOB TABLE'),
        dash_table.DataTable(
          id='datatable-interactivity',
          style_data={
            'whiteSpace': 'normal',
          },
          data=dff.to_dict('records'),
          columns=[
              {"name": i, "id": i,} for i in dff.columns
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
              } for row in dff.to_dict('records')
          ],
          tooltip_duration=None,

          style_cell={
            'textAlign': 'left',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'whiteSpace': 'normal',
            'minWidth': '80px', 'width': '80px', 'maxWidth': '80px',
            }, # left align text in columns for readability
          # style_table={'height': 1000},
          
          editable=True,
          filter_action="native",
          sort_action="native",
          sort_mode="multi",
          column_selectable="single",
          row_selectable="multi",
#           selected_columns=[],
#           selected_rows=[],
          page_action="native",
          page_current= 0,
          page_size= 10,
    ),

    ], className='row',style={'display': 'inline-block', 'vertical-align': 'top'}),

])
# Hàm callback đưa ra dữ liệu sau mỗi lần lựa chọn thay đổi giá trị trong bảng
@app.callback(
    Output(component_id='datatable-interactivity', component_property='data'),
    Output(component_id='datatable-interactivity', component_property='tooltip_data'),
    # Input(component_id='search', component_property='value'),
    Input(component_id='location', component_property='value'),
    Input(component_id='types', component_property='value'),
    # Input(component_id='degree', component_property='value'),
    # Input(component_id='experience', component_property='value'),
    # Input(component_id='gender', component_property='value'),
)


# def update_data(search_, location_, types_, degree_, experience_, gender_):
def update_data(, location_, types_):
  # search trả về value
  # if search_!='':
  # Viết hàm search tìm các dữ liệu theo search rồi gán cho dataframe dff
  if location_ != [] and types_ != []:
    dff = find_df(df, 'working_location', location_)
    dff = find_df(df, 'types', types_)
    # dff = find_df(df, 'degree', degree_)
    # dff = find_df(df, 'experience', experience_)
    # dff = find_df(df, 'gender', gender_)
  elif types_ != []:
    dff = find_df(df, 'types', types_)
    # dff = find_df(df, 'degree', degree_)
    # dff = find_df(df, 'experience', experience_)
    # dff = find_df(df, 'gender', gender_)
  elif location_ != []:
    dff = find_df(df, 'working_location', location_)
    # dff = find_df(df, 'degree', degree_)
    # dff = find_df(df, 'experience', experience_)
    # dff = find_df(df, 'gender', gender_)
  else: 
    dff = df
    # dff = find_df(df, 'degree', degree_)
    # dff = find_df(df, 'experience', experience_)
    # dff = find_df(df, 'gender', gender_)
  data = dff.to_dict('records')
  tooltip_data=[
      {
          column: {'value': str(value), 'type': 'markdown'}
          for column, value in row.items()
      } for row in dff.to_dict('records')
  ]
  return data, tooltip_data




if __name__ == "__main__":
    app.run_server(debug=True)
