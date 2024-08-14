import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
st.title(":coin: Dự liệu ngành Ngân Hàng :coin:",anchor=False)
st.markdown("-----")
options = ["All", "VPB", "VIB", "VCB","VBB","VAB","TPB","TIN","TCB","STB","SBB","SHB","SGB","PGB","OCB","NVB","MSB","MBB","LPB","HDB","KL"
           ,"KLB","EIB","CTG","BID","BVB","ACB","BAB","ABB","NAB"]
selected_option = st.selectbox("MÃ", options)
st.session_state.selected_option = selected_option


st.write(f"Bạn đã chọn: {selected_option}")
st.markdown("-----")
# Đọc một sheet cụ thể
df_sheet1 = pd.read_excel('E:\Bank_Q22024.xlsm', sheet_name=selected_option)
df_sheet1= df_sheet1.fillna(" ")
df_sheet1.columns = df_sheet1.iloc[2]  # Đặt dòng thứ 3 làm tiêu đề
df_sheet1 = df_sheet1.drop(df_sheet1.index[0:3])  # Xóa 3 dòng đầu tiên (bao gồm dòng tiêu đề cũ)

# Đặt lại chỉ số (index)
df_sheet1.reset_index(drop=True, inplace=True)
st.write("Bảng cân đối kế toán")
st.dataframe(df_sheet1.head(98))
st.markdown("-----")
st.write("Báo cáo thu nhập")
st.dataframe(df_sheet1.iloc[98:124])
st.markdown("-----")
st.write("Lưu chuyển tiền tệ")
st.dataframe(df_sheet1.iloc[124:231])
st.markdown("-----")
st.write("Thuyết Minh")
st.dataframe(df_sheet1.iloc[231:437])

# Đọc file Excel và lấy dữ liệu từ sheet 1


# Giả sử ROE và ROA nằm trong các dòng riêng biệt và có thể được tìm thấy bằng cách tìm kiếm từ khóa
# Tìm các dòng liên quan đến ROE và ROA
roe_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('ROE', na=False)].index[0]
roa_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('ROA', na=False)].index[0]

# Lấy dữ liệu ROE và ROA từ các dòng đó
roe_data = df_sheet1.iloc[roe_index, 1:].dropna()*100
roa_data = df_sheet1.iloc[roa_index, 1:].dropna()*100

# Chuyển dữ liệu ROE và ROA thành DataFrame
roe_df = pd.DataFrame({
    'Quý': roe_data.index,
    'ROE': roe_data.values
})

roa_df = pd.DataFrame({
    'Quý': roa_data.index,
    'ROA': roa_data.values
})

# Gộp dữ liệu ROE và ROA vào cùng một DataFrame
combined_df = pd.merge(roe_df, roa_df, on='Quý')
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    # Nếu không thể chuyển đổi thành datetime, sắp xếp theo thứ tự mà bạn mong muốn
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')
# Vẽ biểu đồ cho ROE và ROA
fig0 = go.Figure()

# Thêm các đường chính (NIM, COF, YEOA) với giá trị tại mỗi điểm
fig0.add_trace(go.Scatter(
    x=combined_df['Quý'], y=combined_df['ROE'],
    mode='lines+markers+text',
    line_shape='spline',
    name='ROE',
    text=[f'{x:.2f}%' if i == len(combined_df['ROE']) - 1 else '' for i, x in enumerate(combined_df['ROE'])],
    textposition='top center'  # Vị trí của nhãn
))

fig0.add_trace(go.Scatter(
    x=combined_df['Quý'], y=combined_df['ROA'],
    mode='lines+markers+text',
    line_shape='spline',
    name='ROA',
    text=[f'{x:.2f}%' if i == len(combined_df['ROA']) - 1 else '' for i, x in enumerate(combined_df['ROA'])],
    textposition='top center'  # Vị trí của nhãn
))

fig0.update_layout(
    title='Biểu ROE,ROA(%)',
    xaxis_title='Quý',
    yaxis_title='Giá trị (%)',
    legend_title='Chỉ số'
)

# Hiển thị biểu đồ trên Streamlit


#dữ liệu NIM COF và YEOA

# Tìm các dòng liên quan đến NIM, COF, và YEOA
nim_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Nim', na=False)].index[0]
cof_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('COF', na=False)].index[0]
yeoa_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('YEOA', na=False)].index[0]

