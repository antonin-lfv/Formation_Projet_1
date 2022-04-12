""" Projet numéro 1 : Dashboard de la bourse """

import streamlit as st

from utils import *

st.set_page_config(layout="wide", page_title="Projet 1 : Dashboard", menu_items={
    'About': "Projet numéro 1 - Machine Learnia"
})

st.markdown("""
<style>
.first_titre {
    font-size:60px !important;
    font-weight: bold;
    box-sizing: border-box;
    text-align: center;
    width: 100%;
}
.market_name {
    font-size:30px !important;
    font-weight: bold;
    text-decoration: underline;
    text-decoration-color: #4976E4;
    text-decoration-thickness: 5px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.subheader("Plot the history from " + today_string)
st.sidebar.write("###")
market = st.sidebar.selectbox(
    'Select a market',
    SP.keys()
)
st.sidebar.write("###")
INCREASING_COLOR = st.sidebar.color_picker('Pick A Color for Candlestick increasing values', '#30A03E')
DECREASING_COLOR = st.sidebar.color_picker('Pick A Color for Candlestick decreasing values', '#E94C1A')

# Main page
st.markdown('<p class="first_titre">DashBoard</p>', unsafe_allow_html=True)
st.write("---")

st.write("###")
st.markdown('<p class="market_name">' + market + ' history</p>', unsafe_allow_html=True)
st.plotly_chart(plot_market(add_metrics(get_one_market(market)), INCREASING_COLOR, DECREASING_COLOR),
                use_container_width=True)
