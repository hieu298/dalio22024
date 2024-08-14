import pandas as pd
import streamlit as st
import plotly.graph_objects as go
selected_option = st.session_state.get("selected_option", "Chưa có tùy chọn nào được chọn")

st.write(f"Giá trị selected_option từ Sales Dashboard: {selected_option}")