# Lấy dữ liệu từ các dòng đó
nim_data = df_sheet1.iloc[nim_index, 1:].dropna()*100
cof_data = df_sheet1.iloc[cof_index, 1:].dropna()*100
yeoa_data = df_sheet1.iloc[yeoa_index, 1:].dropna()*100

# Chuyển dữ liệu thành DataFrame
nim_df = pd.DataFrame({
    'Quý': nim_data.index,
    'NIM': nim_data.values
})

cof_df = pd.DataFrame({
    'Quý': cof_data.index,
    'COF': cof_data.values
})

yeoa_df = pd.DataFrame({
    'Quý': yeoa_data.index,
    'YEOA': yeoa_data.values
})

# Gộp dữ liệu NIM, COF, và YEOA vào cùng một DataFrame
combined_df1 = pd.merge(nim_df, cof_df, on='Quý')
combined_df1 = pd.merge(combined_df1, yeoa_df, on='Quý')

# Đảo ngược thứ tự trục X (Quý) nếu cần
try:
    combined_df1['Quý'] = pd.to_datetime(combined_df1['Quý'], format='%Y-%m-%d')
    combined_df1 = combined_df1.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df1['Quý'] = pd.Categorical(combined_df1['Quý'], categories=combined_df1['Quý'].unique()[::-1], ordered=True)
    combined_df1 = combined_df1.sort_values(by='Quý')

# Vẽ biểu đồ
fig1 = go.Figure()

# Thêm các đường chính (NIM, COF, YEOA) với giá trị tại mỗi điểm
fig1.add_trace(go.Scatter(
    x=combined_df1['Quý'], y=combined_df1['NIM'],
    mode='lines+markers+text',
    line_shape='spline',
    name='NIM',
    text=[f'{x:.2f}%' if i == len(combined_df1['NIM']) - 1 else '' for i, x in enumerate(combined_df1['NIM'])],
    textposition='top center'  # Vị trí của nhãn
))

fig1.add_trace(go.Scatter(
    x=combined_df1['Quý'], y=combined_df1['COF'],
    mode='lines+markers+text',
    line_shape='spline',
    name='COF',
    text=[f'{x:.2f}%' if i == len(combined_df1['COF']) - 1 else '' for i, x in enumerate(combined_df1['COF'])],
    textposition='top center'  # Vị trí của nhãn
))

fig1.add_trace(go.Scatter(
    x=combined_df1['Quý'], y=combined_df1['YEOA'],
    mode='lines+markers+text',
    line_shape='spline',
    name='YEOA',
    text=[f'{x:.2f}%' if i == len(combined_df1['YEOA']) - 1 else '' for i, x in enumerate(combined_df1['YEOA'])],
    textposition='bottom center'  # Vị trí của nhãn
))

# Cập nhật bố cục biểu đồ
fig1.update_layout(
    title='Biểu đồ NIM, COF, YEOA (%)',
    xaxis_title='Quý',
    yaxis_title='Giá trị (%)',
    legend_title='Chỉ số'
)

# Hiển thị biểu đồ trong Streamlit
# biểu đồ casa
casa_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Casa', na=False)].index
casa_data = df_sheet1.iloc[casa_index[0], 1:].dropna()*100
    
# Chuyển đổi dữ liệu thành DataFrame
casa_df = pd.DataFrame({
        'Quý': casa_data.index,
        'CASA': casa_data.values
    })
try:
    casa_df['Quý'] = pd.to_datetime(casa_df['Quý'], format='%Y-%m-%d')
    casa_df = casa_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    casa_df['Quý'] = pd.Categorical(casa_df['Quý'], categories=casa_df['Quý'].unique()[::-1], ordered=True)
    casa_df = casa_df.sort_values(by='Quý')
fig2 = go.Figure(data=[
        go.Bar(x=casa_df['Quý'], y=casa_df['CASA'], text=casa_df['CASA'], textposition='outside')
    ])

# Cập nhật tiêu đề và nhãn trục
fig2 = go.Figure(data=[
        go.Bar(x=casa_df['Quý'], y=casa_df['CASA'], text=casa_df['CASA'], textposition='outside',
               texttemplate='%{text:.2f}%')  # Định dạng giá trị hiển thị là phần trăm
    ])

    # Cập nhật tiêu đề, nhãn trục và hiển thị giá trị trên mỗi cột
fig2.update_layout(
        title='Biểu đồ CASA theo Quý',
        xaxis_title='Quý',
        yaxis_title='Giá trị CASA (%)',
        showlegend=False
    )

    # Hiển thị biểu đồ trong Streamlit


# Dư liệu nợ xấu

# Tìm các dòng liên quan đến Nợ xấu nhóm 1, 2, 3, 4, 5, tỷ lệ nợ xấu, và tỷ lệ bao phủ nợ xấu

nhom3_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Nợ xấu nhóm 3', na=False)].index[0]
nhom4_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Nợ xấu nhóm 4', na=False)].index[0]
nhom5_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Nợ xấu nhóm 5', na=False)].index[0]
ty_le_no_xau_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Tỷ lệ nợ xấu', na=False)].index[0]

# Lấy dữ liệu từ các dòng đó
nhom3_data = df_sheet1.iloc[nhom3_index, 1:].dropna()
nhom4_data = df_sheet1.iloc[nhom4_index, 1:].dropna()
nhom5_data = df_sheet1.iloc[nhom5_index, 1:].dropna()
ty_le_no_xau_data = df_sheet1.iloc[ty_le_no_xau_index, 1:].dropna()*100

# Chuyển dữ liệu thành DataFrame
combined_df = pd.DataFrame({
     'Quý': nhom5_data.index,
    'Nợ xấu nhóm 3': nhom3_data.values,
    'Nợ xấu nhóm 4': nhom4_data.values,
    'Nợ xấu nhóm 5': nhom5_data.values,
    'Tỷ lệ nợ xấu': ty_le_no_xau_data.values,
})
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')
# Vẽ biểu đồ
fig3 = go.Figure()

# Thêm các cột trồng cho Nợ xấu nhóm 1, 2, 3, 4, 5
fig3.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Nợ xấu nhóm 3'], name='Nợ xấu nhóm 3'))
fig3.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Nợ xấu nhóm 4'], name='Nợ xấu nhóm 4'))
fig3.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Nợ xấu nhóm 5'], name='Nợ xấu nhóm 5'))

# Thêm biểu đồ đường cho Tỷ lệ nợ xấu và Tỷ lệ bao phủ nợ xấu với trục Y phụ
fig3.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Tỷ lệ nợ xấu'], name='Tỷ lệ nợ xấu', 
                         mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.2f}%' if i == len(combined_df['Tỷ lệ nợ xấu']) - 1 else '' for i, x in enumerate(combined_df['Tỷ lệ nợ xấu'])],
                         textposition='bottom center',
                         yaxis='y2' ))# Vị trí của nhãn yaxis='y2'))

# Cập nhật layout để sử dụng trục Y phụ
fig3.update_layout(
    title='Biểu đồ kết hợp Nợ xấu nhóm 3, 4, 5 và Tỷ lệ nợ xấu, Tỷ lệ bao phủ nợ xấu',
    xaxis_title='Quý',
    yaxis_title='Giá trị Nợ xấu',
    yaxis2=dict(title='Tỷ lệ (%)', overlaying='y', side='right'),
    barmode='stack',
    legend=dict(x=0.1, y=1.1, orientation='h')
)

# Hiển thị biểu đồ trong Streamlit



### Biểu đồ LDR ###############
import pandas as pd
import plotly.graph_objects as go

# Đọc dữ liệu từ file Excel

# Tìm các dòng liên quan đến Tiền gửi khách hàng, Cho vay khách hàng, và LDR
tien_gui_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Tiền gửi khách hàng', na=False)].index[0]
cho_vay_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Cho vay khách hàng', na=False)].index[0]
ldr_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('LDR', na=False)].index[0]

# Lấy dữ liệu từ các dòng đó
tien_gui_data = df_sheet1.iloc[tien_gui_index, 1:].dropna()/1000000000
cho_vay_data = df_sheet1.iloc[cho_vay_index, 1:].dropna()/1000000000
ldr_data = df_sheet1.iloc[ldr_index, 1:].dropna()*100

# Chuyển dữ liệu thành DataFrame
combined_df = pd.DataFrame({
    'Quý': tien_gui_data.index,
    'Tiền gửi khách hàng': tien_gui_data.values,
    'Cho vay khách hàng': cho_vay_data.values,
    'LDR': ldr_data.values
})
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')
# Vẽ biểu đồ
fig4 = go.Figure()

# Thêm các cột cho Tiền gửi khách hàng và Cho vay khách hàng
fig4.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Tiền gửi khách hàng'], name='Tiền gửi khách hàng'))
fig4.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Cho vay khách hàng'], name='Cho vay khách hàng'))
# Thêm biểu đồ đường cho LDR với trục Y phụ
fig4.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['LDR'], name='LDR', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.2f}%' if i == len(combined_df['LDR']) - 1 else '' for i, x in enumerate(combined_df['LDR'])],
                         textposition='bottom center',
                         yaxis='y2' ))# Vị trí của nhãn yaxis='y2'))
                    
# Cập nhật layout để sử dụng trục Y phụ
fig4.update_layout(
    title='Biểu đồ kết hợp Tiền gửi khách hàng, Cho vay khách hàng và LDR',
    xaxis_title='Quý',
    yaxis_title='Giá trị (Tỷ VND)',
    yaxis2=dict(title='Tỷ lệ LDR (%)', overlaying='y', side='right'),
    barmode='group',
    legend=dict(x=0.1, y=1.1, orientation='h')
)

# Hiển thị biểu đồ
############ Tỷ lệ đòn bẩy ##############

TTS_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('TTS', na=False)].index[0]
VCSH_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('VCSH', na=False)].index[0]
leverage_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Tỷ lệ đòn bẩy', na=False)].index[0]

TTS_data = df_sheet1.iloc[TTS_index, 1:].dropna()/1000000000
VCSH_data = df_sheet1.iloc[VCSH_index, 1:].dropna()/1000000000
leverage_data = df_sheet1.iloc[leverage_index, 1:].dropna()

combined_df = pd.DataFrame({
    'Quý': TTS_data.index,
    'Tổng tài sản': TTS_data.values,
    'Vốn chủ sở hữu': VCSH_data.values,
    'Tỷ lệ đòn bẩy': leverage_data.values
})
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')
#Vẽ biểu đồ


### Biên lợi nhuận #####
cir_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('CIR', na=False)].index[0]
bienrong_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Biên lãi ròng', na=False)].index[0]
bienthuan_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Biên lợi nhuận trước chi phí rủi ro tín dụng', na=False)].index[0]

cir_data = df_sheet1.iloc[cir_index, 1:].dropna()*100
bienrong_data = df_sheet1.iloc[bienrong_index, 1:].dropna()*100
bienthuan_data = df_sheet1.iloc[bienthuan_index, 1:].dropna()*100

combined_df = pd.DataFrame({
    'Quý': cir_data.index,
    'CIR': cir_data.values,
    'Biên lãi ròng': bienrong_data.values,
    'Biên lợi nhuận trước chi phí rủi ro tín dụng': bienthuan_data.values
})
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')
#Vẽ biểu đồ

fig6 = go.Figure()

# Thêm các cột cho Tiền gửi khách hàng và Cho vay khách hàng
fig6.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['CIR'], name='CIR'))
# Thêm biểu đồ đường cho LDR với trục Y phụ
fig6.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Biên lãi ròng'], name='Tỷ lệ đòn bẩy', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.1f} %' if i == len(combined_df['Biên lãi ròng']) - 1 else '' for i, x in enumerate(combined_df['Biên lãi ròng'])],
                         textposition='top center' ))
fig6.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Biên lợi nhuận trước chi phí rủi ro tín dụng'], name='Biên lợi nhuận trước chi phí rủi ro tín dụng', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.1f} %' if i == len(combined_df['Biên lợi nhuận trước chi phí rủi ro tín dụng']) - 1 else '' for i, x in enumerate(combined_df['Biên lợi nhuận trước chi phí rủi ro tín dụng'])],
                         textposition='top center' ))# Vị trí của nhãn yaxis='y2'))
                    
# Cập nhật layout để sử dụng trục Y phụ
fig6.update_layout(
    title='Biểu đồ Biên lợi nhuận',
    xaxis_title='Quý',
    yaxis_title='Giá trị (%)',
    legend=dict(x=0.1, y=1.1, orientation='h')
)

# Hiển thị biểu đồ

############### Tăng trưởng thu nhập và lợi nhuận #######################
TTS_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('TTS', na=False)].index[0]
VCSH_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('VCSH', na=False)].index[0]
leverage_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Tỷ lệ đòn bẩy', na=False)].index[0]

TTS_data = df_sheet1.iloc[TTS_index, 1:].dropna()/1000000000
VCSH_data = df_sheet1.iloc[VCSH_index, 1:].dropna()/1000000000
leverage_data = df_sheet1.iloc[leverage_index, 1:].dropna()

combined_df = pd.DataFrame({
    'Quý': TTS_data.index,
    'Tổng tài sản': TTS_data.values,
    'Vốn chủ sở hữu': VCSH_data.values,
    'Tỷ lệ đòn bẩy': leverage_data.values
})
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')
#Vẽ biểu đồ

fig7 = go.Figure()

# Thêm các cột cho Tiền gửi khách hàng và Cho vay khách hàng
fig7.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Tổng tài sản'], name='Tổng tài sản'))
fig7.add_trace(go.Bar(x=combined_df['Quý'], y=combined_df['Vốn chủ sở hữu'], name='Vốn chủ sở hữu'))

# Thêm biểu đồ đường cho LDR với trục Y phụ
fig7.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Tỷ lệ đòn bẩy'], name='Tỷ lệ đòn bẩy', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.2f} lần' if i == len(combined_df['Tỷ lệ đòn bẩy']) - 1 else '' for i, x in enumerate(combined_df['Tỷ lệ đòn bẩy'])],
                         textposition='top center',
                         yaxis='y2' ))# Vị trí của nhãn yaxis='y2'))
                    
# Cập nhật layout để sử dụng trục Y phụ
fig7.update_layout(
    title='Biểu đồ Tỷ lệ đòn bẩy',
    xaxis_title='Quý',
    yaxis_title='Giá trị (Tỷ VND)',
    yaxis2=dict(title='Tỷ lệ đòn bẩy (lần)', overlaying='y', side='right'),
    barmode='group',
    legend=dict(x=0.1, y=1.1, orientation='h')
)

# Hiển thị biểu đồ
### Biên lợi nhuận #####
lnst_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Tăng trưởng LNST', na=False)].index[0]
laithuan_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Tăng trưởng thu nhập lãi thuần', na=False)].index[0]
ngoailai_index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('Thu nhập ngoài lãi', na=False)].index[0]

lnst_data = df_sheet1.iloc[lnst_index, 1:].dropna()*100
laithuan_data = df_sheet1.iloc[laithuan_index, 1:].dropna()*100
ngoailai_data = df_sheet1.iloc[ngoailai_index, 1:].dropna()*100

combined_df = pd.DataFrame({
    'Quý': lnst_data.index,
    'Tăng trưởng LNST': lnst_data.values,
    'Tăng trưởng thu nhập lãi thuần': laithuan_data.values,
    'Tăng trưởng thu nhập ngoài lãi': ngoailai_data.values
})
try:
    combined_df['Quý'] = pd.to_datetime(combined_df['Quý'], format='%Y-%m-%d')
    combined_df = combined_df.sort_values(by='Quý', ascending=False)
except Exception as e:
    combined_df['Quý'] = pd.Categorical(combined_df['Quý'], categories=combined_df['Quý'].unique()[::-1], ordered=True)
    combined_df = combined_df.sort_values(by='Quý')

#Vẽ biểu đồ

fig8 = go.Figure()

# Thêm các cột cho Tiền gửi khách hàng và Cho vay khách hàng
fig8.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Tăng trưởng LNST'], name='Tăng trưởng LNST', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.1f} %' if i == len(combined_df['Tăng trưởng LNST']) - 1 else '' for i, x in enumerate(combined_df['Tăng trưởng LNST'])],
                         textposition='top center' ))
# Thêm biểu đồ đường cho LDR với trục Y phụ
fig8.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Tăng trưởng thu nhập lãi thuần'], name='Tăng trưởng thu nhập lãi thuần', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.1f} %' if i == len(combined_df['Tăng trưởng thu nhập lãi thuần']) - 1 else '' for i, x in enumerate(combined_df['Tăng trưởng thu nhập lãi thuần'])],
                         textposition='top center' ))
fig8.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Tăng trưởng thu nhập ngoài lãi'], name='Tăng trưởng thu nhập ngoài lãi', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.1f} %' if i == len(combined_df['Tăng trưởng thu nhập ngoài lãi']) - 1 else '' for i, x in enumerate(combined_df['Tăng trưởng thu nhập ngoài lãi'])],
                         textposition='top center' ))# Vị trí của nhãn yaxis='y2'))
                    
# Cập nhật layout để sử dụng trục Y phụ
fig8.update_layout(
    title='Tăng trưởng thu nhập và lợi nhuận',
    xaxis_title='Quý',
    yaxis_title='Giá trị (%)',
    legend=dict(x=0.1, y=1.1, orientation='h')
)


####### Ve bieu do co cau doanh thu ###############

keywords = [
    'Thu nhập lãi thuần', 
    'Lãi thuần từ hoạt động dịch vụ',
    'Lãi/lỗ thuần từ hoạt động kinh doanh ngoại hối và vàng',
    'Lãi/lỗ thuần từ mua bán chứng khoán kinh doanh',
    'Lãi/lỗ thuần từ mua bán chứng khoán đầu tư',
    'Lãi/lỗ thuần từ hoạt động khác',
    'Thu nhập từ góp vốn, mua cổ phần'
]

# Lấy dữ liệu từ các dòng liên quan đến cơ cấu doanh thu
doanh_thu_data = {}
for keyword in keywords:
    index = df_sheet1[df_sheet1.iloc[:, 0].str.contains(keyword, na=False)].index
    if len(index) > 0:
        doanh_thu_data[keyword] = df_sheet1.iloc[index[0], 1:].dropna().values

# Tạo DataFrame từ dữ liệu doanh thu
combined_df = pd.DataFrame(doanh_thu_data, index=df_sheet1.columns[1:len(list(doanh_thu_data.values())[0])+1])

fig9= go.Figure()

for column in combined_df.columns:
    fig9.add_trace(go.Bar(
        x=combined_df.index,
        y=combined_df[column],
        name=column
    ))
LNsauthue__index = df_sheet1[df_sheet1.iloc[:, 0].str.contains('LNST', na=False)].index[0]
LNsauthue_data = df_sheet1.iloc[LNsauthue__index, 1:].dropna()
combined_df = pd.DataFrame({
    'Quý': LNsauthue_data.index,
    'Lợi nhuận sau thuế': LNsauthue_data.values,})
fig9.add_trace(go.Scatter(x=combined_df['Quý'], y=combined_df['Lợi nhuận sau thuế'], name='Lợi nhuận sau thuế', mode='lines+markers+text',
                         line_shape='spline',
                         text=[f'{x:.1f} %' if i == len(combined_df['Lợi nhuận sau thuế']) - 1 else '' for i, x in enumerate(combined_df['Lợi nhuận sau thuế'])],
                         textposition='top center' ))# Vị trí của nhãn yaxis='y2'))
# Cập nhật layout của biểu đồ
fig9.update_layout(
    title='Biểu đồ cột chồng về cơ cấu doanh thu',
    xaxis_title='Quý',
    yaxis_title='Giá trị doanh thu (VND)',
    barmode='stack',
    xaxis=dict(autorange='reversed'),
    
)
# Hiển thị biểu đồ

# Chia trang thành ba cột
col1, col2 = st.columns(2)


with col1:
    st.write(fig9)
# Thêm nội dung vào cột 2
with col2:
    st.write(fig1)

# Thêm biểu đồ vào cột 3



 ############################################
col3, col4 = st.columns(2)
with col3:

    st.write(fig8)

# Thêm biểu đồ vào cột 3
with col4:

    st.plotly_chart(fig0)
 ############################################
 
col5, col6 = st.columns(2)
with col5:

    st.write(fig4)

# Thêm biểu đồ vào cột 3
with col6:

    st.plotly_chart(fig6)


col7, col8 = st.columns(2)
with col7:

    st.write(fig2)

# Thêm biểu đồ vào cột 3
with col8:

    st.plotly_chart(fig3)

col9, col10 = st.columns(2)
with col9:

    st.write(fig7)

# Thêm biểu đồ vào cột 3